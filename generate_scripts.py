#!/usr/bin/env python3
import json
import sys
from src.Simulation import Simulation
import argparse

parser = argparse.ArgumentParser(usage="{} input_file.json".format(sys.argv[0]),
                                 epilog="""Generates the necessary input scripts
                                           for PBS submission in the HPC of a long
                                           MD run.\n""")
parser.add_argument("InputFile", help="A JSON file with the different options")

args = parser.parse_args()


def read_jsonfile(file):
    """
    Parse the input JSON file and return a dictionary with the info
    """
    with open(file) as data:
        json_data = json.load(data)
    return(json_data)


def main():
    if args:
        input_file = read_jsonfile(args.InputFile)
        simulation = Simulation(input_file)
        simulation.writeSimulationFiles()


if __name__ == "__main__":
    main()
