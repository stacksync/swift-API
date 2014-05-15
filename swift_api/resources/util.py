__author__ = 'Edgar Zamora Gomez'
from webob import Request, Response

import StringIO, zlib
from cStringIO import StringIO as strIO

from gzip import GzipFile
from hashlib import sha1
from time import time

CHUNK_SIZE = 524288

def getChunks(self, env, urlBase, scriptName, chunks):
        fileCompressContent = []
        statusFile = 200
        for chunk in chunks:
            fileChunk = "chk-" + str(chunk)

            env['PATH_INFO'] = urlBase + '/' + fileChunk
            env['SCRIPT_NAME'] = scriptName

            responseFile = self.__getFile(env)
            statusFile  = responseFile.status_int
            if 200 <= statusFile  < 300:
                fileCompressContent.append(responseFile.body)
            else:
                fileCompressContent = []
                break

def getFile(self, env):
        self.response_args = []

        app_iterFile = self.app(env, self.do_start_response)
        statusFile  = int(self.response_args[0].split()[0])
        headersFile  = dict(self.response_args[1])
        if 200 <= statusFile  < 300:

            new_hdrsFile = {}
            for key, val in headersFile.iteritems():
                _key = key.lower()
                if _key.startswith('x-object-meta-'):
                    new_hdrsFile['x-amz-meta-' + key[14:]] = val
                elif _key in ('content-length', 'content-type', 'content-encoding', 'etag', 'last-modified'):
                    new_hdrsFile[key] = val

            responseFile = Response(status=statusFile, headers=new_hdrsFile, app_iter=app_iterFile)
        elif statusFile == 401:
            responseFile = 'unauthorized'
        else:
            responseFile = 'bad_request'

        return responseFile

def uploadFileChunks(self, env, urlBase, scriptName, separateFile):
        error = False
        for i in range(len(separateFile.chunks)):
            chunkName = separateFile.listNames[i-1]
            chunkContent = separateFile.chunks[i-1]

            env['PATH_INFO'] = urlBase + "/" + chunkName
            env['SCRIPT_NAME'] = scriptName

            req = Request(env)
            req.body = chunkContent
            req.content_length = len(chunkContent)

            self.app(req.environ, self.do_start_response)
            status = int(self.response_args[0].split()[0])

            if 200 > status >= 300:
                break

        if(error):
            response = 'error'
        else:
            response = 'ok'

        return response

class Chunk(object):
    def __init__(self, checksum):
        #self.checksum = str(long(checkSum)).rjust(20, '0').upper()
        self.checksum = checksum.upper()

    def getFileName(self):
        return "chk-" + self.checksum

class GzipWrap(object):
    # input is a filelike object that feeds the input
    def __init__(self, inputStream, filename = None):
        self.input = inputStream
        self.buffer = ''
        self.zipper = GzipFile(filename, mode = 'wb', fileobj = self)

    def read(self, size=-1):
        if (size < 0) or len(self.buffer) < size:
            for s in self.input:
                self.zipper.write(s)
                if size > 0 and len(self.buffer) >= size:
                    self.zipper.flush()
                    break
            else:
                self.zipper.close()
            if size < 0:
                ret = self.buffer
                self.buffer = ''
        else:
            ret, self.buffer = self.buffer[:size], self.buffer[size:]
        return ret

    def flush(self):
        pass

    def write(self, data):
        self.buffer += data

    def close(self):
        self.zipper.close()

class GzipWrap2(object):
    # input is a filelike object that feeds the input
    def __init__(self, inputStream, filename = None):
        init = time()
        self.input = inputStream
        self.buffer = ''
        self.zipper = GzipFile(filename, mode = 'wb', fileobj = self)
        end = time()
        print 'GzipWrap init', ((end - init)), ' s.'

    def read(self, size=-1):
        init = time()
        try:
            self.zipper.write(self.input)
        finally:
            self.zipper.close()
        end = time()
        print 'GzipWrap read', ((end - init)), ' s.'

        return self.buffer

    def flush(self):
        pass

    def write(self, data):
        self.buffer += data

    def close(self):
        self.zipper.close()

class BuildFile(object):
    #chunks are the content chunks
    #listNames are the list of chunks names
    def __init__(self, content, chunks):
        self.listNames = []
        self.hashesList = []
        self.content = content
        self.chunks = chunks

    def join(self):
        init = time()
        self.content = ""
        for chunk in self.chunks:
            f = GzipFile('', 'rb', 9, StringIO.StringIO(chunk))
            temp = f.read()
            f.close()

            self.content += temp
        end = time()
        print 'join process', (end - init), 's.'
    def adlerHash(self, data):
        return (zlib.adler32(data) & 0xffffffff)

    def sha1Hash(self, data):
        init = time()
        shaHash = sha1()
        shaHash.update(data)
        result = shaHash.hexdigest()
        end = time()
        print 'sha1Hash', ((end - init)), ' s.'
        return result

    def separate(self):
        numChunks = int(len(self.content)/CHUNK_SIZE)
        self.listNames = []

        if(numChunks > 0):
            lastIndex = 0
            for i in range(numChunks):
                data = self.content[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE]
                checksum = self.sha1Hash(data)
                chunkObject = Chunk(checksum)
                self.listNames.append(chunkObject.getFileName())
                self.hashesList.append(checksum.upper())
                #compress chunks process
                buf = strIO()
                f = GzipFile(mode='wb', fileobj=buf)
                try:
                    f.write(data)
                finally:
                    f.close()
                chunk = buf.getvalue()

                # with open(str(checksum), "w") as f:
                #     f.write(chunk)

                self.chunks.append(chunk)
                lastIndex = i

            data = self.content[(lastIndex+1)*CHUNK_SIZE:]
        else:
            data = self.content

        if(len(data) > 0): #controlar si data no vale nada...
            checksum = self.sha1Hash(data)
            chunkObject = Chunk(checksum)

            #nameChunk = "chunk-" + str(long(checksum)).rjust(20, '0')
            self.listNames.append(chunkObject.getFileName())
            self.hashesList.append(checksum.upper())

            f = GzipWrap(data)
            chunk = f.read()
            f.close()

            self.chunks.append(chunk)