# -*- coding:utf-8 -*-

"""
@author: delu
@file: update.py
@time: 17/4/24 下午2:19
"""
from v1.base.base import Base


class Controller(Base):
    auth = (('admin',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'admin_id': self.user_data['admin_id'],
            'nick_name': self.params('nick_name'),
            'mobile_no': self.params('mobile_no'),
            'qq_account': self.params('qq_account'),
            'email_address': self.params('email_address')
        }
        res = self.do_service('user.service.user_service', 'update', params=params)

        self.out(res)
