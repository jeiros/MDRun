===============================
MDRun
===============================


.. image:: https://img.shields.io/pypi/v/JobSubmitter.svg
        :target: https://pypi.python.org/pypi/mdrun

.. image:: https://travis-ci.org/jeiros/MDRun.svg?branch=master
    :target: https://travis-ci.org/jeiros/MDRun

.. image:: https://readthedocs.org/projects/JobSubmitter/badge/?version=latest
        :target: https://JobSubmitter.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/jeiros/JobSubmitter/badge.svg?branch=master
        :target: https://coveralls.io/github/jeiros/JobSubmitter?branch=master


I've started developing this Python program to generate the appropriate files for long classic
Molecular Dynamics (MD) runs in the Imperial College HPC facility, using the AMBER MD engine (GPU version).


The objective is to automate the process, so you can chain several jobs and get the results of each one directly
to your machine. No more manual edit of your submission scripts, copying restart files back and forth, etc. All is
needed is to specify the settings of your simulation in a configuration JSON file and then chain the PBS jobs using
dependency on each other.

Maybe this can be useful for other people as well, I think this should be fairly general for other HPC facilities.

Before you start
----------------

You need to set up your `passwordless ssh <http://www.linuxproblem.org/art_9.html>`_ from your local machine to the HPC.
To test if it works properly, you should be able to ``scp`` a file from the HPC to your local machine
and not be prompted for your password. Like so::

    $ scp username@HPC-hostname:/home/username/test_file.txt .
    test_file.txt              100%    0     0.0KB/s   00:00

You should also check that `rsync <https://download.samba.org/pub/rsync/>`_ is available in your HPC cluster,
since it is used to transfer the files (should be available in any Linux distribution, I think).

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
