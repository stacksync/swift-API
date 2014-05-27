# Copyright (c) 2010 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time, datetime
import zlib, gzip, StringIO
import string, json, random
import xmlrpclib
import magic

from swift.common.swob import HTTPBadRequest, HTTPAccepted, HTTPOk, HTTPCreated, HTTPInternalServerError,\
    HTTPNotFound, HTTPServerError, HTTPUnauthorized, HTTPForbidden,\
    HTTPMethodNotAllowed, wsgify, Request, Response
from swift.common.request_helpers import get_param
from linecache import updatecache
from gzip import GzipFile
from hashlib import sha1
from swift.common.wsgi import make_pre_authed_request

CHUNK_SIZE = 524288

class Chunk(object):
    def __init__(self, checksum):
        #self.checksum = str(long(checkSum)).rjust(20, '0').upper()
        self.checksum = checksum.upper()
                
    def getFileName(self):
        return "chk-" + self.checksum


# TODO: This is not useful
class Controller(object):
    def __init__(self, app):
        self.app = app
        self.response_args = []

    def do_start_response(self, status, headers, exc_info=None):
        """
        Saves response info without sending it to the remote client.
        Uses the same semantics as the usual WSGI start_response.
        """
        self._response_status = status
        self._response_headers = headers
        self._response_exc_info = exc_info

class GzipWrap(object):
    # input is a filelike object that feeds the input
    def __init__(self, inputStream, filename = None):
        self.input = inputStream
        self.buffer = ''
        self.zipper = GzipFile(filename, mode = 'wb', fileobj = self)

    def read(self, size=-1):
        if (size < 0) or len(self.buffer) < size:
            for s in self.input:
                self.zipper.write(s)
                if size > 0 and len(self.buffer) >= size:
                    self.zipper.flush()
                    break
            else:
                self.zipper.close()
            if size < 0:
                ret = self.buffer
                self.buffer = ''
        else:
            ret, self.buffer = self.buffer[:size], self.buffer[size:]
        return ret

    def flush(self):
        pass

    def write(self, data):
        self.buffer += data

    def close(self):
        self.zipper.close()


class BuildFile(object):
    #chunks are the content chunks
    #listNames are the list of chunks names
    def __init__(self, content, chunks):
        self.listNames = []
        self.hashesList = []
        self.content = content
        self.chunks = chunks
        
    def join(self): 
        
        self.content = ""
        for chunk in self.chunks:                    
            f = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(chunk))
            temp = f.read()
            f.close()
                     
            self.content += temp         
            
    def adlerHash(self, data):
        return (zlib.adler32(data) & 0xffffffff)
    
    def sha1Hash(self, data):
        shaHash = sha1()
        shaHash.update(data)
        return shaHash.hexdigest()    
    
    def separate(self):                
        numChunks = int(len(self.content)/CHUNK_SIZE)        
        self.listNames = []
        
        if(numChunks > 0):
            lastIndex = 0
            for i in range(numChunks):
                data = self.content[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE]
                checksum = self.sha1Hash(data)

                chunkObject = Chunk(checksum)
                self.listNames.append(chunkObject.getFileName())
                self.hashesList.append(checksum.upper())
                
                f = GzipWrap(data)
                chunk = f.read()                
                f.close()
                
                self.chunks.append(chunk)
                lastIndex = i
                
            data = self.content[(lastIndex+1)*CHUNK_SIZE:]
        else:
            data = self.content
            
        if(len(data) > 0): #controlar si data no vale nada...
            checksum = self.sha1Hash(data)
            chunkObject = Chunk(checksum)
            
            #nameChunk = "chunk-" + str(long(checksum)).rjust(20, '0')
            self.listNames.append(chunkObject.getFileName())
            self.hashesList.append(checksum.upper())
        
            f = GzipWrap(data)
            chunk = f.read()
            f.close()
                        
            self.chunks.append(chunk)
        
