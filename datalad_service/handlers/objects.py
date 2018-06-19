import logging
import os
import hashlib
import struct
import zlib

import falcon

import git
from datalad_service.common.annex import get_from_header
from datalad_service.common.celery import dataset_queue
from datalad_service.tasks.files import unlock_files, commit_files, get_files, remove_files


class ObjectsResource(object):
    _CHUNK_SIZE_BYTES = 4096

    def __init__(self, store):
        self.store = store
        self.logger = logging.getLogger('datalad_service.' + __name__)

    def annex_key_to_path(self, annex_key):
        word = struct.unpack('<I', hashlib.md5(annex_key).digest()[:4])[0]
        integer_encoding = [word >> (6 * x) & 31 for x in range(4)]
        values = ['0123456789zqjxkmvwgpfZQJXKMVWGPF'[x] for x in integer_encoding]
        return '{}{}/{}{}'.format(values[1], values[0], values[3], values[2])

    @property
    def annex_path(self):
        return self.store.annex_path

    def on_get(self, req, resp, dataset, filekey=None):
        ds_path = self.store.get_dataset_path(dataset)
        ds = self.store.get_dataset(dataset)
        if filekey:
            try:
                if filekey.startswith('MD5E'):
                    filepath = '.git/annex/objects/{}/{}/{}'.format(self.annex_key_to_path(filekey), filekey, filekey)
                    path = '{}/{}'.format(ds_path, filepath)
                    fd = open(path, 'rb')
                    resp.stream = fd
                    resp.stream_len = os.fstat(fd.fileno()).st_size
                    resp.status = falcon.HTTP_OK
                else:
                    dir = filekey[:2]
                    remaining_hex = filekey[2:]
                    filepath = '.git/objects/{}/{}'.format(dir, remaining_hex)
                    path = '{}/{}'.format(ds_path, filepath)
                    compressed_contents = open(path, 'rb').read()
                    contents = zlib.decompress(compressed_contents)
                    resp.body = contents
                    resp.status = falcon.HTTP_OK
            except git.exc.GitCommandError:
                # File is not present in tree
                resp.media = {'error': 'file not found in git tree'}
                resp.status = falcon.HTTP_NOT_FOUND
            except IOError:
                # File is not kept locally
                resp.media = {'error': 'file not found'}
                resp.status = falcon.HTTP_NOT_FOUND
            except:
                # Some unknown error
                resp.media = {
                    'error': 'an unknown error occurred accessing this file'}
                resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
                self.logger.exception(
                    'An unknown error processing file with key "{}"'.format(filekey))
        else:
            # Filekey was not provided
            resp.media = {'error': 'no file key was provided'}
            resp.status = falcon.HTTP_NOT_FOUND