
class Simulation:
    def __init__(self, json):
        """Parsear json a propiedades de clase"""
        self.pbs_headers = ""

        # PBS settings
        self.queue_type = json['pbs_settings']['queue']
        self.walltime = json['pbs_settings']['walltime']
        self.mail = json['pbs_settings']['email']

    def generateSimulationFiles(self):
        self._generate_PBS_headers()
        self._generate_pre_simulation_file()

    def _generate_pqigould_headers(self):
        pass

    def _generate_gpgpu_headers(self):
        pass

    def _generate_PBS_headers(self):
        if self.queue_type == 'gpgpu':
            self._generate_gpgpu_headers()
        elif self.queue_type == 'pqigould':
            self._generate_pqigould_headers()
        else:
            sys.exit("Supported queues are 'pgigould' or 'gpgpu' only.")

        self.pbs_headers += "#PBS -lwalltime=%s\n" % self.walltime
        self.pbs_headers += "#PBS -q %s\n" % self.queue_type
        self.pbs_headers += "#PBS -M %s\n" % self.mail
        self.pbs_headers += "#PBS -m abe\n\n"

        print(self.pbs_headers)

    def _generate_pre_simulation_file(self):
        pass


