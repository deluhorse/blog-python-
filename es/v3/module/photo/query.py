# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 18/5/7 14:58
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def get(self):
        params = self.params()
        params['user_id'] = 'delu'
        res = yield self.do_service('photo.service', 'query_list', params=params)
        self.out(res)
