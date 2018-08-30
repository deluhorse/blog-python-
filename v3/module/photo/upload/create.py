# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 18/5/5 18:27
"""
import tornado.gen

from base.base import Base


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        # print self.request.files
        # print self.request.headers
        # params['files'] = self.request.files['file']
        # params['need_chunk_decode'] = self.request.headers._dict.get('Transfer-Encoding', '')
        result = yield self.do_service('photo.upload.service', 'upload_file', params)
        self.out(result)
