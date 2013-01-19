#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com
import logging
import importlib

from thumbor.storages import BaseStorage

class Storage(BaseStorage):
    """Uses each storage option, in order"""

    def __init__(self, context):
        BaseStorage.__init__(self, context)

        self.storages = []
        for modpath in context.config.FAILOVER_STORAGE_OPTIONS:
            logging.debug("importing " + modpath)
            mod = importlib.import_module(modpath)
            self.storages.append(mod.Storage(context))

    def put(self, path, bytes):
        for s in self.storages:
            s.put(path, bytes)
        return path

    def put_crypto(self, path):
        for s in self.storages:
            s.put_crypto(path)
        return path

    def put_detector_data(self, path, data):
        for s in self.storages:
            s.put_detector_data(path, path, data)
        return path

    def get_crypto(self, path):
        for i, s in enumerate(self.storages):
            result = s.get_crypto(path)
            if result:
                for s2 in self.storages[0:i]:
                    s2.put_crypto(path)
                return result
        return None

    def get_detector_data(self, path):
        for i, s in enumerate(self.storages):
            result = s.get_detector_data(path)
            if result:
                for s2 in self.storages[0:i]:
                    s2.put_detector_data(path, result)
                return result
        return None

    def get(self, path):
        for i, s in enumerate(self.storages):
            result = s.get(path)
            if result:
                for s2 in self.storages[0:i]:
                    s2.put_detector_data(path, result)
                return result
        return None

    def exists(self, path):
        for s in self.storages:
            result = s.exists(path)
            if result:
                return True
        return False

    def remove(self, path):
        for s in self.storages:
            s.remove(path)
