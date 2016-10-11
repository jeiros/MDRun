from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='JobSubmitter',
      version='0.1',
      description='Automated submission of MD runs in HPC service with PBS',
      url='https://github.com/jeiros/JobSubmitter',
      author='Juan Eiros',
      author_email='juaneiros@hotmail.com',
      license='MIT',
      scripts=['bin/generate_scripts', 'bin/launcher.sh'],
      packages=['jobsubmitter'],
      include_package_data=True,
      zip_safe=False)
