# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 17/4/24 下午2:01
"""
from v1.base.base import Base


class Controller(Base):

    auth = (('admin',), 'get')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'admin_id': self.user_data['admin_id']
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('user.service.user_service', 'query_user', params=params)

        self.out(res)
