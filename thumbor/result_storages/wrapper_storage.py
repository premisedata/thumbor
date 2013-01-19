#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com
import importlib
import logging

from thumbor.storages import BaseStorage


class Storage(BaseStorage):

    def __init__(self, context):
        BaseStorage.__init__(self, context)
        mod = importlib.import_module(context.config.WRAPPER_RESULT_STORAGE)
        self.storage = mod.Storage(context)
        logging.debug('Instantiated Wrapper Result Storage')

    def put(self, bytes):
        logging.debug('Storing with Wrapper Result Storage')
        return self.storage.put(self.path(self.context.request.url), bytes)

    def get(self):
        logging.debug('Retrieving with Wrapper Result Storage')
        return self.storage.get(self.path(self.context.request.url))

    def path(self, url):
        return "rs-" + url
