===============================
Job Submitter
===============================


.. image:: https://img.shields.io/pypi/v/JobSubmitter.svg
        :target: https://pypi.python.org/pypi/JobSubmitter

.. image:: https://img.shields.io/travis/jeiros/JobSubmitter.svg
        :target: https://travis-ci.org/jeiros/JobSubmitter

.. image:: https://readthedocs.org/projects/JobSubmitter/badge/?version=latest
        :target: https://JobSubmitter.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/jeiros/JobSubmitter/shield.svg
     :target: https://pyup.io/repos/github/jeiros/JobSubmitter/
     :alt: Updates


Python tool to generate the appropriate files for long classic MD runs in the Imperial College HPC facility.
The objective is to automate the process, so you can chain several jobs and get the results of each one directly
to your machine. No more manual edit of your submission scripts, copying restart files back and forth, etc.

**Before you start:** You need to set up your [passwordless ssh](http://www.linuxproblem.org/art_9.html) from your local machine to the HPC.
To test if it works properly, you should be able to secure-copy a file from the HPC to your local machine
and not be prompted for your password. Like so: 
```
je714@ch-knuth.ch.ic.ac.uk:~$ scp je714@login.cx1.hpc.ic.ac.uk:/home/je714/test_file.txt .
test_file.txt              100%    0     0.0KB/s   00:00
```

Create an example input file using the `jobsubmitter example` command.

* Free software: MIT license
* Documentation: https://JobSubmitter.readthedocs.io.


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

