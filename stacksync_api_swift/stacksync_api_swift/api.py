import os
from swift.common.swob import wsgify, HTTPUnauthorized, HTTPBadRequest
from stacksync_api_v2.api_library import StackSyncApi
from stacksync_api_v2 import STACKSYNC
from swift.common.utils import get_logger


class StackSyncMiddleware(object):
    def __init__(self, app, conf):
        self.app = app
        host = conf.get('stacksync_host', '127.0.0.1').lower()
        port = conf.get('stacksync_port', 61234)
        self.api_library = StackSyncApi(STACKSYNC, host=host, port=port)
        self.app.logger = get_logger(conf, log_route='stacksync_api')
        self.app.logger.info('StackSync API: Init OK')

    @wsgify
    def __call__(self, req):
        self.app.logger.info('StackSync API: __call__: %r', req.environ)
        if not self.__is_api_call(req):
            return self.app

        response = self.authorize(req)
        if response:
            return response

        # redirect the request to the proper resource
        #TODO: replace this code by regular expressions that identify resources
        head, tail = os.path.split(req.environ['PATH_INFO'])
        if tail == 'data' or tail == 'versions' or tail == 'file' or tail == 'folder' or tail == 'contents':
            return self.__call_resource(tail, req)
        else:
            head, tail = os.path.split(head)
            if tail == 'data' or tail == 'versions' or tail == 'file' or tail == 'folder':
                return self.__call_resource(tail, req)

        # request does not match any resource
        return HTTPBadRequest()

    def __call_resource(self, tail, req):
        controller = __import__('resources' + '.' + tail + '_resource', globals(), locals(),
                                ['GET', 'POST', 'DELETE', 'PUT'], -1)

        self.app.logger.info('StackSync API: call_object: method info: %s path info: %s', req.method, req.path)

        response = getattr(controller, req.method)(req, self.api_library, self.app)

        return response

    def authorize(self, req):
        self.app.logger.info('StackSync API: authorize: path info: %s', req.path)
        if 'swift.authorize' in req.environ:
            resp = req.environ['swift.authorize'](req)
            del req.environ['swift.authorize']
            return resp
        return HTTPUnauthorized()

    def __is_api_call(self, req):
        enable_api = False
        headers = req.headers.items()
        for header, value in headers:
            if header.lower() == 'stacksync-api' and value.lower() == 'v2':
                enable_api = True
        return enable_api


def filter_factory(global_conf, **local_conf):
    """Standard filter factory to use the middleware with paste.deploy"""
    conf = global_conf.copy()
    conf.update(local_conf)

    def stacksync_filter(app):
        return StackSyncMiddleware(app, conf)

    return stacksync_filter

