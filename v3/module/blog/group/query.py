# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 18/9/11 15:46
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (('need',), False)

    @tornado.gen.coroutine
    def get(self):
        params = self.params()
        params['user_id'] = self.user_data['user_id']
        res = yield self.do_service('blog.group.service', 'query_group', params=params)
        self.out(res)
