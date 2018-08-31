# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 18/8/31 14:11
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        res = yield self.do_service('blog.comments.service', 'create_comments', params=params)
        self.out(res)
