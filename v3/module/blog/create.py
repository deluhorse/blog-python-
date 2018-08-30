# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 18/5/15 22:13
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = ('need', False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        params['user_id'] = self.user_data['user_id']
        res = yield self.do_service('blog.service', 'create_blog', params=params)
        self.out(res)
