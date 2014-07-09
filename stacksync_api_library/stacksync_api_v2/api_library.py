from stacksync_api_v2.server_factory import ServerControllerFactory


class StackSyncApi(object):

    def __init__(self, server_type, host='127.0.0.1', port=61234):
        self.server = ServerControllerFactory().get_server(server_type, host, port)

    def get_metadata(self, user_id, file_id, include_chunks=False, specific_version=None, is_folder=False):
        results = self.server.get_metadata(user_id, file_id, include_chunks, specific_version, is_folder)
        return results

    def get_folder_contents(self, user_id, folder_id, include_deleted=True):
        results = self.server.get_folder_contents(user_id, folder_id, include_deleted)
        return results

    def get_versions(self, user, file_id):
        message = self.server.get_versions(user, file_id)
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

    def delete_item(self, user_id,  file_id, is_folder=False):
        message = self.server.delete_item(user_id, file_id, is_folder)
        return message

    def put_metadata(self, user_id, file_id, name=None, parent=None):
        if not name and not parent:
            return "{'error':404,'description':'BadRequest: Nothing to update'}"
        message = self.server.update_metadata(user_id, file_id, name, parent)
        return message

    def get_workspace_info(self, user_id, item_id):
        message = self.server.get_workspace_info(user_id, item_id)
        return message

    def share_folder(self, user_id, folder_id, users_list):
        message = self.server.share_folder(user_id, folder_id, users_list)
        return message

    def unshare_folder(self, user_id, folder_id, users_list):
        message = self.server.unshare_folder(user_id, folder_id, users_list)
        return message

    def get_folder_members(self, user_id, folder_id):
        message = self.server.get_folder_members(user_id, folder_id)
        return message