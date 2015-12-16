#!/usr/bin/env python
"""
Fantail provides a configuration object that can be saved to disk as a YAML
file. Fantail can be used to store program configuration and make the
configuration data easily accessible."""

from setuptools.command.test import test as TestCommand
import sys

from distutils.core import setup

class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

DESCRIPTION = "Yaml based application configuration"

setup(name='fantail',
      version='0.2.4',
      description=DESCRIPTION,
      author='Mark Fiers',
      author_email='mark.fiers42@gmail.com',
      url='https://github.com/mfiers/Fantail',
      include_package_data=True,
      packages=['fantail'],
      install_requires=[
          'PyYAML>=3.0',
          'requests'
          ],
      tests_require=['tox', 'PyYAML>=3.0'],
      cmdclass={'test': Tox},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ]
      )
