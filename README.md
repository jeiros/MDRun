# JobSumitter
Python tool to submit several PBS jobs on the HPC

# Basic usage
Adapt settings in the JSON file. Example file is `input_example.json`.
Generate the PBS scripts with:

```
generate_scripts.py input_example.json
```
This will generate a series of `.pbs` files that have to be copied to the HPC along with the `launcher.sh` script.

Once you're in the appropriate HPC directory, submit the jobs with `launcher.sh`.

