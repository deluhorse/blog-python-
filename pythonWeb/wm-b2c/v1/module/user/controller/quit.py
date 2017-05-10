# -*- coding:utf-8 -*-

"""
@author: delu
@file: quit.py
@time: 17/4/19 下午6:13
管理员退出登录
"""
from v1.base.base import Base


class Controller(Base):

    auth = (('admin', 'seller'), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):

        self.delete_token()

        self.out(self._e('SUCCESS'))

