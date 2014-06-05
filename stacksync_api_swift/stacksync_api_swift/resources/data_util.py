import StringIO
from cStringIO import StringIO as strIO
from gzip import GzipFile
from hashlib import sha1

CHUNK_SIZE = 524288


class Chunk(object):

    def __init__(self, checksum):
        self.checksum = checksum.upper()

    def get_filename(self):
        return "chk-" + self.checksum


def get_sha1_hash(data):
    sha1_hash = sha1()
    sha1_hash.update(data)
    result = sha1_hash.hexdigest()
    return result


class BuildFile(object):

    #chunks are the content chunks
    #listNames are the list of chunks names
    def __init__(self, content, chunks):
        self.name_list = []
        self.hash_list = []
        self.content = content
        self.chunks = chunks

    def join(self):
        self.content = ""
        for chunk in self.chunks:
            f = GzipFile('', 'rb', 9, StringIO.StringIO(chunk))
            temp = f.read()
            f.close()

            self.content += temp

    def separate(self):
        num_chunks = int(len(self.content)/CHUNK_SIZE)
        self.name_list = []

        if num_chunks > 0:
            last_index = 0
            for i in range(num_chunks):
                data = self.content[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE]
                checksum = get_sha1_hash(data)
                chunk_object = Chunk(checksum)
                self.name_list.append(chunk_object.get_filename())
                self.hash_list.append(checksum.upper())
                # compress chunks process
                buf = strIO()
                f = GzipFile(mode='wb', fileobj=buf)
                try:
                    f.write(data)
                finally:
                    f.close()
                chunk = buf.getvalue()

                self.chunks.append(chunk)
                last_index = i

            data = self.content[(last_index+1)*CHUNK_SIZE:]
        else:
            data = self.content

        # FIXME: Do not repeat code, handle the last chunk differently
        if len(data) > 0:
            checksum = get_sha1_hash(data)
            chunk_object = Chunk(checksum)
            self.name_list.append(chunk_object.get_filename())
            self.hash_list.append(checksum.upper())
            buf = strIO()
            f = GzipFile(mode='wb', fileobj=buf)
            try:
                f.write(data)
            finally:
                f.close()
            chunk = buf.getvalue()

            self.chunks.append(chunk)
