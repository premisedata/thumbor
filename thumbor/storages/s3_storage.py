#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com
import hashlib

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from thumbor.storages import BaseStorage

class Storage(BaseStorage):
    """Uses Amazon S3 for storage"""

    def __init__(self, context):
        BaseStorage.__init__(self, context)

        access_key = context.config.S3_ACCESS_KEY_ID
        secret_key = context.config.S3_SECRET_ACCESS_KEY
        bucket = context.config.S3_BUCKET
        if access_key and secret_key:
            self.s3 = S3Connection(access_key, secret_key).create_bucket(bucket)
        else:
            # key passed in implicitly via AWS_ACCESS_KEY_ID and
            # AWS_SECRET_ACCESS_KEY environment variables
            self.s3 = S3Connection().create_bucket(bucket)

    def put(self, path, bytes):
        k = Key(self.s3)
        k.key = path

        try:
            k.set_contents_from_string(bytes)
            return path
        except:
            return None

    def put_crypto(self, path):
        return path

    def put_detector_data(self, path, data):
        return path

    def get(self, path):
        k = Key(self.s3)
        k.key = path

        try:
            return s3.get_contents_from_string(bytes)
        except:
            return None

    def get_crypto(self, path):
        return None

    def get_detector_data(self, path):
        return None

    def remove(self, path):
        k = Key(self.s3)
        k.key = path
        self.s3.delete_key(k)

    def exists(self, path):
        k = Key(self.s3)
        k.key = path
        return k.exists()
