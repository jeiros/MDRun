def write_MDscript(job_number, json, timeList):
    job_str = str(job_number).zfill(2)
    with open("%s_job%s.pbs" % (json['simulation_details']['system_name'],
                                job_str), "a") as file:

        file.write("module load cuda/7.5.18\n")  # CUDA version
        file.write("module load intel-suite\n\n")
        file.write("prmtop=%s\n" % json['simulation_details']['topology_file'])
        file.write("sim=%s\n\n" % timeList[job_number])

        if job_number == 1:
            file.write("inpcrd=%s\n" % json['simulation_details']['inpcrd_file'])
            file.write("cd /tmp/pbs.${PBS_JOBID}\n")
            file.write("cp %s/*.in .\n" % json['simulation_details']['job_directory'])
            file.write("cp %s/${inpcrd} .\n" % json['simulation_details']['job_directory'])
            file.write("cp %s/${prmtop} .\n\n" % json['simulation_details']['job_directory'])
            file.write("/home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i premin.in -o premin.out -c ${inpcrd} -p ${prmtop} -r premin.rst -ref ${inpcrd}\n\n")
            file.write("/home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i sandermin1.in -o sandermin1.out -c premin.rst -p ${prmtop} -r sandermin1.rst\n\n")
            file.write("/home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i 02_Heat.in -o 02_Heat.out -c sandermin1.rst -p ${prmtop} -r 02_Heat.rst -ref sandermin1.rst -x 02_Heat.nc\n\n")
            file.write("/home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i 03_Heat2.in -o 03_Heat2.out -c 02_Heat.rst -p ${prmtop} -r 03_Heat2.rst -ref 02_Heat.rst -x 03_Heat2.nc\n\n")
            file.write("pbsexec -grace 15 /home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i 05_Prod.in -o %s_${sim}ns.out -c 03_Heat2.rst -p ${prmtop} -r %s_${sim}ns.rst -x 05_Prod_%s_${sim}ns.nc\n\n"
                       % (json['simulation_details']['system_name'],
                          json['simulation_details']['system_name'],
                          json['simulation_details']['system_name']))
            file.write("cp /tmp/pbs.${PBS_JOBID}/%s_${sim}ns.rst %s/\n"
                       % (json['simulation_details']['system_name'],
                          json['simulation_details']['job_directory']))
            file.write("rm /tmp/pbs.${PBS_JOBID}/${inpcrd}\n")

        else:
            file.write("prevrst=%s_%sns.rst\n" % (json['simulation_details']['system_name'],
                                                  timeList[job_number - 1]))
            file.write("prevsim=%s\n" % timeList[job_number - 1])
            file.write("cd /tmp/pbs.${PBS_JOBID}\n")
            file.write("cp %s/05_Prod.in .\n" % json['simulation_details']['job_directory'])
            file.write("cp %s/${prevrst} .\n" % json['simulation_details']['job_directory'])
            file.write("cp %s/${prmtop} .\n\n" % json['simulation_details']['job_directory'])
            file.write("pbsexec -grace 15 /home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i 05_Prod.in -o %s_${sim}ns.out -c ${prevrst} -p ${prmtop} -r %s_${sim}ns.rst -x 05_Prod_%s_${sim}ns.nc\n\n"
                       % (json['simulation_details']['system_name'],
                          json['simulation_details']['system_name'],
                          json['simulation_details']['system_name']))
            file.write("cp /tmp/pbs.${PBS_JOBID}/%s_${sim}ns.rst %s/\n"
                       % (json['simulation_details']['system_name'],
                          json['simulation_details']['job_directory']))
            file.write("rm /tmp/pbs.${PBS_JOBID}/${prevrst}\n")

        file.write("tar -zcvf %s/results/%s_${sim}ns.tgz *\n\n"
                   % (json['simulation_details']['job_directory'],
                      json['simulation_details']['system_name']))
        file.write("rsync -avz --remove-source-files %s/results/%s_${sim}ns.tgz %s@%s:%s/\n"
                   % (json['simulation_details']['job_directory'],
                      json['simulation_details']['system_name'],
                      json['local_machine']['user'],
                      json['local_machine']['hostname'],
                      json['local_machine']['destination']))