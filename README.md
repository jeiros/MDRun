# JobSumitter
Python tool to generate the appropriate files for long classic MD runs in the Imperial College HPC facility.

# Basic workflow
Tune settings in the JSON file. Example file is `input_example.json`.
Generate the PBS scripts with:

```
generate_scripts.py input_example.json
```
This will generate a series of `.pbs` files that have to be copied to the HPC along with the `launcher.sh` script, with the appropriate
files to run the MD job (topology, any restart/inpcrd files, as well as the input files with the MD settings.)

Once you're in the appropriate HPC directory, submit the jobs with `launcher.sh`.

## JSON inputs

### Scheduler
At the moment only the `pbs` job scheduler is implemented.

### PBS settings
*walltime* Specify the walltime to be used in format `hh:m:s`.

*nnodes* Nodes to be used.

*ncpus* Number of cores to be used.

*ngpus* Number of GPU cards to be used.

*mem* Specify the memory (in MB) for the job in the format `XXXXmb`.

*host* Host were the job is going to run.

*queue* Queue were the job is going to run. Only two options are supported: `qpgpu` for public chemistry department queue,
and `pqigould` for the private queue.

*gpu_type* The type of GPU to be used. 

*email* You're email, so you can get notified when a job aborts, begins or ends successfully.

### Simulation details
*system_name* The name of your system. This is used throughout the code to give the files matching names.

*inpcrd_file* The input coordinates file. This is used if you want to start your simulation from 0. Should end with `.inpcrd`.

*topology_file* The topology file of your system. Should end with `.prmtop`

*start_time* The time from which you want to launch the simulation (in nanoseconds).

*final_time* The time at which you want your simulation to stop (in nanoseconds).

*job_length* The lenght of each individual MD run. You should set accordingly the amount of MD iterations and timestep to
be used in your MD input file. Also, be careful not to hit the wallclock time.

*job_directory* The directory in which the job is going to be run in the HPC. You should launch the `launcher.sh` script 
from here once all the necessary files are in it. :exclamation: This directory **must** contain a `results` directory in it,
if it doesn't your job will fail at the end!:exclamation:

*start_rst* The restart file that the first job is going to use. If you start from 0 and want to run pre-production commands
in the GPU (discouraged), this should match the name of the restart file that is written after your last pre-production run 
(usually a heating protocol).

*cuda_version* The cuda version to use via `module load cuda`.

*binary_location* The full path to the `pmemd.cuda_SPFP` binary (or whatever it's called).

*pre_simulation_type* Where to run the pre-production commands. Two options are supported:

    * `cpu`: Whatever commands you want to run before the production run are read from the *pre_simulation_cmd*
        section in the JSON file and are written to a bash script called `pre_simulation.sh` which you can then
        run in your machine.
    * `gpu`: If you want to run the *pre_simulation_cmd* commands in the HPC. Then they will be used in the first
        `.pbs` file. This is not recommended as for some systems GPUs are known to give trouble with minimisations.

*pre_simulation_cmd* An indefinite list of commands that you want to run before the production run. These can be run on the
HPC or locally. Nothing is assumed here, they'll be run as is (so if you want them to run in the HPC the binary location
should match the one in the HPC, for instance.)

### Local Machine
*user* Your username in your local machine
*hostname* The hostname of your machine
*destination* The **full** path in which the results of the simulations are going to be moved to. This directory should
exist before the data copy is attempted, or else it will fail.

