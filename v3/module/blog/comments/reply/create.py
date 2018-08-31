# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 18/8/31 14:31
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        res = yield self.do_service('blog.comments.reply.service', 'create_reply', params=params)
        self.out(res)