class SyncServerController(Controller):
    """
    Handles requests on objects
    """
    def __init__(self, app, serverIp, serverPort, **kwargs):
        Controller.__init__(self, app)
        
        #Create Sync server connection
        self.xmlIp = serverIp
        self.xml = serverPort
        self.rpcServer = xmlrpclib.ServerProxy("http://"+serverIp+':'+str(serverPort))
        
    def getMetadata(self, user, requestId, fileId, includeList, includeDeleted, includeChunks, version):
        response = self.rpcServer.XmlRpcSyncHandler.getMetadata(user, requestId, fileId, includeList, includeDeleted, includeChunks, version);
        return response.encode('utf-8')
    
    def putMetadataFile(self, user, requestId, fileName, parent, overwrite, checksum, fileSize, mimetype, chunks):
        response = self.rpcServer.XmlRpcSyncHandler.putMetadataFile(user, requestId, fileName, parent, overwrite, checksum, fileSize, mimetype, chunks);
        return response.encode('utf-8')
    
    def getVersions(self, user, requestId, fileId):
        response = self.rpcServer.XmlRpcSyncHandler.getVersions(user, requestId, fileId);
        return response.encode('utf-8')
    
    def doDelete(self, user, requestId, fileId):
        response = self.rpcServer.XmlRpcSyncHandler.deleteMetadataFile(user, requestId, fileId);
        return response.encode('utf-8')
    
    def putMetadataFolder(self, user, requestId, folderName, parent):
        response = self.rpcServer.XmlRpcSyncHandler.putMetadataFolder(user, requestId, folderName, parent);
        return response.encode('utf-8')
    
    def restoreMetadata(self, user, requestId, fileId, version):
        response = self.rpcServer.XmlRpcSyncHandler.restoreMetadata(user, requestId, fileId, version);
        return response.encode('utf-8')        


