# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_login.py
@time: 17/4/16 上午10:25
管理员登录
"""
from v1.base.base import Base


class Controller(Base):

    user_service = None
    auth = (None, 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        """
        管理员登录
        :return: 
        """

        params = {
            'account': self.params('username'),
            'password': self.params('password')
        }

        result = self.do_service('user.service.user_service', 'login', params=params)

        if result['code'] == 0:
            # 成功后生成一个cookie和服务器token
            self.create_cookie_and_token(result['data'])

        self.out(result)
