#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
]

test_requirements = [
    'nosetests>=1.3.7',
]


NAME = "mdrun"
VERSION = '0.1.5'


setup(
    name=NAME,
    version=VERSION,
    description="Submission of MD runs to HPC with PBS",
    long_description=readme + '\n\n' + history,
    author="Juan Eiros",
    author_email='jeirosz@gmail.com',
    url='https://github.com/jeiros/%s' % NAME,
    download_url='https://github.com/jeiros/%s/archive/%s.tar.gz' % (NAME, VERSION),
    packages=find_packages(exclude=['docs', 'tests*']),
    entry_points={
        'console_scripts': [
            'mdrun=mdrun.cli:main'
        ]
    },
    scripts=['mdrun/bin/launch_PBS_jobs'],
    package_data={'mdrun': ['data/*']},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='MD',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
