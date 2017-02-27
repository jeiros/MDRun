#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_Simulation
----------------------------------

Tests for `Simulation` class
"""

from __future__ import print_function, absolute_import
import os
import sys
import unittest
from contextlib import contextmanager
import mdrun
from mdrun import Simulation
from mdrun import cli
import nose.tools


class TestSimulation:

    def setUp(self):
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

    def test__get_NumberOfJobs1(self):
        sim = Simulation.Simulation(self.testing_dict)
        assert sim._get_NumberOfJobs() == 11

    @nose.tools.raises(ValueError)
    def test__get_NumberOfJobs2(self):
        sim = Simulation.Simulation(self.testing_dict)
        sim.job_length = 43
        sim._get_NumberOfJobs()

    @nose.tools.raises(ValueError)
    def test__get_NumberOfJobs3(self):
        sim = Simulation.Simulation(self.testing_dict)
        sim.start_time = -1
        sim._get_NumberOfJobs()

    @nose.tools.raises(ValueError)
    def test__get_NumberOfJobs4(self):
        sim = Simulation.Simulation(self.testing_dict)
        sim.start_time = 10
        sim.final_time = 5
        sim._get_NumberOfJobs()

    def test__get_Times1(self):
        """Test for the _get_Times method"""
        sim = Simulation.Simulation(self.testing_dict)
        times = sim._get_Times()
        target_times = {1: '0000-0050',
                        2: '0050-0100',
                        3: '0100-0150',
                        4: '0150-0200',
                        5: '0200-0250',
                        6: '0250-0300',
                        7: '0300-0350',
                        8: '0350-0400',
                        9: '0400-0450',
                        10: '0450-0500'}
        assert times == target_times
