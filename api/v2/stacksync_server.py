import xmlrpclib

class StacksyncServerController():
    """
    Handles requests on objects
    """
    def __init__(self, serverIp, serverPort, **kwargs):
        
        #Create Sync server connection
        self.xml_ip = serverIp
        self.xml = serverPort
        self.rpc_server = xmlrpclib.ServerProxy("http://"+serverIp+':'+str(serverPort))


    def get_metadata(self, user, file_id, include_chunks, version):
        #TODO: chunks, version value = b if a > 10 else c

        version = "null" if version is None else version
        include_chunks = "false" if include_chunks is False else "true"

        response = self.rpc_server.XmlRpcSyncHandler.getMetadata(user, str(file_id), str(include_chunks),
                                                                 str(version))

        return response
    def get_versions(self, user, file_id):

        response = self.rpc_server.XmlRpcSyncHandler.getVersions(user, str(file_id))
        return response

    def get_folder_contents(self, user, folder_id, include_deleted):

        include_deleted = "true" if include_deleted is True else "false"
        folder_id = "null" if folder_id is None else folder_id

        response = self.rpc_server.XmlRpcSyncHandler.getFolderContents(str(user), str(folder_id), str(include_deleted))
        return response

    def delete_item(self, user, file_id):
        response = self.rpc_server.XmlRpcSyncHandler.deleteItem(user, str(file_id))

        return response

    def new_folder(self, user, name, parent):
        parent = "null" if parent is None else parent

        response = self.rpc_server.XmlRpcSyncHandler.newFolder(str(user), str(name), str(parent))

        return response

    def new_file(self, user, name, parent, checksum, file_size, mimetype, chunks):
        chunks = [] if chunks is None else chunks
        mimetype = "empty" if mimetype is None else mimetype
        checksum = "0" if checksum is None else checksum
        parent = "null" if parent is None else parent

        response = self.rpc_server.XmlRpcSyncHandler.newFile(user, str(name), str(parent),
                                                            str(checksum), str(file_size), str(mimetype), chunks)

        return response

    def update_data(self, user, file_id, checksum, size,  mimetype, chunk):

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
