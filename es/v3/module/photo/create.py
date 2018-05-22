# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 18/5/7 14:58
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        params['user_id'] = 'delu'
        res = yield self.do_service('photo.service', 'create_photo', params=params)
        self.out(res)
