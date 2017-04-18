# -*- coding:utf-8 -*-

"""
@author: delu
@file: short_message_service.py
@time: 17/4/16 上午11:16
"""
from service.service import ServiceBase


class Service(ServiceBase):
    """
    short_message_service
    """

    user_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        # self.user_model = self.import_model('user.user_model')
        pass

    def send_vertify_code(self, mobile_no=''):
        """
        发送短信验证码
        :param mobile_no: 
        :return: 
        """
        pass

