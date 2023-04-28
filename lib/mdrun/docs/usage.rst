=====
Usage
=====

Basic workflow
--------------

Select your settings in the JSON file. There is an example file ``input_example.json``.
You can also generate an input example file with ``mdrun skeleton``.

The code uses Python 3. Test your Python version in your machine with ``python --version``.

Then, use the program with::

    mdrun generate_scripts input_example.json

This will generate a series of ``.pbs`` files that have to be copied to the HPC along with the ``launch_PBS_jobs`` script and the appropriate
files to run the MD job (topology, any restart/inpcrd files, as well as the input files with the MD settings.)

Once you're in the appropriate HPC directory (the one you've specified in the ``job_directory`` variable),
submit the jobs with ``launch_PBS_jobs``.

JSON inputs
-----------

Scheduler
#########

At the moment only the PBS job scheduler is implemented.

HPC_job
#######

Set this to ``true`` if the job is going to be run in the HPC at Imperial. Set to ``false`` of leave empty
if you want to run on a local machine that has torque installed.

PBS settings
############

These settings are used to build the `PBS directives <https://www.osc.edu/supercomputing/batch-processing-at-osc/pbs-directives-summary>`_ as headers.

* ``walltime`` Specify the walltime to be used in format ``hh:m:s``.

* ``nnodes`` Nodes to be used.

* ``ncpus`` Number of cores to be used.

* ``ngpus`` Number of GPU cards to be used.

* ``mem`` Specify the memory (in MB) for the job in the format ``XXXXmb``.

* ``host`` Host were the job is going to run.

* ``queue`` Queue were the job is going to run. Only two options are supported for the HPC:

  * ``qpgpu`` for public chemistry department queue
  * ``pqigould`` for the private queue.

To run on the local machines, there is the 'long' queue with a walltime of 192 hours enabled.

* ``gpu_type`` The type of GPU to be used. 

Simulation details
##################

* ``system_name`` The name of your system. This is used throughout the code to give the files matching names.

* ``inpcrd_file`` The input coordinates file. This is used if you want to start your simulation from 0. Should end with ``.inpcrd``.

* ``topology_file`` The topology file of your system. Should end with ``.prmtop``

* ``start_rst`` The restart file that the first job is going to use. If you start from 0 and want to run pre-production commands in the GPU (discouraged), this should match the name of the restart file that is written after your last pre-production run (usually a heating protocol). If you don't start from 0, this file will be read to start the first job.

* ``input_file`` The input file with the MD settings for the production run. You should be specially careful that the timestep (``dt``) and number of MD steps to be performed (``nstlim``) match the ``job_lenght`` that you want, as the program does not do this for you nor checks if it is correct.

* ``start_time`` The time from which you want to launch the simulation (in nanoseconds). Doesn't necessarily have to be 0 (you can start from an existing simulation, using the appropriate ``.rst`` file, as specified in the ``start_rst`` variable.)

* ``final_time`` The time at which you want your simulation to stop (in nanoseconds).

* ``job_length`` The lenght of each individual MD run (in nanoseconds). You should set accordingly the amount of MD iterations and timestep to be used in your MD input file. Also, be careful not to hit the wallclock time.

* ``job_directory`` The directory in which the job is going to be run in the HPC. You should launch the ``launch_PBS_jobs`` script  from here once all the necessary files are in it. This is the directory were all the ``.pbs`` & the rest of the input files should be. Also, this is where you issue the ``launch_PBS_jobs`` command.

* ``cuda_version`` The cuda version to use via ``module load cuda``. This is expected to not changed very frequently.

* ``binary_location`` The full path to the ``pmemd.cuda_SPFP`` binary (or whatever it's called). This is expected to not changed very frequently.

* ``pre_simulation_cmd`` An indefinite list of commands that you want to run before the production run. These can be run on the HPC or locally. Nothing is assumed here, they'll be run as is (so if you want them to run in the HPC the binary location should match the one in the HPC, for instance).

* ``pre_simulation_type`` Where to run the pre-production commands. Two options are supported:

  * ``cpu``: Whatever commands you want to run before the production run are read from the ``pre_simulation_cmd`` section in the JSON file and are written to a bash script called ``pre_simulation.sh`` which you can then run in your machine.
  * ``gpu``: If you want to run the *pre_simulation_cmd* commands in the HPC. Then they will be used in the first ``.pbs`` file. This is not recommended as for some systems GPUs are known to give trouble with minimisations.

Local Machine
#############

* ``user`` Your username in your local machine. Find it with the ``whoami`` command.

* ``hostname`` The hostname of your machine. Find it with the ``hostname`` command.

* ``destination`` The *full path* in which the results of the simulations are going to be moved to. This directory should exist before the data copy is attempted, or else it will fail.

Master Node
###########

This is just used if the jobs are run on the local machines.

* ``user_m`` Your username on the master node.

* ``hostname_m`` The hostname of the master node. Shouldn't change.

* ``job_directory_m`` The job where you'll launch the ``.pbs`` scripts from.

