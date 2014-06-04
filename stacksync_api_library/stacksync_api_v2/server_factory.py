from stacksync_api_v2.stacksync_server import StacksyncServerController
from stacksync_api_v2.dummy_server import DummyServerController

STACKSYNC = 'stacksync'
DUMMY = 'dummy'

class ServerControllerFactory(object):

    def get_server(self, kind):
        if kind == STACKSYNC:
            return StacksyncServerController("localhost", 61234)
        elif kind == DUMMY:
            return DummyServerController()
