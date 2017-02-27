#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_CLI
----------------------------------

Tests for the command line interface
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner
import mdrun
from mdrun import cli


class TestCLI(object):

    """docstring for TestCLI"""

    def setUp(self):
        self.input_file = cli.read_jsonfile('data/input_example.json')
        self.testing_dict = {'HPC_job': 'True',
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

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'Console script for JobSubmitter' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_read_jsonfile(self):
        """Test the read_json function"""
        try:
            assert type(self.input_file) is dict
        finally:
            assert self.input_file == self.testing_dict
