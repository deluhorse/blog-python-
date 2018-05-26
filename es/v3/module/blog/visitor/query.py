# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 18/5/27 00:49
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def get(self):
        params = self.params()
        res = yield self.do_service('blog.service', 'query_blog', params=params)
        self.out(res)
