# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_controller_test.py
@time: 17/5/5 下午5:54
"""
from test.test_base import TestBase


class UserControllerTest(TestBase):
    def login(self):
        params = {
            'username': 'delu',
            'password': '123456'
        }
        print self.do_service('user.login', params, 'post')


test = UserControllerTest()
test.login()
