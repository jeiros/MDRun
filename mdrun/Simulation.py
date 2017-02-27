from .SchedulingEngine import PBSEngine
import sys


class Simulation(object):

    """docstring for Simulation"""

    def __init__(self, json):
        """Parse the information inside the JSON file into
        class atributes."""
        if json['scheduler'] == 'pbs':
            self.scheduler = PBSEngine(self)

        # Is it an HPC job or local machine job
        self.is_HPCjob = (json['HPC_job'] == "True")
        # PBS settings
        self.queue = json['pbs_settings']['queue']
        self.walltime = json['pbs_settings']['walltime']
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
        self.start_rst = json['simulation_details']['start_rst']
        self.input_file = json['simulation_details']['input_file']
        self.start_time = json['simulation_details']['start_time']
        self.final_time = json['simulation_details']['final_time']
        self.job_length = json['simulation_details']['job_length']
        self.job_directory = json['simulation_details']['job_directory']
        self.cuda_version = json['simulation_details']['cuda_version']
        self.binary_location = json['simulation_details']['binary_location']
        self.pre_simulation_cmd = json[
            'simulation_details']['pre_simulation_cmd']
        self.pre_simulation_type = json[
            'simulation_details']['pre_simulation_type']

        # Workstation details
        self.user = json['local_machine']['user']
        self.hostname = json['local_machine']['hostname']
        self.destination = json['local_machine']['destination']

        # Master node details for local TORQUE queue
        self.user_m = json['master_node']['user_m']
        self.hostname_m = json['master_node']['hostname_m']
        self.job_directory_m = json['master_node']['job_directory_m']

    def writeSimulationFiles(self):
        needs_pre_simulation_file = (self.pre_simulation_type == "cpu")

        self.sch_headers = self.scheduler.generate_headers()
        # If we do the pre-simulation commands specified in the JSON file
        # then we write them to a file called pre_simulation.sh to run it
        # on a local machine
        if needs_pre_simulation_file:
            self._write_pre_simulation_CPUfile()

        self.times = self._get_Times()

        for sim_number, time_interval in self.times.items():
            self.sim_number = sim_number
            if ((sim_number == 1) and (self.start_time == 0) and
                    (not needs_pre_simulation_file)):
                print(
                    "The presimulation commands are going to be run on a GPU.\n")
                # Only if the user wants to run the pre-simulation commands
                # in a qsub script.
                self._write_first_step_file(time_interval)
            else:
                self._write_step_file(sim_number, time_interval)

    def _write_step_file(self, sim_number, time_interval):
        rendered_commands = self.sch_headers
        rendered_commands += self._generate_preliminary_cmds(time_interval)

        if (sim_number == 1):
            rendered_commands += "prevrst=%s\n" % self.start_rst
        else:
            rendered_commands += "prevrst=%s_%sns.rst\n" % (self.system_name,
                                                            self.times[sim_number - 1])

        rendered_commands += self.scheduler.get_work_directory_cmd()
        rendered_commands += "cp %s/%s .\n" % (
            self.job_directory, self.input_file)
        rendered_commands += "cp %s/${prmtop} .\n" % self.job_directory
        rendered_commands += "cp %s/${prevrst} .\n\n" % self.job_directory
        if self.is_HPCjob:
            rendered_commands += "pbsexec -grace 15 "
        rendered_commands += """%s -O -i %s \\
    -o %s_${sim}ns.out -c ${prevrst} -p ${prmtop} -r %s_${sim}ns.rst \\
    -x 05_Prod_%s_${sim}ns.nc\n\n""" % (self.binary_location,
                                        self.input_file,
                                        self.system_name,
                                        self.system_name,
                                        self.system_name)
        rendered_commands += self._generate_final_cmds()

        file = open("%s_job%s.pbs" % (self.system_name,
                                      str(sim_number).zfill(2)), "w")
        file.write(rendered_commands)
        file.close()

    def _write_first_step_file(self, time_interval):
        simulation_cmds_rendered = self.sch_headers
        simulation_cmds_rendered += self._generate_preliminary_cmds(
            time_interval)
        simulation_cmds_rendered += "inpcrd=%s\n" % self.inpcrd_file
        simulation_cmds_rendered += self.scheduler.get_work_directory_cmd()
        simulation_cmds_rendered += "cp %s/*.in .\n" % self.job_directory
        simulation_cmds_rendered += "cp %s/*.rst .\n" % self.job_directory
        simulation_cmds_rendered += "cp %s/${prmtop} .\n" % self.job_directory
        simulation_cmds_rendered += "cp %s/${inpcrd} .\n\n" % self.job_directory

        for cmd in self.pre_simulation_cmd:
            simulation_cmds_rendered += cmd + "\n"

        if self.is_HPCjob:
            simulation_cmds_rendered += "pbsexec -grace 15 "
        simulation_cmds_rendered += """%s -O -i %s \\
    -o %s_${sim}ns.out -c %s -p ${prmtop} -r %s_${sim}ns.rst \\
    -x 05_Prod_%s_${sim}ns.nc\n\n""" % (self.binary_location,
                                        self.input_file,
                                        self.system_name,
                                        self.start_rst,
                                        self.system_name,
                                        self.system_name)
        simulation_cmds_rendered += self._generate_final_cmds()

        file = open("%s_job%s.pbs" % (self.system_name,
                                      str(1).zfill(2)), "w")
        file.write(simulation_cmds_rendered)
        file.close()

    def _write_pre_simulation_CPUfile(self):
        """Write a bash script to do the pre simulation commands as specified
        in the JSON file. Also specify what the prmtop and inprcrd files are
        from the JSON.
        """
        pre_simulation_cmds_rendered = ""

        pre_simulation_cmds_rendered += "prmtop=%s\n" % self.topology_file
        pre_simulation_cmds_rendered += "inpcrd=%s\n\n" % self.inpcrd_file

        for cmd in self.pre_simulation_cmd:
            pre_simulation_cmds_rendered += cmd + "\n"

        file = open("pre_simulation.sh", "w")
        file.write(pre_simulation_cmds_rendered)
        file.close()

    def _generate_preliminary_cmds(self, time_interval):
        """Return the usual commands that every run uses."""
        prelim_cmds = ""
        if self.is_HPCjob:
            prelim_cmds += "module load cuda/%s\n" % self.cuda_version
            prelim_cmds += "module load intel-suite\n\n"
        prelim_cmds += "prmtop=%s\n" % self.topology_file
        prelim_cmds += "sim=%s\n\n" % time_interval
        return(prelim_cmds)

    def _generate_final_cmds(self):
        """Write the commands after the production run. The first copy and remove
        commands are scheduler-specific and are implemented in the corresponding
        engine class."""
        final_cmds = self.scheduler.get_afterProd_cmds()
        final_cmds += "tar -zcvf %s/%s_${sim}ns.tgz *\n" % (self.job_directory,
                                                            self.system_name)
        final_cmds += """rsync -avz --remove-source-files \\
    %s/%s_${sim}ns.tgz \\
    %s@%s:%s/\n""" % (self.job_directory,
                      self.system_name,
                      self.user,
                      self.hostname,
                      self.destination)
        if not self.is_HPCjob:
            final_cmds += "rm -rf /tmp/pbs.${PBS_JOBID}/\n"
        return(final_cmds)

    def _get_NumberOfJobs(self):
        """Counts how many jobs are going to be needed."""
        if self.start_time < 0:
            raise ValueError("Start time must be 0 or positive.")
        total_time = self.final_time - self.start_time
        if total_time < 0:
            raise ValueError("Total time is negative. Check your inputs!")
        if (total_time % self.job_length) != 0:
            raise ValueError(
                "Job length must be a divisor of total simulation time.")
        else:
            return(int(total_time / self.job_length) + 1)

    def _get_Times(self):
        """Returns a dictionary with the number of each simulation (starting at 1)
        and its corresponding time frame."""
        timeList = {}
        for job in range(1, self._get_NumberOfJobs()):
            if job == 1:
                time_at_start = self.start_time
                time_at_finish = time_at_start + self.job_length
            else:
                time_at_finish = self.start_time + (job * self.job_length)
                time_at_start = time_at_finish - self.job_length
            seq = (str(time_at_start).zfill(4), str(time_at_finish).zfill(4))
            timeList[job] = '-'.join(seq)
        return(timeList)
