'''
Created on 05/02/2014

@author: Edgar Zamora Gomez
'''
from twisted.internet import reactor
from twisted.web import server, resource, http
from v2.api_library import Api_library
import string, json, random
from urllib import quote
import os, sys

#init the api_library instance. You can select between 'dummy' or 'stack'
global api_library
api_library = Api_library('dummy')

def split_path(path, minsegs=1, maxsegs=None, rest_with_last=False):
    """
    Validate and split the given HTTP request path.
    **Examples**::

        ['a'] = split_path('/a')
        ['a', None] = split_path('/a', 1, 2)
        ['a', 'c'] = split_path('/a/c', 1, 2)
        ['a', 'c', 'o/r'] = split_path('/a/c/o/r', 1, 3, True)

    :param path: HTTP Request path to be split
    :param minsegs: Minimum number of segments to be extracted
    :param maxsegs: Maximum number of segments to be extracted
    :param rest_with_last: If True, trailing data will be returned as part
                           of last segment.  If False, and there is
                           trailing data, raises ValueError.
    :returns: list of segments with a length of maxsegs (non-existant
              segments will return as None)
    :raises: ValueError if given an invalid path
    """
    if not maxsegs:
        maxsegs = minsegs
    if minsegs > maxsegs:
        raise ValueError('minsegs > maxsegs: %d > %d' % (minsegs, maxsegs))
    if rest_with_last:
        segs = path.split('/', maxsegs)
        minsegs += 1
        maxsegs += 1
        count = len(segs)
        if (segs[0] or count < minsegs or count > maxsegs or
                '' in segs[1:minsegs]):
            raise ValueError('Invalid path: %s' % quote(path))
    else:
        minsegs += 1
        maxsegs += 1
        segs = path.split('/', maxsegs)
        count = len(segs)
        if (segs[0] or count < minsegs or count > maxsegs + 1 or
                '' in segs[1:minsegs] or
                (count == maxsegs + 1 and segs[maxsegs])):
            raise ValueError('Invalid path: %s' % quote(path))
    segs = segs[1:maxsegs]
    segs.extend([None] * (maxsegs - 1 - len(segs)))
    return segs

def clear_args(args):
    for x in args.keys():
        args[x] = args[x][0]
    return args
    
class Simple(resource.Resource):
    isLeaf = False
    def my_import(self, name):
        __import__(name)
        return sys.modules[name]
    def call_object(self, tail, request):
        module_ = self.my_import('server')
        obj = getattr(module_, tail + '_resource')()
        return obj
    def getChild(self, name, request):
        #Check auth_token parameter. Authorize user.
        #In twisted model only check if header contents auth_token key.
        headers = request.received_headers.copy()
        if not headers.has_key('x-auth-token'):
            return resource.ErrorPage(401, "AUTHORIZATION REQUIRED", "You are not authorized.").render(request)

            
        #Redirect the petition to resource using url information     
        head, tail = os.path.split(request.uri)
        if tail == 'data'or tail == 'versions'or tail == 'file' or tail == 'folder' or tail == 'contents':
            return self.call_object(tail, request)
        else:
            head, tail = os.path.split(head)
            if tail == 'data'or tail == 'versions'or tail == 'file' or tail == 'folder':
                return self.call_object(tail, request)
        
        return resource.NoResource()
#         return resource.Resource.getChild(self, name, request)
    def render_GET(self, request):
        return "Prepath=%r, Args=%r" % (request.prepath, request.args,)
    

class file_resource(resource.Resource):  
    isLeaf = True
    def render_POST(self, request):
        
        args = clear_args(request.args)
        parent = args.get('parent')
        name = args.get('name')
        if not name:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "It's mandatory to enter a name").render(request)

        message = api_library.post_metadata(1234, name, parent)
       
        # create a file using name of arguments
        f3 = open(args.get("name"), 'w')
        f3.close()
        
        request.setHeader("content-type", "application/json")
        request.write(message)
        request.finish()
        return server.NOT_DONE_YET
    
    def render_DELETE(self, request):
     
        try:
            _, _, file_id = split_path(request.path, 3, 3, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "It's mandatory to enter a file_id. ").render(request)
        # get Metadata of the file
        message = api_library.delete_item(1234, file_id)
   
        
        request.setHeader("content-type", "application/json")
        request.write(message)
        request.finish()
        return server.NOT_DONE_YET
    
    def render_GET(self, request):  
 
        try:
            _, _, file_id = split_path(request.path, 3, 3, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "It's mandatory to enter a file_id. ").render(request)

        message = api_library.get_metadata(1234, file_id)
        
        if not message:
            return resource.ErrorPage(404, "NOT FOUND", "File or folder not found at the specified path:" + request.path).render(request)

        request.setHeader("content-type", "application/json")
        request.write(message)        
        request.finish()
        return server.NOT_DONE_YET
       
    def render_PUT(self, request):

        parameters = http.parse_qs(request.content.read(), 1)

        try:
            _, _, file_id = split_path(request.path, 3, 3, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "It's mandatory to enter a file_id. ").render(request)

        try:
            parent = parameters.get('parent')
        except:
            parent = None
        try:
            name = parameters.get('name')
        except:
            name = None
        message = api_library.put_metadata(1234, file_id, name, parent)

        request.setHeader("content-type", "application/json")
        request.write(message)
        request.finish()
        return server.NOT_DONE_YET
        # TODO: Move file to different parent
        
