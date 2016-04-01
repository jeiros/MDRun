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
At the moment only the `input_example.json` job scheduler is implemented. 

### PBS settings
*walltime* Specify the walltime to be used in format hh:m:s.

*nnodes* Nodes to be used.

*ncpus* Number of cores to be used.

*ngpus* Number of GPU cards to be used.

*mem* Specify the memory (in MB) for the job in the format XXXXmb.

*host* Host were the job is going to run.

*queue* Queue were the job is going to run. Only two options are supported: `qpgpu` for public chemistry department queue,
and `pqigould` for the private queue.

*gpu_type* The type of GPU to be used. 
