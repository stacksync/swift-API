__author__ = 'edgar'

from webob import Request, Response
from swift_server.util import create_error_response
from swift.common.swob import HTTPCreated, HTTPUnauthorized, HTTPBadRequest
from swift.common.wsgi import make_pre_authed_request

class DataHandler(object):

    def __init__(self, app):
        self.app = app
        self.response_args = []

    def do_start_response(self, *args):
        self.response_args.extend(args)

    def upload_file_chunks(self, env, url_base, separate_file):
        error = False
        for i in range(len(separate_file.chunks)):
            chunk_name = separate_file.listNames[i-1]
            chunk_content = separate_file.chunks[i-1]
            '''Revisar aquesta part!!! Handoff requested'''
            env_aux = env.copy()
            new_path = url_base + "/AUTH_5e446d39e4294b57831da7ce3dd0d2c2/edgar/"+chunk_name
            env_aux['SCRIPT_NAME'] = "" 
            print 'new_path', new_path
            del env_aux['HTTP_STACKSYNC_API']
            seg_req = make_pre_authed_request(env_aux, method='PUT', path=new_path, body=chunk_content, agent=('%(orig)s '))


            # req = Request(env)
            # req.body = chunk_content
            # req.content_length = len(chunk_content)
            seg_resp = seg_req.get_response(self.app)
            print 'response', seg_resp.status

        if(error):
            response = create_error_response(500, "Internal Server Error")
        else:
            response = HTTPCreated(body="OK")

        return response

    def get_chunks(self, env, url_base, chunks):
        file_compress_content = []
        status_file = 200
        for chunk in chunks:
            file_chunk = "chk-" + str(chunk)
            env_aux = env.copy()

            new_path = url_base + '/AUTH_5e446d39e4294b57831da7ce3dd0d2c2/edgar/' + file_chunk
            seg_req = make_pre_authed_request(env, method='GET', path=new_path, body="", agent=('%(orig)s '))
            seg_resp = seg_req.get_response(self.app)

            if 200 <= seg_resp.status_int < 300:
                file_compress_content.append(seg_resp.body)
            else:
                file_compress_content = []
                break

        return file_compress_content, seg_resp.status_int

