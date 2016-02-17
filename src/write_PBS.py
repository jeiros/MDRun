def write_PBSheader(job_number, json):
    """
    Writes the header with the PBS information
    """
    job_str = str(job_number).zfill(2)
    file = open("%s_job%s.sh" % (json['simulation_details']['system_name'],
                                 job_str), "w")
    file.write("#PBS -N %s_job%s\n" % (json['simulation_details']['system_name'],
                                       job_str))
    file.write("#PBS -l select=%s\n" % json['pbs_settings']['nnodes'])
    file.write("#PBS -l ncpus=%s:ngpus=%s\n" % (json['pbs_settings']['ncpus'],
                                                json['pbs_settings']['ngpus']))
    file.write("#PBS -l walltime=%s\n" % json['pbs_settings']['walltime'])
    file.write("#PBS -l host=%s\n" % json['pbs_settings']['host'])
    file.write("#PBS -q %s\n" % json['pbs_settings']['queue'])
    file.write("#PBS -M %s\n" % json['pbs_settings']['email'])
    file.write("#PBS -m abe\n\n")
    file.close()