'''
Created on 17/02/2014

@author: Edgar Zamora Gomez
'''
import sys, os
from swift.common.swob import wsgify, HTTPUnauthorized
from v2.api_library import Api_library


class StackSyncMiddleware(object):
    def __init__(self, app, conf, *args, **kwargs):
        self.app = app
        self.conf = conf
        #Use Api_Library module with dummy or stacksync sever to handle the metadata
        self.api_library = Api_library('stack')
    
    @wsgify
    def __call__(self, req):
     
        '''Test user provisional'''
        req.environ["stacksync_user_id"] = "8a534b8a-2aa6-4b08-b4d9-dfb2556376ab"
        if not self.isAPICall(req.headers.items()):
            return self.app
        
        response = self.authorize(req)
        if response:
            return response

                #Redirect the petition to resource using url information
        head, tail = os.path.split(req.environ['PATH_INFO'])
        if tail == 'data'or tail == 'versions'or tail == 'file' or tail == 'folder' or tail == 'contents':
            return self.call_object(tail, req)
        else:
            head, tail = os.path.split(head)
            if tail == 'data'or tail == 'versions'or tail == 'file' or tail == 'folder':
                return self.call_object(tail, req)
        #return error (bad request) if it was not any case
#         version, account, container, resource, ids = split_path(req.path_info, 1, 5, True)
        return self.app
    
    def call_object(self, tail, req):
        controller = __import__('resources'+'.'+tail+'_resource', globals(), locals(), ['GET','POST','DELETE'\
                                                                                        ,'PUT'], -1)
        response = getattr(controller, req.method)(req, self.api_library, self.app)
#         module_ = self.my_import(tail+'_resource')
#         obj = getattr(module_, tail + '_resource')(req, self.api_library)
        return response
    
    def authorize(self, req):
        if 'swift_api.authorize' in req.environ:
            resp = req.environ['swift_api.authorize'](req)
            if not resp:
                # No resp means authorized, no delayed recheck required.
                del req.environ['swift_api.authorize']
            else:
                # Response indicates denial, but we might delay the denial
                # and recheck later. If not delayed, return the error now.
                response = HTTPUnauthorized()

                return response
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
