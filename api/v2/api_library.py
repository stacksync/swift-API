'''
Created on 04/02/2014

@author: edgar
'''
import json
from server_factory import server_factory


class Api_library(object):
    def __init__(self, server_type):
        self.server = server_factory().new_server(server_type)

    def get_metadata(self, user_id, file_id, include_chunks=False, specific_version=None):
        results = self.server.get_metadata(user_id, file_id, include_chunks, specific_version)
        return results

    def get_folder_contents(self, user_id, folder_id, include_deleted=True):
        results = self.server.get_folder_contents(user_id, folder_id, include_deleted)
        return results

    def get_versions(self, user, fileId):        
        message = self.server.get_versions(user, fileId)
        return message

    def new_folder(self, user_id, name, parent=None):
        response = self.server.new_folder(user_id, name, parent)
        return response

    def new_file(self, user_id, name, parent, checksum, file_size, mimetype, chunks):
        response = self.server.new_file(user_id, name, parent, checksum, file_size, mimetype, chunks)
        return response

    def update_data(self, user, file_id, parent, mimetype, size, chunk):
        #TODO: What is chunk? list of chunks or a specific chunk
        try:
            response = self.server.update_data(user, file_id, parent, mimetype, size, chunk)
        except:
            return None
        return response
    def delete_item(self, user_id,  file_id):
        message = self.server.delete_item(user_id, file_id)
        return message
    def put_metadata(self, user_id, file_id, name=None, parent=None):
        if not name and not parent:
            return "{'error':404,'description':'BadRequest: Nothing to update'}"
        message = self.server.update_metadata(user_id, file_id, name, parent)
        return message