#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_Simulation
----------------------------------

Tests for `Simulation` class
"""


import sys
import unittest
from contextlib import contextmanager
import JobSubmitter
from JobSubmitter import Simulation
from JobSubmitter import cli


class TestSimulation(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__get_Times(self):
        """Test for the _get_Times method"""
        input_file = cli.read_jsonfile('../data/input_example.json')
        sim = Simulation.Simulation(input_file)
        sim.start_time = 0
        sim.final_time = 100


