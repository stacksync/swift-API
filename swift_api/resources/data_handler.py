__author__ = 'edgar'

from webob import Request, Response
from swift_server.util import create_error_response
from swift.common.swob import HTTPCreated, HTTPUnauthorized, HTTPBadRequest

class DataHandler(object):

    def __init__(self, app):
        self.app = app
        self.response_args = []

    def do_start_response(self, *args):
        self.response_args.extend(args)

    def upload_file_chunks(self, env, url_base, script_name, separate_file):
        error = False
        for i in range(len(separate_file.chunks)):
            chunk_name = separate_file.listNames[i-1]
            chunk_content = separate_file.chunks[i-1]
            '''Revisar aquesta part!!! Handoff requested'''
            env['PATH_INFO'] = url_base + "/AUTH_5e446d39e4294b57831da7ce3dd0d2c2/edgar/" + chunk_name
            env['SCRIPT_NAME'] = script_name

            req = Request(env)
            req.body = chunk_content
            req.content_length = len(chunk_content)

            self.app(req.environ, self.do_start_response)
            status = int(self.response_args[0].split()[0])

            if 200 > status >= 300:
                break

        if(error):
            response = create_error_response(500, "Internal Server Error")
        else:
            response = HTTPCreated(body="OK")

        return response

    def __get_file(self, env):
        self.response_args = []

        app_iterFile = self.app(env, self.do_start_response)
        status_file  = int(self.response_args[0].split()[0])
        headers_file  = dict(self.response_args[1])
        if 200 <= status_file < 300:
            new_headers_file = {}
            for key, val in headers_file.iteritems():
                _key = key.lower()
                if _key.startswith('x-object-meta-'):
                    new_headers_file['x-amz-meta-' + key[14:]] = val
                elif _key in ('content-length', 'content-type', 'content-encoding', 'etag', 'last-modified'):
                    new_headers_file[key] = val

            response_file = Response(status=status_file, headers=new_headers_file, app_iter=app_iterFile)
        elif status_file == 401:
            response_file = HTTPUnauthorized()
        else:
            response_file = HTTPBadRequest()

        return response_file

    def get_chunks(self, env, url_base, script_name, chunks):
        file_compress_content = []
        status_file = 200
        for chunk in chunks:
            file_chunk = "chk-" + str(chunk)

            env['PATH_INFO'] = url_base + '/AUTH_5e446d39e4294b57831da7ce3dd0d2c2/edgar/' + file_chunk
            env['SCRIPT_NAME'] = script_name

            response_file = self.__get_file(env)
            status_file = response_file.status_int
            if 200 <= status_file < 300:
                file_compress_content.append(response_file.body)
            else:
                file_compress_content = []
                break

        return file_compress_content, status_file