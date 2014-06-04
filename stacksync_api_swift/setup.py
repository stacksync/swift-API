from setuptools import setup
import stacksync_api_swift

setup(name='stacksync_api_swift',
      version=stacksync_api_swift.__version__,
      description='StackSync API module for OpenStack Swift',
      author='The StackSync Team',
      url='http://stacksync.org',
      packages=['stacksync_api_swift', 'stacksync_api_swift.resources'],
      requires=['swift(>=1.4)'],
      install_requires=['stacksync_api_v2>=2.0', 'python-magic>=0.4.6'],
      entry_points={'paste.filter_factory':
                        ['stacksync_api=stacksync_api_swift.swift_server:filter_factory']})
