'''
Created on 03/02/2014

@author: edgar
'''
import time
class DummyServerController():
    """
    Handles requests on objects
    """
    def get_metadata(self, user, file_id, include_chunks, version):
        #TODO: chunks, version
        if version and not include_chunks:
            return {
                    
                    "name":"Winter2012.jpg",
                    "path":"/documents/clients/Winter2012.jpg",
                    "id":32565632156,
                    "size":7482,
                    "mimetype":"image/jpg",
                    "status":"CHANGED",
                    "version":2,
                    "parent":12386548974,
                    "user":"Cristian",
                    "client_modified":"2013-03-08 10:36:41.997",
                    "server_modified":"2013-03-08 10:36:41.997"
                    }
            
        if include_chunks and not version:
            return {
                       "name":"Client1.pdf",
                       "path":"/documents/clients/Client1.pdf",
                       "id":32565632156,
                       "size":775412,
                       "mimetype":"application/pdf",
                       "chunks":["a", "b"],
                       "status":"DELETED",
                       "version":3,
                       "parent":-348534824681,
                       "user":"Adrian",
                       "client_modified":"2013-03-08 10:36:41.997",
                       "server_modified":"2013-03-08 10:36:41.997"
                    }
        if include_chunks and version:
            return {
                       "name":"Client1.pdf",
                       "path":"/documents/clients/Client1.pdf",
                       "id":32565632156,
                       "size":775412,
                       "mimetype":"application/pdf",
                       "chunks":["a", "b"],
                       "status":"DELETED",
                       "version":3,
                       "parent":-348534824681,
                       "user":"Adrian",
                       "client_modified":"2013-03-08 10:36:41.997",
                       "server_modified":"2013-03-08 10:36:41.997"
                    }
            
        response = {
                       "name":"Client1.pdf",
                       "path":"/documents/clients/Client1.pdf",
                       "id":32565632156,
                       "size":775412,
                       "mimetype":"application/pdf",
                       "status":"DELETED",
                       "version":3,
                       "parent":-348534824681,
                       "user":"Adrian",
                       "client_modified":"2013-03-08 10:36:41.997",
                       "server_modified":"2013-03-08 10:36:41.997"
        }
        return response
    
    def get_versions(self, user, file_id):
        response = [ {
                       "name":"Winter2012.jpg",
                       "path":"/documents/clients/Winter2012.jpg",
                       "id":32565632156,
                       "size":775412,
                       "mimetype":"image/jpg",
                       "status":"NEW",
                       "version":1,
                       "parent":12386548974,
                       "user":"Adrian",
                       "client_modified":"2013-03-08 10:36:41.997",
                       "server_modified":"2013-03-08 10:36:41.997"
                     },
                    
                     {
                       "name":"Winter2012.jpg",
                       "path":"/documents/clients/Winter2012.jpg",
                       "id":32565632156,
                       "size":7482,
                       "mimetype":"image/jpg",
                       "status":"CHANGED",
                       "version":2,
                       "parent":12386548974,
                       "user":"Cristian",
                       "client_modified":"2013-03-08 10:36:41.997",
                       "server_modified":"2013-03-08 10:36:41.997"
                     },
                     {
                       "name":"Winter2015.jpg",
                       "path":"/documents/clients/Winter2015.jpg",
                       "id":32565632156,
                       "size":775412,
                       "mimetype":"image/jpg",
                       "status":"RENAMED",
                       "version":3,
                       "parent":12386548974,
                       "user":"Adrian",
                       "client_modified":"2013-03-08 10:36:41.997",
                       "server_modified":"2013-03-08 10:36:41.997"
                     }
                    ]
        return response

                
    def get_folder_contents(self, user, folder_id, include_deleted):
        #TODO: user item in documentation doesn't exist
        response ={
                   "name":"clients",
                   "path":"/documents/clients",
                   "id":9873615,
                   "status":"NEW",
                   "version":1,
                   "parent":-348534824681,
                   "user":"Adrian",
                   "client_modified":"2013-03-08 10:36:41.997",
                   "server_modified":"2013-03-08 10:36:41.997",
                   "contents":[{ 
                                "name":"Client1.pdf",
                                "path":"/documents/clients/Client1.pdf",
                                "id":32565632156,
                                "size":775412,
                                "mimetype":"application/pdf",
                                "status":"DELETED",
                                "version":3,
                                "parent":-348534824681,
                                "user":"Adrian",
                                "client_modified":"2013-03-08 10:36:41.997",
                                "server_modified":"2013-03-08 10:36:41.997"
                                },
                               { 
                                "name":"Client1.pdf",
                                "path":"/documents/clients/Client1.pdf",
                                "id":32565632156,
                                "size":775412,
                                "mimetype":"application/pdf",
                                "status":"DELETED",
                                "version":3,
                                "parent":-348534824681,
                                "user":"Adrian",
                                "client_modified":"2013-03-08 10:36:41.997",
                                "server_modified":"2013-03-08 10:36:41.997"
                                }
                               ]
                   }
         
        return response
    
    def delete_item(self, user, file_id):
        response = {
           "name":"Client1.pdf",
           "path":"/documents/clients/Client1.pdf",
           "id":32565632156,
           "size":775412,
           "mimetype":"application/pdf",
           "status":"DELETED",
           "version":3,
           "parent":-348534824681,
           "user":"Adrian",
           "client_modified":"2013-03-08 10:36:41.997",
           "server_modified":"2013-03-08 10:36:41.997"
        }
        return response
    def new_folder(self, user, name, parent):
        response = {
                    "name":"clients",
                    "path":"/documents/clients",
                    "id":9873615,
                    "parent":-348534824681,
                    "user":"Adrian"
        }
        return response
    def new_file(self, user, name, parent):
        response = {
                    "name":"Client1.pdf",
                    "path":"/documents/clients/Client1.pdf",
                    "id":32565632156,
                    "parent":-348534824681,
                    "user":"Adrian"
        }
        return response
    def update_data(self, user, file_id, parent, mimetype, size, chunk):
        #TODO: Define this method, how to create a new version
        response = {
                    "name":"Client1.pdf",
                    "path":"/documents/clients/Client1.pdf",
                    "id":32565632156,
                    "parent":-348534824681,
                    "user":"Adrian"
        }
        return response

    def update_metadata(self, user, file_id, name, parent):
        response = {
         "name":"Winter2012_renamed.jpg",
        "path":"/documents/clients/Client1.pdf",
         "id":32565632156,
         "size":775412,
         "mimetype":"application/pdf",
         "status":"CHANGED",
         "version":2,
         "parent":12386548974,
         "user":"Adrian",
         "client_modified":"2013-03-08 10:36:41.997",
         "server_modified":"2013-03-08 10:36:41.997"
        }
        return response

    
    def touchNewFile(self, user, fileName, parent):
        requestId = self.__getRequestId()
        response = self.rpcServer.XmlRpcSyncHandler_v2.touchNewFile(user, requestId, fileName, parent)
        return response
    
    def __generateDateTime(self):   
        delta = int(round(time.time() * 1000))
        return delta
    
    def __getRequestId(self):
        requestId = "Api-web_" + str(self.__generateDateTime())   
        return requestId