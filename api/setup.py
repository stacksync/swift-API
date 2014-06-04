from setuptools import setup

import v2

setup(name='v2',
      version=v2.version,
      description='StackSync API WEB module for OpenStack Swift',
      author='AST Research Group',
      url='http://stacksync.org',
      packages=['v2'],
      requires=['swift(>=1.4)']
      )
