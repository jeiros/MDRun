from src.SchedulingEngine import PBSEngine
from src.SchedulingEngine import OpenLavaEngine

class Simulation:
    def __init__(self, json):
        """Parsear json a propiedades de clase"""
        if json['scheduler'] == 'pbs':
            self.scheduler = PBSEngine(self)
        elif json['scheduler'] == 'openlava':
            self.scheduler = OpenLavaEngine(self)

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

        # Simulation details
        self.system_name = json['simulation_details']['system_name']
        self.inpcrd_file = json['simulation_details']['inpcrd_file']
        self.topology_file = json['simulation_details']['topology_file']
        self.start_time = json['simulation_details']['start_time']
        self.final_time = json['simulation_details']['final_time']
        self.job_length = json['simulation_details']['job_length']
        self.job_directory = json['simulation_details']['job_directory']
        self.start_rst = json['simulation_details']['start_rst']
        self.pre_simulation_cmd = json['simulation_details']['pre_simulation_cmd']

        # Local machine details
        self.user = json['local_machine']['user']
        self.hostname = json['local_machine']['hostname']
        self.destination = json['local_machine']['destination']

    def generateSimulationFiles(self):
        self.sch_headers = self.scheduler.generate_headers()
        self.work_directory_cmd = self.scheduler.get_work_directory_cmd()

        self._generate_pre_simulation_file()

    def _generate_pre_simulation_file(self):
        self.pre_simulation_cmds_rendered = ""

        self.pre_simulation_cmds_rendered += "prmtop=%s\n" % self.topology_file
        self.pre_simulation_cmds_rendered += "inpcrd=%s\n\n" % self.inpcrd_file

        self.pre_simulation_cmds_rendered += self.work_directory_cmd
        self.pre_simulation_cmds_rendered += "cp %s/*.in .\n" % self.job_directory
        self.pre_simulation_cmds_rendered += "cp %s/${inpcrd} .\n" % self.job_directory
        self.pre_simulation_cmds_rendered += "cp %s/${prmtop} .\n\n" % self.job_directory

        for cmd in self.pre_simulation_cmd:
            self.pre_simulation_cmds_rendered += cmd + "\n"

        file = open("pre_simulation.sh", "w")
        file.write(self.pre_simulation_cmds_rendered)
        file.close()

    def _generate_move_files_cmd(self):
        pass
