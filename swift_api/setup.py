__author__ = 'Edgar Zamora Gomez'

from setuptools import setup

import swift_server

setup(name='stacksync-api',
      version=swift_server.version,
      description='StackSync API WEB module for OpenStack Swift',
      author='AST Research Group',
      author_email='edgar.zamora@urv.cat',
      url='',
      packages=['swift_server', 'resources'],
      requires=['swift(>=1.4)','stacksync_api_v2(==2.0)'],
      entry_points={'paste.filter_factory':
                        ['stacksync_api=swift_server.swift_server:filter_factory']})