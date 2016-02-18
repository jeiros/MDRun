def write_PBSheader(job_number, json):
    import sys
    """
    Writes the header with the PBS information
    """
    job_str = str(job_number).zfill(2)
    file = open("%s_job%s.pbs" % (json['simulation_details']['system_name'],
                                  job_str), "w")

    if json['pbs_settings']['queue'] == 'gpgpu':
        file.write("#PBS -lselect=%s:ncpus=%s:ngpus=%s:mem=%s:gpu_type=%s\n"
                   % (json['pbs_settings']['nnodes'],
                      json['pbs_settings']['ncpus'],
                      json['pbs_settings']['ngpus'],
                      json['pbs_settings']['mem'],
                      json['pbs_settings']['gpu_type']))
    elif json['pbs_settings']['queue'] == 'pqigould':
        file.write("#PBS -lselect=%s:ncpus=%s:ngpus=%s:mem=%s:host=%s\n"
                   % (json['pbs_settings']['nnodes'],
                      json['pbs_settings']['ncpus'],
                      json['pbs_settings']['ngpus'],
                      json['pbs_settings']['mem'],
                      json['pbs_settings']['host']))
    else:
        sys.exit("Supported queues are 'pgigould' or 'gpgpu' only.")

    file.write("#PBS -lwalltime=%s\n" % json['pbs_settings']['walltime'])
    file.write("#PBS -q %s\n" % json['pbs_settings']['queue'])
    file.write("#PBS -M %s\n" % json['pbs_settings']['email'])
    file.write("#PBS -m abe\n\n")
    file.close()
