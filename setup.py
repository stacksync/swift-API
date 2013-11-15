from setuptools import setup

import apiweb

setup(name='apiweb',
      version=apiweb.version,
      description='StackSync API WEB module for OpenStack Swift',
      author='AST Research Group',
      author_email='guillermo.guerrero@urv.cat, cristian@cotesgonzalez.com, adria.moreno@urv.cat',
      url='',
      packages=['apiweb'],
      requires=['swift(>=1.4)'],
      entry_points={'paste.filter_factory':
                        ['apiweb=apiweb.apiweb:filter_factory']})
