#!/usr/bin/env python
import json
import sys


def read_jsonfile(file):
    """
    Parse the input JSON file and return a dictionary with the info
    """
    with open(file) as data:
        json_data = json.load(data)
    return(json_data)


def write_PBSheader(job_number, json):
    """
    Writes the header with the PBS information
    """
    file = open("job%s.sh" % job_number, "w")
    file.write("#PBS -N job%s\n" % job_number)
    file.write("#PBS -l select=%s\n" % json['pbs_settings']['nnodes'])
    file.write("#PBS -l ncpus=%s:ngpus=%s\n" % (json['pbs_settings']['ncpus'],
                                                json['pbs_settings']['ngpus']))
    file.write("#PBS -l walltime=%s\n" % json['pbs_settings']['walltime'])
    file.write("#PBS -l host=%s\n" % json['pbs_settings']['host'])
    file.write("#PBS -q %s\n" % json['pbs_settings']['queue'])
    file.write("#PBS -M %s\n" % json['pbs_settings']['email'])
    file.write("#PBS -m abe\n\n")
    file.close()


def write_MDscript(job_number, json, timeList):
    with open("job%s.sh" % job_number, "a") as file:
        if job_number == 1:
            file.write("module load cuda/6.5.19\n\n")

            file.write("inpcrd=%s\n" % json['simulation_details']['inpcrd_file'])
            file.write("prmtop=%s\n" % json['simulation_details']['topology_file'])
            file.write("sim=%s\n\n" % timeList[job_number])

            file.write("cd /tmp/pbs.${PBS_JOBID}\n")
            file.write("cp %s/*.in .\n" % json['simulation_details']['job_directory'])
            file.write("cp %s/${inpcrd} .\n" % json['simulation_details']['job_directory'])
            file.write("cp %s/${prmtop} .\n\n" % json['simulation_details']['job_directory'])

            file.write("""/home/igould/pmemd.cuda_SPFP -O -i premin.in \ 
    -o premin.out -c ${inpcrd} -p ${prmtop} \ 
    -r premin.rst -ref ${inpcrd}\n\n""")

            file.write("""/home/igould/pmemd.cuda_SPFP -O -i sandermin1.in \ 
    -o sandermin1.out -c premin.rst -p ${prmtop} \ 
    -r sandermin1.rst\n\n""")

            file.write("""/home/igould/pmemd.cuda_SPFP -O -i 02_Heat.in \ 
    -o 02_Heat.out -c sandermin1.rst -p ${prmtop} \ 
    -r 02_Heat.rst -ref sandermin1.rst -x 02_Heat.nc\n\n""")

            file.write("""/home/igould/pmemd.cuda_SPFP -O -i 03_Heat2.in \ 
    -o 03_Heat2.out -c 02_Heat.rst -p ${prmtop} \ 
    -r 03_Heat2.rst -ref 02_Heat.rst -x 03_Heat2.nc\n\n""")


            file.write("""pbsexec -grace 30 /home/igould/pmemd.cuda_SPFP -O -i 05_Prod.in \ 
    -o %s_${sim}ns.out -c 03_Heat2.rst -p ${prmtop} \ 
    -r %s_${sim}ns.rst -x %s_${sim}ns.nc\n\n""" % (json['simulation_details']['system_name'],
                                                   json['simulation_details']['system_name'],
                                                   json['simulation_details']['system_name']))

            file.write("cp /tmp/pbs.${JOB_ID}/%s_${sim}ns.rst %s/\n" % (json['simulation_details']['system_name'],
                                                                        json['simulation_details']['job_directory']))
            file.write("rm /tmp/pbs.${JOB_ID}/${inpcrd}\n")
            file.write("tar -zcvf %s/results/%s_${sim}ns.tgz *\n\n" % (json['simulation_details']['job_directory'],
                                                                       json['simulation_details']['system_name']))
            file.write("scp %s/results/%s_${sim}ns.tgz \ \n\t%s@%s:%s/" % (json['simulation_details']['job_directory'],
                                                                           json['simulation_details']['system_name'],
                                                                           json['local_machine']['user'],
                                                                           json['local_machine']['hostname'],
                                                                           json['local_machine']['destination']))

        else:
            file.write("module load cuda/6.5.19\n\n")

            file.write("prevrst=%s_%sns.rst\n" % (json['simulation_details']['system_name'],
                                                  timeList[job_number - 1]))
            file.write("prmtop=%s\n" % json['simulation_details']['topology_file'])
            file.write("prevsim=%s\n" % timeList[job_number - 1])
            file.write("sim=%s\n\n" % timeList[job_number])


            file.write("cd /tmp/pbs.${PBS_JOBID}\n")
            file.write("cp %s/05_Prod.in .\n" % json['simulation_details']['job_directory'])
            file.write("cp %s/${prevrst} .\n" % json['simulation_details']['job_directory'])
            file.write("cp %s/${prmtop} .\n\n" % json['simulation_details']['job_directory'])

            file.write("""pbsexec -grace 30 /home/igould/pmemd.cuda_SPFP -O -i 05_Prod.in \ 
    -o %s_${sim}ns.out -c ${prevrst} -p ${prmtop} \ 
    -r %s_${sim}ns.rst -x %s_${sim}ns.nc\n\n""" % (json['simulation_details']['system_name'],
                                                   json['simulation_details']['system_name'],
                                                   json['simulation_details']['system_name']))


            file.write("cp /tmp/pbs.${JOB_ID}/%s_${sim}ns.rst %s/\n" % (json['simulation_details']['system_name'],
                                                                      json['simulation_details']['job_directory']))
            file.write("rm /tmp/pbs.${JOB_ID}/${prevrst}\n")
            file.write("tar -zcvf %s/results/%s_${sim}ns.tgz *\n\n" % (json['simulation_details']['job_directory'],
                                                                       json['simulation_details']['system_name']))
            file.write("scp %s/results/%s_${sim}ns.tgz \ \n\t%s@%s:%s/" % (json['simulation_details']['job_directory'],
                                                                           json['simulation_details']['system_name'],
                                                                           json['local_machine']['user'],
                                                                           json['local_machine']['hostname'],
                                                                           json['local_machine']['destination']))


 # /home/igould/pmemd.cuda_SPFP -O -i premin.in -o premin_${count}_${cluster}.out -c $inpcrd -p $prmtop -r premin_${count}_${cluster}.rst  -ref $inpcrd

 # /home/igould/pmemd.cuda_SPFP -O -i sandermin1.in -o sandermin_${count}_${cluster}.out -c premin_${count}_${cluster}.rst -p $prmtop -r sandermin1_${count}_${cluster}.rst

 # /home/igould/pmemd.cuda_SPFP -O -i 02_Heat.in -o 02_Heat_${count}_${cluster}.out -c sandermin1_${count}_${cluster}.rst -p $prmtop -r 02_Heat_${count}_${cluster}.rst -x 02_Heat_$    {count}_${cluster}.nc -ref sandermin1_${count}_${cluster}.rst

 # /home/igould/pmemd.cuda_SPFP -O -i 03_Heat2.in -o 03_Heat2_${count}_${cluster}.out -c 02_Heat_${count}_${cluster}.rst -p $prmtop -r 03_Heat2_${count}_${cluster}.rst -x 03_Heat2_    ${count}_${cluster}.nc -ref 02_Heat_${count}_${cluster}.rst





def get_NumberOfJobs(json):
    total_lenght = json['simulation_details']['final_time'] - json['simulation_details']['start_time']
    job_length = json['simulation_details']['job_length']
    return(int(total_lenght/job_length) + 1)


def get_Times(number_of_jobs, job_length, start_time):
    """
    Returns a dictionary with the corresponding time window for each
    simulation
    """
    timeList = {}
    for job in range(1, number_of_jobs):
        if job == 1:
            time_at_start = start_time
            time_at_finish = time_at_start + job_length
        else:
            time_at_finish = start_time + (job * job_length)
            time_at_start = time_at_finish - job_length
        seq = (str(time_at_start).zfill(4), str(time_at_finish).zfill(4))
        timeList[job] = '-'.join(seq)
    return(timeList)


details = read_jsonfile(sys.argv[1])
dictionary = get_Times(get_NumberOfJobs(details), details['simulation_details']['job_length'], details['simulation_details']['start_time'])

print(dictionary)

for i in range(1, get_NumberOfJobs(details)):
    write_PBSheader(i, details)
    write_MDscript(i, details, dictionary)