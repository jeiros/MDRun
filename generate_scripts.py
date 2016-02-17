#!/usr/bin/env python
import json
import sys
from src.write_MDcmds import write_MDscript
from src.write_PBS import write_PBSheader
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


def get_NumberOfJobs(json):
    total_time = json['simulation_details']['final_time'] - json['simulation_details']['start_time']
    job_length = json['simulation_details']['job_length']
    if (total_time % job_length) != 0:
        sys.exit("Job lenght must be a divisor of total simulation time.")
    else:
        return(int(total_time/job_length) + 1)


def get_Times(number_of_jobs, job_length, start_time):
    """
    Returns a dictionary with the corresponding time window for each
    job
    """
    timeList = {}
    for job in range(1, number_of_jobs):
        if job == 1:
            time_at_start = start_time
            time_at_finish = time_at_start + job_length
        else:
            time_at_finish = start_time + (job * job_length)
            time_at_start = time_at_finish - job_length
        seq = (str(time_at_start).zfill(4), str(time_at_finish).zfill(4))
        timeList[job] = '-'.join(seq)
    return(timeList)


def main():
    if args:
        input_file = read_jsonfile(args.InputFile)
        dictionary = get_Times(get_NumberOfJobs(input_file),
                               input_file['simulation_details']['job_length'],
                               input_file['simulation_details']['start_time'])
        print(dictionary)
        for i in range(1, get_NumberOfJobs(input_file)):
            write_PBSheader(i, input_file)
            write_MDscript(i, input_file, dictionary)


if __name__ == "__main__":
    main()