class HttpHandler(Controller):
    """
    Handles requests on objects
    """
    def __init__(self, req, app, conf, **kwargs):
        Controller.__init__(self, app)
        
        self.req = req
        self.env = self.req.environ
        self.conf = conf
        
        self.updateList = []
        self.updateContent = []
        self.createRepository = True
        self.userID = self.env['PATH_INFO'].split('/')[2]
        
        self.ServerRpcIp = conf.get('rpc_server_ip')        
        if not self.ServerRpcIp:
            self.ServerRpcIp = '127.0.0.1'
            
        self.ServerRpcPort = conf.get('rpc_server_port')
        if not self.ServerRpcPort:
            self.ServerRpcPort = '61234'
            
        self.syncServer = SyncServerController(app, self.ServerRpcIp, self.ServerRpcPort)            
        
                
    def __generateDateTime(self):
        #delta = datetime.now() - datetime(1970, 1, 1)    
        #milliseconds = (delta.days * 24 * 60 * 60 + delta.seconds) * 1000 + delta.microseconds / 1000.0        
        delta = int(round(time.time() * 1000))
        return delta

    def __generateRandom(self):
        fileId = random.randrange(-9223372036854775808, 9223372036854775807)
        return fileId
    
    def __getRequestId(self):
        requestId = "Api-web_" + str(self.__generateDateTime())   
        return requestId

    def __getMetadataParameters(self):
        requestId = self.__getRequestId()                    
        fileId = get_param(self.req, "file_id", default="")            
        includeList = get_param(self.req, "list", default="")
        includeDeleted = get_param(self.req, "include_deleted", default="")
        #includeChunks = get_param(self.req, "include_chunks", default="")
        version = get_param(self.req, "version", default="")
        
        return requestId, fileId, includeList, includeDeleted, version
        
        
    def LIST(self):
        requestId, fileId, includeList, includeDeleted, version = self.__getMetadataParameters()
        includeChunks = "False"
        
        message = self.syncServer.getMetadata(self.userID, requestId, fileId, includeList, includeDeleted, includeChunks, version)
        
        # Check if error key exist
        data = json.loads(message)
        if "error" in data:
            # Create error response
            error = data["error"]
            return self.__createErrorResponse(error, message)
        else:
            return HTTPOk(body=message)
        
    
    def __getFile(self, env):
        self.response_args = []

        subrequest = make_pre_authed_request(env, agent=('%(orig)s '))       
        response = subrequest.get_response(self.app)

        if 200 <= response.status_int  < 300:
            pass
        #    new_hdrsFile = {}
        #    for key, val in headersFile.iteritems():
        #        _key = key.lower()
        #        if _key.startswith('x-object-meta-'):
        #            new_hdrsFile['x-amz-meta-' + key[14:]] = val
        #        elif _key in ('content-length', 'content-type', 'content-encoding', 'etag', 'last-modified'):
        #            new_hdrsFile[key] = val
            
        #    responseFile = Response(status=statusFile, headers=new_hdrsFile, app_iter=app_iterFile)        
        elif response.status_int == 401:
            response = HTTPUnauthorized()
        else:
            response = HTTPBadRequest()
            
        return response
    
    
    def __getChunks(self, env, urlBase, scriptName, chunks):    
        fileCompressContent = []
        statusFile = 200
        
        for chunk in chunks: 
            fileChunk = "chk-" + str(chunk)
                
            env['PATH_INFO'] = urlBase + '/' + fileChunk
            env['SCRIPT_NAME'] = scriptName
            
            responseFile = self.__getFile(env)
            statusFile  = responseFile.status_int  
            if 200 <= statusFile  < 300:            
                fileCompressContent.append(responseFile.body)
            else:
                fileCompressContent = []
                break
                                       
        return fileCompressContent, statusFile
    
    
    def GET(self):
        requestId, fileId, includeList, includeDeleted, version = self.__getMetadataParameters()   
        includeChunks = "True"
        
        # Check if no file id
        if not fileId: # TODO CHECK si funciona con strings vacios
            return HTTPBadRequest( body = "File id not specified" )
                    
        message = self.syncServer.getMetadata(self.userID, requestId, fileId, includeList, includeDeleted, includeChunks, version)
        
        # Check if error key exist
        data = json.loads(message)
        if "error" in data:
            # Create error response
            error = data["error"]
            return self.__createErrorResponse(error, message)            
        
        urlBase = self.env['PATH_INFO'].replace("/files", "")
        scriptName = self.env['SCRIPT_NAME']
        self.env['QUERY_STRING'] = ""
        
        fileCompressContent, status = self.__getChunks(self.env, urlBase, scriptName, data['chunks'])
        if(len(fileCompressContent) > 0):
            joinFile = BuildFile("", fileCompressContent)
            joinFile.join()
            return HTTPOk(body=joinFile.content)
        elif(len(data['chunks']) == 0):
            return HTTPOk(body="")
            
        
        if status == 401:
            return HTTPUnauthorized()
        else:
            return HTTPBadRequest()            


    def GETVERSIONS(self):
        requestId, fileId, includeList, includeDeleted, version = self.__getMetadataParameters()
        message = self.syncServer.getVersions(self.userID, requestId, fileId)
        
        # Check if error key exist
        data = json.loads(message)
        if "error" in data:
            # Create error response
            error = data["error"]
            return self.__createErrorResponse(error, message)
        else:
            return HTTPOk(body=message)   


    def __getPutParameters(self):        
        requestId = self.__getRequestId()
        fileName = self.req.params.get('file_name', "")
        parent = self.req.params.get('parent', "")
        overwrite = self.req.params.get('overwrite', "True")           
        
        return requestId, fileName, parent, overwrite

    def __uploadFileChunks(self, env, urlBase, scriptName, separateFile):        
        error = False
        for i in range(len(separateFile.chunks)):          
            chunkName = separateFile.listNames[i-1]
            chunkContent = separateFile.chunks[i-1]
                              
            env['PATH_INFO'] = urlBase + "/" + chunkName
            env['SCRIPT_NAME'] = scriptName

            subrequest = make_pre_authed_request(env, body=chunkContent, agent=('%(orig)s '))
            response = subrequest.get_response(self.app)            
            status = response.status_int                
    
            if 200 > status >= 300:
                break
            
        if(error):
            response = HTTPInternalServerError()
        else:            
            response = HTTPCreated()
         
        return response
    
    
    def __checkContainer(self):
        urlBase = self.env['PATH_INFO']        
        self.env['PATH_INFO'] = self.env['PATH_INFO'].replace("/files", "")
        
        scriptName = self.env['SCRIPT_NAME']
        self.env['SCRIPT_NAME'] = ""
        
        queryString = self.env['QUERY_STRING']
        self.env['QUERY_STRING'] = ""
       
        method = self.env['REQUEST_METHOD']
        self.env['REQUEST_METHOD'] = "GET"
        
        
        self.response_args = []
        
        app_iterFile = self.app(self.env, self.do_start_response)
        statusFile = int(self.response_args[0].split()[0])
        headersFile = dict(self.response_args[1])
        
        print statusFile
        if statusFile == 404:            
            self.response_args = []
        
            self.env['REQUEST_METHOD'] = "PUT"
            #self.env['PATH_INFO'] = self.env['PATH_INFO'] + "/stacksync"
            print self.env['PATH_INFO']
            app_iterFile = self.app(self.env, self.do_start_response)
            statusFile = int(self.response_args[0].split()[0])
            headersFile = dict(self.response_args[1])
            print statusFile
            print self.response_args

        self.env['PATH_INFO'] = urlBase                 
        self.env['SCRIPT_NAME'] = scriptName        
        self.env['QUERY_STRING'] = queryString
        self.env['REQUEST_METHOD'] = method

    def PUT(self):
        requestId, fileName, parent, overwrite = self.__getPutParameters()
        
        # Check if no file id
        if not fileName: # TODO CHECK si funciona con strings vacios
            return HTTPBadRequest( body = "File name not specified" )
        
        #self.__checkContainer()
        
        fileData = self.req.body        
        
        chunkMaker = BuildFile(fileData, [])
        chunkMaker.separate()
        
        urlBase = self.env['PATH_INFO'].replace("/files", "");
        scriptName = self.env['SCRIPT_NAME']
        response = self.__uploadFileChunks(self.env, urlBase, scriptName, chunkMaker)
        
        chunks = chunkMaker.hashesList
        checksum = str((zlib.adler32(fileData) & 0xffffffff))
        fileSize = str(len(fileData))
        mimetype = magic.from_buffer(fileData, mime=True)
        
        status = response.status_int
        if 200 > status >= 300:
            return response
            
        message = self.syncServer.putMetadataFile(self.userID, requestId, fileName, parent, overwrite, checksum, fileSize, mimetype, chunks)
        
        data = json.loads(message)
        if "error" in data:
            # Create error response
            error = data["error"]
            response = self.__createErrorResponse(error, str(json.dumps(data['description'])))
        else:
            response = HTTPCreated(body=str(json.dumps(data['metadata'])))
        
        return response
        
        
    def __getPostParameters(self):  
        requestId = self.__getRequestId()
        
        folderName = self.req.params.get("folder_name", "")
        parent = self.req.params.get("parent", "")
        version = self.req.params.get("version", "")
        fileId = self.req.params.get("file_id", "")
                   
        return requestId, folderName, parent, fileId, version
     
        
    def POST(self):
        requestId, folderName, parent, fileId, version = self.__getPostParameters()
        
        # Check if no file id
        if not folderName: # TODO CHECK si funciona con strings vacios
            return HTTPBadRequest( body = "Folder name not specified" )            
            
        message = self.syncServer.putMetadataFolder(self.userID, requestId, folderName, parent)
        
        data = json.loads(message)
        if "error" in data:
            # Create error response
            error = data["error"]
            response = self.__createErrorResponse(error, str(json.dumps(data['description'])))
        else:
            response = HTTPCreated(body=str(json.dumps(data['metadata'])))
        
        return response
    
        
    def POSTRESTORE(self):
        requestId, folderName, parent, fileId, version = self.__getPostParameters()
        
        # Check if no file id
        if not fileId or not version: # TODO CHECK si funciona con strings vacios
            return HTTPBadRequest( body = "Folder name not specified" )            
            
        message = self.syncServer.restoreMetadata(self.userID, requestId, fileId, version)
        
        data = json.loads(message)
        if "error" in data:
            # Create error response
            error = data["error"]
            response = self.__createErrorResponse(error, str(json.dumps(data['description'])))
        else:
            response = HTTPCreated(body=str(json.dumps(data['metadata'])))
        
        return response
    
    
    def __getParametersFromDelete(self):
        requestId = self.__getRequestId()
        fileId = self.req.params.get("file_id", "")

        return requestId, fileId
        
    
    def DELETE(self):            
        requestId, fileId = self.__getParametersFromDelete()
        #data["user"] = self.userID
        
        # Check if no file id
        if not fileId: # TODO CHECK si funciona con strings vacios
            return HTTPBadRequest( body = "File id not specified" )
        
        #TODO check if file exist
        
        message = self.syncServer.doDelete(self.userID, requestId, fileId)
        # Check if error key exist
        data = json.loads(message)
        if "error" in data:
            # Create error response
            error = data["error"]
            response = self.__createErrorResponse(error, message)
        else:
            response = HTTPOk(body=str(json.dumps(data['metadata'])))
        
        return response
    
            
    def __createErrorResponse(self, error, message):
        if error == 400:
            response = HTTPBadRequest(body = message)
        elif error == 401:
            response = HTTPUnauthorized(body = message)
        elif error == 403:
            response = HTTPForbidden(body = message)
        elif error == 404:
            response = HTTPNotFound(body = message)
        elif error == 405:
            response = HTTPMethodNotAllowed(body=message)
        else:
            response = HTTPServerError(body=message)
            
        return response    



