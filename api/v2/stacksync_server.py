import xmlrpclib
import json
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
        version = "null" if version is None else version
        include_chunks = "false" if include_chunks is False else "true"
        file_id = "null" if str(file_id) == "root" else file_id

        response = self.rpc_server.XmlRpcSyncHandler.getMetadata(user, str(file_id), str(include_chunks),
                                                                 str(version))

        return response

    def get_versions(self, user, file_id):

        response = self.rpc_server.XmlRpcSyncHandler.getVersions(user, str(file_id))
        return response

    def get_folder_contents(self, user, folder_id, include_deleted):

        include_deleted = "true" if include_deleted is True else "false"
        folder_id = "null" if str(folder_id) == 'root' else folder_id

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

    def update_data(self, user, file_id, checksum, size,  mimetype, chunks):
        chunks = [] if chunks is None else chunks

        response = self.rpc_server.XmlRpcSyncHandler.updateData(user, str(file_id), str(checksum), str(size), str(mimetype), chunks)

        return response

    def update_metadata(self, user, file_id, name, parent):
        parent = "null" if parent is None else parent
        name = "null" if name is None else name

        response = self.rpc_server.XmlRpcSyncHandler.updateMetadata(user, str(file_id), str(name), str(parent))

        return response
