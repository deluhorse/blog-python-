# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 18/8/31 19:11
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def get(self):
        params = self.params()
        res = yield self.do_service('blog.comments.service', 'query_blog_comment_list', params=params)
        self.out(res)
