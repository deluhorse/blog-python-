# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 18/5/7 20:33
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (('seller',), False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        res = yield self.do_service('user.user_service', 'create', params=params)
        self.out(res)
