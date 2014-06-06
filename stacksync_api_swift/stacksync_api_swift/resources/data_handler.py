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
        for i in range(len(chunked_file.chunks)):
            chunk_name = chunked_file.listNames[i - 1]
            chunk_content = chunked_file.chunks[i - 1]

            env_aux = env.copy()
            new_path = "/v1/" + env['stacksync_user_account'] + "/" + container + "/" + chunk_name
            env_aux['SCRIPT_NAME'] = ""
            del env_aux['HTTP_STACKSYNC_API']
            seg_req = make_pre_authed_request(env_aux, method='PUT', path=new_path, body=chunk_content,
                                              agent='%(orig)s')

            seg_resp = seg_req.get_response(self.app)

            if not is_valid_status(seg_resp.status_int):
                self.app.logger.error('StackSync API: upload_file_chunks: error uploading chunk %s', chunk_name)
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
        for chunk in chunks:
            file_chunk = "chk-" + str(chunk)

            new_path = "/v1/" + env['stacksync_user_account'] + "/" + container + "/" + file_chunk
            seg_req = make_pre_authed_request(env, method='GET', path=new_path, body="", agent='%(orig)s')
            seg_resp = seg_req.get_response(self.app)

            if is_valid_status(seg_resp.status_int):
                file_compress_content.append(seg_resp.body)
            else:
                file_compress_content = []
                break

        return file_compress_content, seg_resp.status_int

