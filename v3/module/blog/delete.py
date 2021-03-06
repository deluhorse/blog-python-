# -*- coding:utf-8 -*-

"""
@author: delu
@file: delete.py
@time: 18/8/30 11:27
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (('need',), False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        params['user_id'] = self.user_data['user_id']
        res = yield self.do_service('blog.service', 'delete_blog', params=params)
        self.out(res)
