# -*- coding:utf-8 -*-

"""
@author: delu
@file: update.py
@time: 18/8/31 14:06
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        res = yield self.do_service('blog.read_nums.service', 'update_read_nums', params=params)
        self.out(res)
