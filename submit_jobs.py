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
    file = open("run%s.sh" % job_number, "w")
    file.write("#PBS -N job%s\n" % job_number)
    file.write("#PBS -lselect=%s\n" % json['pbs_settings']['nnodes'])
    file.write("#PBS -l ncpus=%s:ngpus=%s\n" % (json['pbs_settings']['ncpus'],
                                                json['pbs_settings']['ngpus']))
    file.write("#PBS -l walltime=%s\n" % json['pbs_settings']['walltime'])
    file.write("#PBS -l host=%s\n" % json['pbs_settings']['host'])
    file.write("#PBS -q %s\n" % json['pbs_settings']['queue'])
    file.write("#PBS -M %s\n" % json['pbs_settings']['email'])
    file.write("#PBS -m abe\n")
    file.close()


def write_MDscript(job_number, json, timeList):
    with open("run%s.sh" % job_number, "a") as file:
        if job_number == 1:
            pass
        else:
            file.write("module load cuda/6.5.19\n")
            file.write("prevrst=%s_%sns.rst\n" % (json['simulation_details']['system_name'],
                                                timeList[job_number - 1]))
            file.write("prmtop=%s\n" % json['simulation_details']['topology_file'])
            file.write("cd /tmp/pbs.$PBS_JOBID\n")
            file.write("cp %s/*.in .\n" % json['simulation_details']['job_directory']) # This copies all the input scripts
            file.write("cp %s/${prevrst} .\n" % json['simulation_details']['job_directory'])
            file.write("cp %s/${prmtop} .\n" % json['simulation_details']['job_directory'])
            file.write("""pbsexec -grace 15 /home/igould/pmemd.cuda_SPFP -O -i 05_Prod.in \ 
    -o %s_%sns.out -c ${prevrst} -p ${prmtop} \ 
    -r %s_%sns.rst -x %s_%sns.nc""" % (json['simulation_details']['system_name'],
                                       timeList[job_number],
                                       json['simulation_details']['system_name'],
                                       timeList[job_number],
                                       json['simulation_details']['system_name'],
                                       timeList[job_number]))




def get_NumberOfJobs(json):
    total_lenght = json['simulation_details']['final_time'] - json['simulation_details']['start_time']
    job_length = json['simulation_details']['job_length']
    return(int(total_lenght/job_length) + 1)


def get_Times(number_of_jobs, job_length):
    """
    Returns a dictionary with the corresponding time window for each
    simulation
    """
    timeList = {}
    for job in range(1, number_of_jobs):
        if job == 1:
            time_at_finish = job_length
            time_at_start = 0
        else:
            time_at_finish = job * job_length
            time_at_start = time_at_finish - job_length
        seq = (str(time_at_start).zfill(4), str(time_at_finish).zfill(4))
        timeList[job] = '-'.join(seq)
    return(timeList)


details = read_jsonfile(sys.argv[1])
dictionary = get_Times(get_NumberOfJobs(details), details['simulation_details']['job_length'])

for i in range(1, get_NumberOfJobs(details)):
    write_PBSheader(i, details)
    write_MDscript(i, details, dictionary)



#PBS -lselect=1:ncpus=1:ngpus=1:mem=2000mb:host=cx1-51-3-1
#PBS -lwalltime=192:00:0
#PBS -q pqigould