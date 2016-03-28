class Simulation:
    def __init__(self, json):
        """Parsear json a propiedades de clase"""
        self.pbs_headers = ""

        # PBS settings
        self.queue_type = json['pbs_settings']['queue']
        self.walltime = json['pbs_settings']['walltime']
        self.mail = json['pbs_settings']['email']
        self.nnodes = json['pbs_settings']['nnodes']
        self.ncpus = json['pbs_settings']['ncpus']
        self.ngpus = json['pbs_settings']['ngpus']
        self.memory = json['pbs_settings']['mem']
        self.gpu_type = json['pbs_settings']['gpu_type']
        self.host = json['pbs_settings']['host']

    def generateSimulationFiles(self):
        self._generate_PBS_headers()
        self._generate_pre_simulation_file()

    def _generate_PBS_headers(self):
        self.pbs_headers = "#PBS -lselect=%s:" % self.nnodes
        self.pbs_headers += "ncpus=%s:" % self.ncpus
        self.pbs_headers += "ngpus=%s:" % self.ngpus
        self.pbs_headers += "mem=%s:" % self.memory

        if self.queue_type == 'gpgpu':
            self.pbs_headers += "gpu_type=%s\n" % self.gpu_type
        elif self.queue_type == 'pqigould':
            self.pbs_headers += "host=%s\n" % self.host
        else:
            sys.exit("Supported queues are 'pgigould' or 'gpgpu' only.")

        self.pbs_headers += "#PBS -lwalltime=%s\n" % self.walltime
        self.pbs_headers += "#PBS -q %s\n" % self.queue_type
        self.pbs_headers += "#PBS -M %s\n" % self.mail
        self.pbs_headers += "#PBS -m abe\n\n"

        print(self.pbs_headers)

    def _generate_pre_simulation_file(self):
        pass


