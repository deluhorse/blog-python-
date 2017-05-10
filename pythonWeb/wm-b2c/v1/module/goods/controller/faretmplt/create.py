# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 17/5/10 上午10:49
"""
from base.base import Base


class Controller(Base):
    auth = (('admin',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'faretmplt_name': self.params('faretmplt_name'),
            'fare_list': self.json.loads(self.params('fare_list')),
            'admin_id': self.user_data['admin_id']
        }
        res = self.do_service('goods.service.faretmplt.faretmplt_service', 'create', params=params)
        self.out(res)
