from setuptools import setup
import stacksync_api_v2

setup(name='stacksync_api_v2',
      version=stacksync_api_v2.__version__,
      description='StackSync API v2 library',
      author='The StackSync Team',
      url='http://stacksync.org',
      packages=['stacksync_api_v2'],
      requires=['swift(>=1.4)']
      )
