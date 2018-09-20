# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 18/5/5 18:27
"""
import tornado.gen

from base.base import Base


class Controller(Base):
    auth = ('need', False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        params['user_id'] = self.user_data['user_id']
        params['need_chunk_decode'] = self.request.headers._dict.get('Transfer-Encoding', '')
        params['files'] = self.request.files['file']
        result = yield self.do_service('photo.upload.service', 'upload_file', params)
        self.out(result)
