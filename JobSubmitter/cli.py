# -*- coding: utf-8 -*-

from __future__ import print_function
import click
import json
from JobSubmitter.Simulation import Simulation


@click.group()
def main():
    """Console script for JobSubmitter"""
    pass


@main.command()
@click.argument('json_file', type=click.Path(exists=True))
def generate_scripts(json_file):
    """Read the JSON_FILE and write the PBS files"""
    json_file = click.format_filename(json_file)
    settings = read_jsonfile(json_file)
    simulation = Simulation(settings)
    simulation.writeSimulationFiles()


@main.command()
def skeleton():
    """Get an example example.json input file."""
    example_file = {'HPC_job': 'True',
                    'local_machine': {'destination': '/Users/username/protein1',
                                      'hostname': 'hostname',
                                      'user': 'username'},
                    'master_node': {'hostname_m': 'master_node-hostname',
                                    'job_directory_m': '/home/username/protein1',
                                    'user_m': 'username'},
                    'pbs_settings': {'gpu_type': 'K80',
                                     'host': 'cx1-51-6-1',
                                     'mem': '1000mb',
                                     'ncpus': 1,
                                     'ngpus': 1,
                                     'nnodes': 1,
                                     'queue': 'gpgpu',
                                     'walltime': '72:0:0'},
                    'scheduler': 'pbs',
                    'simulation_details': {'binary_location': '/path/to/AMBERHOME/bin/pmemd.cuda_SPFP',
                                           'cuda_version': '7.5.18',
                                           'final_time': 500,
                                           'inpcrd_file': 'protein1.inpcrd',
                                           'input_file': 'Production_cmds.in',
                                           'job_directory': '/work/username/protein1',
                                           'job_length': 50,
                                           'pre_simulation_cmd': ['/path/to/AMBERHOME/bin/pmemd.cuda_SPFP -O -i premin.in -o premin.out -c ${inpcrd} -p ${prmtop} -r premin.rst -ref ${inpcrd}',
                                                                  '/path/to/AMBERHOME/bin/pmemd.cuda_SPFP -O -i sandermin1.in -o sandermin1.out -c premin.rst -p ${prmtop} -r sandermin1.rst',
                                                                  '/path/to/AMBERHOME/bin/pmemd.cuda_SPFP -O -i 02_Heat.in -o 02_Heat.out -c sandermin1.rst -p ${prmtop} -r 02_Heat.rst -ref sandermin1.rst -x 02_Heat.nc',
                                                                  '/path/to/AMBERHOME/bin/pmemd.cuda_SPFP -O -i 03_Heat2.in -o 03_Heat2.out -c 02_Heat.rst -p ${prmtop} -r Heated_eq.rst -ref 02_Heat.rst -x 03_Heat2.nc'],
                                           'pre_simulation_type': 'gpu',
                                           'start_rst': 'Heated_eq.rst',
                                           'start_time': 0,
                                           'system_name': 'protein1',
                                           'topology_file': 'protein1.prmtop'}}

    with open('example.json', 'w') as f:
        json.dump(example_file, f)


def read_jsonfile(file):
    """
    Parse the input JSON file and return a dictionary with the info
    """
    with open(file) as data:
        json_data = json.load(data)
    return(json_data)