class StackSyncMiddleware(object):
    """REST API for StackSync"""
    def __init__(self, app, conf, *args, **kwargs):
        self.app = app
        self.conf = conf

    @wsgify
    def __call__(self, request):
        req = request
        pathSplitted = req.path.lower().split("/")
        
        existStackSyncHeader = False
        for header, value in req.headers.items():
            if header.lower() == 'stacksync-api' and value.lower() == 'true':
                existStackSyncHeader = True
        
        if not existStackSyncHeader:
            return self.app
        
        if 'swift.authorize' in req.environ:
            resp = req.environ['swift.authorize'](req)
            if not resp:
                # No resp means authorized, no delayed recheck required.
                del req.environ['swift.authorize']
            else:
                # Response indicates denial, but we might delay the denial
                # and recheck later. If not delayed, return the error now.
                response = HTTPUnauthorized()     

                return response
        
        handler = HttpHandler(req, self.app, self.conf)
        if req.method == 'GET':
            if(pathSplitted[-1] == "metadata"):                           
                response = handler.LIST()
            elif(pathSplitted[-1] == "files"): 
                response = handler.GET()
            elif(pathSplitted[-1] == "versions"): 
                response = handler.GETVERSIONS()                
            else:
                response = HTTPBadRequest()        
        elif req.method == 'PUT': 
            if(pathSplitted[-1] == "files"): 
                response = handler.PUT()
            else:
                response = HTTPBadRequest()
        elif req.method == 'POST':
            if(pathSplitted[-1] == "files"): 
                response = handler.POST()
            elif(pathSplitted[-1] == "restore"): 
                response = handler.POSTRESTORE()            
            else:
                response = HTTPBadRequest()            
        elif req.method == 'DELETE':
            if(pathSplitted[-1] == "files"): 
                response = handler.DELETE()
            else:
                response = HTTPBadRequest()
        else:                        
            response = HTTPBadRequest()     
        
        return response                  


def filter_factory(global_conf, **local_conf):
    """Standard filter factory to use the middleware with paste.deploy"""
    conf = global_conf.copy()
    conf.update(local_conf)

    def stacksync_filter(app):
        return StackSyncMiddleware(app, conf)

    return stacksync_filter
