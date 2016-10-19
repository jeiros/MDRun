#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_JobSubmitter
----------------------------------

Tests for `JobSubmitter` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from JobSubmitter import JobSubmitter
from JobSubmitter import cli


# class TestJobsubmitter(unittest.TestCase):

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def test_000_something(self):
#         pass

#     def test_command_line_interface(self):
#         runner = CliRunner()
#         result = runner.invoke(cli.main)
#         assert result.exit_code == 0
#         assert 'JobSubmitter.cli.main' in result.output
#         help_result = runner.invoke(cli.main, ['--help'])
#         assert help_result.exit_code == 0
#         assert '--help  Show this message and exit.' in help_result.output


class TestHelloWorld(unittest.TestCase):

    """docstring for TestHelloWorld"""

    def setUp(self):
        self.hello_message = "Hello, world"

    def test_print_hello_world(self):
        output = JobSubmitter.hello()
        assert(output == self.hello_message)
