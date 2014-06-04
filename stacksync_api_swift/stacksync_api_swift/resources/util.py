from webob import Request, Response
import StringIO, zlib
from cStringIO import StringIO as strIO
from gzip import GzipFile
from hashlib import sha1
from time import time

CHUNK_SIZE = 524288

class Chunk(object):
    def __init__(self, checksum):
        #self.checksum = str(long(checkSum)).rjust(20, '0').upper()
        self.checksum = checksum.upper()

    def getFileName(self):
        return "chk-" + self.checksum



class BuildFile(object):
    #chunks are the content chunks
    #listNames are the list of chunks names
    def __init__(self, content, chunks):
        self.listNames = []
        self.hashesList = []
        self.content = content
        self.chunks = chunks

    def join(self):
        self.content = ""
        for chunk in self.chunks:
            f = GzipFile('', 'rb', 9, StringIO.StringIO(chunk))
            temp = f.read()
            f.close()

            self.content += temp
    def adlerHash(self, data):
        return (zlib.adler32(data) & 0xffffffff)

    def sha1Hash(self, data):
        shaHash = sha1()
        shaHash.update(data)
        result = shaHash.hexdigest()
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
            buf = strIO()
            f = GzipFile(mode='wb', fileobj=buf)
            try:
                f.write(data)
            finally:
                f.close()
            chunk = buf.getvalue()

            self.chunks.append(chunk)
