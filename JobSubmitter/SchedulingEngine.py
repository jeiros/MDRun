class SchedulingEngine:
    def __init__(self, simulation):
        self.pbs_headers = ""
        self.simulation = simulation


class PBSEngine(SchedulingEngine):
    def generate_headers(self):
        if self.simulation.is_HPCjob:
            self.pbs_headers = "#PBS -lselect=%s:" % self.simulation.nnodes
            self.pbs_headers += "ncpus=%s:" % self.simulation.ncpus
            self.pbs_headers += "ngpus=%s:" % self.simulation.ngpus
            self.pbs_headers += "mem=%s:" % self.simulation.memory

            if self.simulation.queue == 'gpgpu':
                self.pbs_headers += "gpu_type=%s\n" % self.simulation.gpu_type
            elif self.simulation.queue == 'pqigould':
                self.pbs_headers += "host=%s\n" % self.simulation.host
            else:
                print("""Queue wasn't gpgpu or pqigould. Assume nothing and print
                      in the PBS header both the gpu_type and the host.\n""")
                self.pbs_headers += "gpu_type=%s\n" % self.simulation.gpu_type
                self.pbs_headers += "host=%s\n" % self.simulation.host

            self.pbs_headers += "#PBS -lwalltime=%s\n" % self.simulation.walltime
            self.pbs_headers += "#PBS -q %s\n\n" % self.simulation.queue
        else:
            self.pbs_headers = "#PBS -l nodes=%s" % self.simulation.host
            self.pbs_headers += ":gpus=%s:ppn=%s\n" % (self.simulation.ngpus,
                                                       self.simulation.ncpus)
            self.pbs_headers += "#PBS -l mem=%s\n" % self.simulation.memory
            self.pbs_headers += "#PBS -l walltime=%s\n" % self.simulation.walltime
            self.pbs_headers += "#PBS -q %s\n" % self.simulation.queue
            self.pbs_headers += "#PBS -j oe\n\n"

        return(self.pbs_headers)

    def get_work_directory_cmd(self):
        # If working on a local machine, we first have to copy the files from
        # the master node to the compute node, as well as creating the /tmp
        # directory where the job will run
        if self.simulation.is_HPCjob:
            return("cd /tmp/pbs.${PBS_JOBID}\n")
        else:
            work_dir_cmd = ""
            work_dir_cmd += "mkdir -p %s && " % self.simulation.job_directory
            work_dir_cmd += "cd %s\n" % self.simulation.job_directory
            work_dir_cmd += "scp %s@%s:%s/* .\n" % (self.simulation.user_m,
                                                    self.simulation.hostname_m,
                                                    self.simulation.job_directory_m)
            work_dir_cmd += "mkdir -p /tmp/pbs.${PBS_JOBID} && "
            work_dir_cmd += "cd /tmp/pbs.${PBS_JOBID}\n"
            return(work_dir_cmd)

    def get_afterProd_cmds(self):
        self.afterProd_cmd = ""
        self.afterProd_cmd += "cp /tmp/pbs.${PBS_JOBID}/%s_${sim}ns.rst %s/\n" % (self.simulation.system_name, self.simulation.job_directory)
        if (self.simulation.sim_number == 1) and (self.simulation.start_time == 0):
            self.afterProd_cmd += "rm /tmp/pbs.${PBS_JOBID}/${inpcrd}\n"
        else:
            self.afterProd_cmd += "rm /tmp/pbs.${PBS_JOBID}/${prevrst}\n"
        return(self.afterProd_cmd)
