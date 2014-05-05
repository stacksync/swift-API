import xmlrpclib


class StacksyncServerController():
    """
    Handles requests on objects
    """
    def __init__(self, serverIp, serverPort, **kwargs):
        
        #Create Sync server connection
        self.request_id = 123
        self.xml_ip = serverIp
        self.xml = serverPort
        self.rpc_server = xmlrpclib.ServerProxy("http://"+serverIp+':'+str(serverPort))


    def get_metadata(self, user, file_id, include_chunks, version, include_list, include_deleted):
        #TODO: chunks, version value = b if a > 10 else c

        version = "null" if version is None else version
        include_chunks = "false" if include_chunks is False else "true"
        include_list = "true" if include_list is True else "false"
        include_deleted = "true" if include_deleted is True else "false"

        response = self.rpc_server.XmlRpcSyncHandler.getMetadata(str(user), str(file_id), str(include_list),
                                                                 str(include_deleted), str(include_chunks),
                                                                 str(version))

        return response
    def get_versions(self, user, file_id):

        response = self.rpcServer.XmlRpcSyncHandler.getVersions(str(user), str(file_id))
        return response

    def get_folder_contents(self, user, folder_id, include_deleted):

        include_deleted = "true" if include_deleted is True else "false"

        response = self.rpc_server.XmlRpcSyncHandler.getMetadata(str(user), str(folder_id), "true", str(include_deleted)
                                                                 , "null", "null")
        return response
        #TODO: user item in documentation doesn't exist
        # response ={
        #            "name":"clients",
        #            "path":"/documents/clients",
        #            "id":9873615,
        #            "status":"NEW",
        #            "version":1,
        #            "parent":-348534824681,
        #            "user":"Adrian",
        #            "client_modified":"2013-03-08 10:36:41.997",
        #            "server_modified":"2013-03-08 10:36:41.997",
        #            "contents":[{
        #                         "name":"Client1.pdf",
        #                         "path":"/documents/clients/Client1.pdf",
        #                         "id":32565632156,
        #                         "size":775412,
        #                         "mimetype":"application/pdf",
        #                         "status":"DELETED",
        #                         "version":3,
        #                         "parent":-348534824681,
        #                         "user":"Adrian",
        #                         "client_modified":"2013-03-08 10:36:41.997",
        #                         "server_modified":"2013-03-08 10:36:41.997"
        #                         },
        #                        {
        #                         "name":"Client1.pdf",
        #                         "path":"/documents/clients/Client1.pdf",
        #                         "id":32565632156,
        #                         "size":775412,
        #                         "mimetype":"application/pdf",
        #                         "status":"DELETED",
        #                         "version":3,
        #                         "parent":-348534824681,
        #                         "user":"Adrian",
        #                         "client_modified":"2013-03-08 10:36:41.997",
        #                         "server_modified":"2013-03-08 10:36:41.997"
        #                         }
        #                        ]
        #            }
        #
        # return response

    def delete_item(self, user, file_id):
        response = self.rpcServer.XmlRpcSyncHandler.deleteMetadataFile(user, file_id)

        return response

    def new_folder(self, user, name, parent):
        response = self.rpcServer.XmlRpcSyncHandler.putMetadataFolder(str(user), str(name), str(parent))

        return response

    def new_file(self, user, name, parent):
        response = self.rpcServer.XmlRpcSyncHandler.putMetadataFile(str(user), str(name), str(parent), overwrite,
                                                                    checksum, fileSize, mimetype, chunks)

        return response

    def update_data(self, user, file_id, mimetype, size, chunk):

        """When u update the data content, it's necessary to create a new file version metadata
         to guarantee the version control. Using old methods, we will use the method new_file, to implement
         this requirement"""
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
