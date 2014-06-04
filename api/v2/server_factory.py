'''
Created on 04/02/2014

@author: Edgar Zamora Gomez
'''

from stacksync_server import StacksyncServerController
from dummy_server import DummyServerController
STACKSYNC = 'stack'
DUMMY = 'dummy'
class server_factory(object):
    def new_server(self, kind):
        if kind == STACKSYNC:
            return StacksyncServerController("localhost", 61234)
        elif kind == DUMMY:
            return DummyServerController()
