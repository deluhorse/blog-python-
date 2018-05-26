# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 18/5/14 11:49
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (('need',), False)

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def get(self):
        params = self.params()
        params['user_id'] = self.user_data['user_id']
        res = yield self.do_service('blog.service', 'query_blog', params=params)
        self.out(res)