class versions_resource(resource.Resource):    
    isLeaf = True
    def render_GET(self, request):
        try:    
            _, _, file_id, resource, version = split_path(request.path, 4, 5, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "en principi no tindrie que passar aixo jaja").render(request)
        # if version alone return all versions metadata
        if not version:
            message = api_library.get_versions(1234, file_id)
            if not message:
                return resource.ErrorPage(404, "NOT FOUND", "File or folder not found at the specified path:" + request.path).render(request)
            request.write(message)
            request.finish()
            return server.NOT_DONE_YET
        # if version/id return information about specific version
        message = api_library.get_metadata(1234, file_id, specific_version=version)
        if not message:
            return resource.ErrorPage(404, "NOT FOUND", "File or folder not found at the specified path:" + request.path).render(request)
        request.write(message)
        request.finish()
        return server.NOT_DONE_YET
        
        '''
        The case /api/file/file_id/versions/version_id/data you can find in data_resource
        ''' 
    
class contents_resource(resource.Resource):
    isLeaf = True
    def render_GET(self, request):

        args = clear_args(request.args)
        try:
            include_deleted = args.get('include_deleted')
        except:
            include_deleted = False
        try:    
            _, _, folder_id, _ = split_path(request.path, 4, 4, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "No tindrie que entra mai aqui ").render(request)
        
        message = api_library.get_folder_contents(123, folder_id, include_deleted)
        if not message:
            return resource.ErrorPage(404, "NOT FOUND", "File or folder not found at the specified path:" + request.path).render(request)
        request.setHeader("content-type", "application/json")
        request.write(message)
        request.finish()
        return server.NOT_DONE_YET
    
class folder_resource(resource.Resource):    
    isLeaf = True
    
    def render_POST(self, request):

        args = clear_args(request.args)
      
        parent = args.get('parent')
        name = args.get('name')
        if not name:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "It's mandatory to enter a file name. ").render(request)
        
        message = api_library.post_folder(1234, name, parent)

        request.setHeader("content-type", "application/json")
        request.write(message)
        request.finish()
        return server.NOT_DONE_YET
    
    def render_DELETE(self, request):

        try:    
            _, _, folder_id = split_path(request.path, 3, 3, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "It's mandatory to enter a folder_id. ").render(request)
        
        message = api_library.delete_item(123, folder_id)
        if not message:
            return resource.ErrorPage(404, "NOT FOUND", "File or folder not found at the specified path:" + request.path).render(request)
        request.setHeader("content-type", "application/json")
        request.write(message)
        request.finish()
        return server.NOT_DONE_YET
    
    def render_GET(self, request):

        try:    
            _, _, folder_id = split_path(request.path, 3, 3, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "It's mandatory to enter a folder_id. ").render(request)
        message = api_library.get_metadata(123, folder_id)

        if not message:
            return resource.ErrorPage(404, "NOT FOUND", "File or folder not found at the specified path:" + request.path).render(request)
               

        request.setHeader("content-type", "application/json")
        request.write(message)
        request.finish()
        return server.NOT_DONE_YET 
    
    def render_PUT(self, request):

        args = http.parse_qs(request.content.read(), 1)
        try:
            _, _, folder_id = split_path(request.path, 3, 3, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "It's mandatory to enter a folder_id. ").render(request)

        parent = args.get('parent')
        name = args.get('name')
            
        message = api_library.put_metadata(1234, folder_id, name, parent)
        
        request.write(message)
        request.finish()
        return server.NOT_DONE_YET
    
class data_resource(resource.Resource):
    isLeaf = True
    
    def render_PUT(self, request):

        #take parameters. In this case, the content for update the file
        args = http.parse_qs(request.content.read(), 1)
        if not args:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "Supervise parameters, you not put anything to update ").render(request)

        try:
            _, file_resource, file_id, _ = split_path(request.path, 4, 4, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "Supervise parameters, the correct form is api/file/file_id/data ").render(request)
    
        # We look up the name of file, and full path, to update it.
        message = api_library.get_metadata(1234, file_id)
        if not message:
            return resource.ErrorPage(404, "NOT FOUND", "File or folder not found at the specified path:" + request.path).render(request)
        message = json.loads(message)
        # Create new version to save old content version
        #TODO: Define mimetype, size and chunk
        message_new_version = api_library.update_data(1234, message["id"], message["parent"], None, None, None)
        if not message_new_version:
            return resource.ErrorPage(404, "NOT FOUND", "Some problem to create a new version of file").render(request)

        # TODO: Using name and full path update the file into DB, using new version.
  
        request.setHeader("content-type", "application/json")
        request.finish()
        return server.NOT_DONE_YET
    
    def render_GET(self, request):

        try:
            _, file_resource, file_id, resource, version, _ = split_path(request.path, 4, 6, True)
        except:
            return resource.ErrorPage(400, "INCORRECT PARAMETERS", "Supervise parameters, something is wrong").render(request)

        metadata = api_library.get_metadata(1234, file_id, include_chunks=True, specific_version=version)  
        if not metadata:
                return resource.ErrorPage(404, "NOT FOUND", "File or folder not found at the specified path:" + request.path).render(request)

        # TODO: using metadata, where we can find the name and path of file, return content of file with DB
        content = 'There are the content of specific version of file'
        request.setHeader("content-type", "application/json")
        request.setHeader("content-length", len(content))
        request.write(content)
        request.finish()
        return server.NOT_DONE_YET




if __name__ == '__main__':
    root = Simple()
    api = Simple()
    root.putChild('api', api)

    print 'Server started'
    site = server.Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()
