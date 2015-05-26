from swift.common.swob import HTTPCreated
from swift.common.wsgi import make_pre_authed_request
from stacksync_api_swift.resources.resource_util import create_error_response, is_valid_status


class DataHandler(object):
    def __init__(self, app):
        self.app = app
        self.response_args = []

    def do_start_response(self, *args):
        self.response_args.extend(args)

    def upload_file_chunks(self, env, chunked_file, container):
        error = False
        self.app.logger.info('StackSync API: upload_file_chunks: container: %s', str(container))
        upload_chunks = []
	for k, v in chunked_file.chunk_dict.iteritems():
            chunk_name = k
            chunk_content = v[1]

            env_aux = env.copy()
            new_path = "/v1/" + env['stacksync_user_account'] + "/" + container + "/" + chunk_name
            del env_aux['HTTP_STACKSYNC_API']
            seg_req = make_pre_authed_request(env_aux, method='PUT', path=new_path, body=chunk_content,
                                              agent=str(container))

            seg_resp = seg_req.get_response(self.app)

            if not is_valid_status(seg_resp.status_int):
                self.app.logger.error('StackSync API: upload_file_chunks: error uploading chunk %s', chunk_name)
                error = True
                break
            upload_chunks.append(chunk_name)

        if error:
            self.app.logger.error(
                'StackSync API: upload_file_chunks: status: %s description: Error uploading chunks to storage backend',
                seg_resp.status)
            response = create_error_response(500, "Error uploading chunks to storage backend")
            self.remove_chunks(env, upload_chunks, container)

        else:
            response = HTTPCreated()

        return response
    def remove_old_chunks(self, env, chunks_diff, container):
        error = False
        self.app.logger.info('StackSync API: remove old chunks: container: %s', str(container))
        for chunk_name in chunks_diff:

            env_aux = env.copy()
            new_path = "/v1/" + env['stacksync_user_account'] + "/" + container + "/" + str(chunk_name)
            del env_aux['HTTP_STACKSYNC_API']
            seg_req = make_pre_authed_request(env_aux, method='DELETE', path=new_path,
                                              agent=str(container))

            seg_resp = seg_req.get_response(self.app)

            if not is_valid_status(seg_resp.status_int):
                self.app.logger.error('StackSync API: upload_file_chunks: error deleting old chunk %s', str(chunk_name))
                error = True
                break

        if error:
            self.app.logger.error(
                'StackSync API: upload_file_chunks: status: %s description: Error uploading chunks to storage backend',
                seg_resp.status)
            response = create_error_response(500, "Error uploading chunks to storage backend")
        else:
            response = HTTPCreated()

        return response

    def get_chunks(self, env, chunks, container):
        file_compress_content = []
        self.app.logger.info('StackSync API: get_chunks: chunks: %s container: %s', str(chunks), str(container))
        seg_resp = None
        for chunk in chunks:

            new_path = "/v1/" + env['stacksync_user_account'] + "/" + container + "/" + str(chunk)
            seg_req = make_pre_authed_request(env, method='GET', path=new_path, body="", agent='%(orig)s')
            seg_resp = seg_req.get_response(self.app)

            if is_valid_status(seg_resp.status_int):
                file_compress_content.append(seg_resp.body)
            else:
                file_compress_content = []
                break
        if seg_resp:
            return file_compress_content, seg_resp.status_int
        else:
            # No chunks
            return file_compress_content, 200

    def remove_chunks(self, env, chunks_names, container):
        error = False
        self.app.logger.info('StackSync API: internal remove uploaded chunks: container: %s', str(container))
        for chunk_name in chunks_names:

            env_aux = env.copy()
            new_path = "/v1/" + env['stacksync_user_account'] + "/" + container + "/" + str(chunk_name)
            del env_aux['HTTP_STACKSYNC_API']
            seg_req = make_pre_authed_request(env_aux, method='DELETE', path=new_path,
                                              agent=str(container))

            seg_resp = seg_req.get_response(self.app)

            if not is_valid_status(seg_resp.status_int):
                self.app.logger.error('StackSync API: remove_chunks: error deleting uploaded chunks %s', str(chunk_name))
                error = True
                break

        if error:
            self.app.logger.error(
                'StackSync API: upload_file_chunks: status: %s description: Error uploading chunks to storage backend',
                seg_resp.status)
            return False

        return True
