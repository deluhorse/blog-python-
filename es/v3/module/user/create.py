# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 18/5/7 20:32
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        res = yield self.do_service('user.service', 'create_user', params=params)
        self.out(res)
