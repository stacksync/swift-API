from stacksync_api_v2 import STACKSYNC, DUMMY
from stacksync_api_v2.stacksync_server import StacksyncServerController
from stacksync_api_v2.dummy_server import DummyServerController


class ServerControllerFactory(object):

    def get_server(self, kind, host, port):
        if kind == STACKSYNC:
            return StacksyncServerController(host, port)
        elif kind == DUMMY:
            return DummyServerController()
