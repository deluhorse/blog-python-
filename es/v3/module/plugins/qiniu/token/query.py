# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 18/5/7 14:04
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def get(self):
        params = self.params()
        res = yield self.do_service('plugins.qiniu.token.service', 'create_token', params=params)
        self.out(res)
