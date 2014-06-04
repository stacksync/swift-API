import sys, os
from swift.common.swob import wsgify, HTTPUnauthorized
from stacksync_api_v2.api_library import StackSyncApi
from swift.common.utils import get_logger


class StackSyncMiddleware(object):

    def __init__(self, app, conf, *args, **kwargs):
        self.app = app
        self.conf = conf
        #Use Api_Library module with dummy or stacksync sever to handle the metadata
        self.api_library = StackSyncApi('stacksync')
        self.app.logger = get_logger(conf, log_route='stacksync_api')
        self.app.logger.info('StackSync API: Init OK')

    @wsgify
    def __call__(self, req):
        self.app.logger.info('StackSync API: __call__: %r', req.environ)
        if not self.isAPICall(req.headers.items()):
            return self.app
        response = self.authorize(req)
        if response:
            return response

        #Redirect the petition to resource using url information
        head, tail = os.path.split(req.environ['PATH_INFO'])
        if tail == 'data' or tail == 'versions' or tail == 'file' or tail == 'folder' or tail == 'contents':
            return self.call_object(tail, req)
        else:
            head, tail = os.path.split(head)
            if tail == 'data' or tail == 'versions' or tail == 'file' or tail == 'folder':
                return self.call_object(tail, req)
        #return error (bad request) if it was not any case
        return self.app

    def call_object(self, tail, req):
        controller = __import__('resources' + '.' + tail + '_resource', globals(), locals(), ['GET', 'POST', 'DELETE' \
            , 'PUT'], -1)

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

    def isAPICall(self, headers):

        existStackSyncHeader = False
        for header, value in headers:
            if header.lower() == 'stacksync-api' and value.lower() == 'v2':
                existStackSyncHeader = True

        return existStackSyncHeader


def filter_factory(global_conf, **local_conf):
    """Standard filter factory to use the middleware with paste.deploy"""
    conf = global_conf.copy()
    conf.update(local_conf)

    def stacksync_filter(app):
        return StackSyncMiddleware(app, conf)

    return stacksync_filter

