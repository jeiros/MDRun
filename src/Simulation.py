from SchedulingEngine import PBSEngine

class Simulation:
    def __init__(self, json):
        """Parsear json a propiedades de clase"""
        self.scheduler = PBSEngine(json)

    def generateSimulationFiles(self):
        self._generate_PBS_headers()
        self._generate_pre_simulation_file()

    def _generate_scheduler_headers(self):
        print(self.pbs_headers)

    def _generate_pre_simulation_file(self):
        pass


