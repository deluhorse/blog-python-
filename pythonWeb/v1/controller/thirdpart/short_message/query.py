# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 17/4/16 上午11:07
"""
from controller.base import Base


class Controller(Base):
    queryService = None
    short_message_service = None

    def initialize(self):
        Base.initialize(self)
        # self.queryService = self.import_service('queryService')
        self.short_message_service = self.import_service('thirdpart.short_message.short_message_service')

    def index(self):
        """
        生成验证码并发送验证码
        :return: 
        """
        params = eval(self.params('para'))
        mobile_no = params['mobile_no']
        vertify_code = self.salt(is_num=True)
        self.redis.set(mobile_no, vertify_code, ex=30 * 60)

        # 调短信服务发送验证码
        self.short_message_service.send_vertify_code(mobile_no)
