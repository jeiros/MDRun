# -*- coding: utf-8 -*-

from __future__ import print_function
import click
import json
import os
import shutil
from mdrun.Simulation import Simulation


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
    click.echo('Printing example.json file')
    script_dir = os.path.dirname(__file__)  # Absolute path the script is in
    relative_path = 'data/input_example.json'
    shutil.copyfile(
        os.path.join(script_dir, relative_path), './input_example.json')


def read_jsonfile(file):
    """
    Parse the input JSON file and return a dictionary with the info
    """
    with open(file) as data:
        json_data = json.load(data)
    return(json_data)
