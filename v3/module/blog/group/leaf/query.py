# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 18/9/13 09:59
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (('need',), False)

    @tornado.gen.coroutine
    def get(self):
        params = self.params()
        params['user_id'] = self.user_data['user_id']
        res = yield self.do_service('blog.group.leaf.service', 'query_leafs', params=params)
        self.out(res)
