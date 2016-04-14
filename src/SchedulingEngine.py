class SchedulingEngine:
    def __init__(self, simulation):
        self.pbs_headers = ""
        self.simulation = simulation


class PBSEngine(SchedulingEngine):
    def generate_headers(self):
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
        self.pbs_headers += "#PBS -q %s\n" % self.simulation.queue
        self.pbs_headers += "#PBS -M %s\n" % self.simulation.email
        self.pbs_headers += "#PBS -m abe\n\n"

        return(self.pbs_headers)

    def get_work_directory_cmd(self):
        return "cd /tmp/pbs.${PBS_JOBID}\n"

    def get_afterProd_cmds(self):
        self.afterProd_cmd = ""
        self.afterProd_cmd += "cp /tmp/pbs.${PBS_JOBID}/%s_${sim}ns.rst %s/\n" % (self.simulation.system_name, self.simulation.job_directory)
        if self.simulation.start_time == 0:
            self.afterProd_cmd += "rm /tmp/pbs.${PBS_JOBID}/${inpcrd}\n"
        else:
            self.afterProd_cmd += "rm /tmp/pbs.${PBS_JOBID}/${prevrst}\n"
        return(self.afterProd_cmd)


class OpenLavaEngine(SchedulingEngine):
    def generate_headers(self):
        pass

    def get_work_directory_cmd(self):
        pass

    def get_afterProd_cmds(self):
        pass
