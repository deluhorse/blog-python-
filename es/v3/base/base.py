#!usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.gen
import json

import conf.config as config
import random
from source.controller import Controller
from source.service_manager import ServiceManager as serviceManager
from tools.date_json_encoder import CJsonEncoder
from constants.error_code import Code
from source.redisbase import RedisBase


class Base(Controller):

    json = json
    error_code = Code
    redis = RedisBase()
    user_data = {}
    auth = None
    _params = {}

    @tornado.gen.coroutine
    def prepare(self):
        if self.auth:
            if self.auth[0] is not None:
                # 如果控制器需要登录, 则进行登录检查
                token = self.get_cookie('token')
                self.user_data = self.redis.hgetall(token)
                if not self.user_data:
                    self.error_out(self._e('NOT_LOGIN'))
                    self.finish()

    def out(self, data):
        """ 
        输出结果
        :param data: 返回数据字典
        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self.json.dumps(data, cls=CJsonEncoder))

    def error_out(self, error, data=''):
        """
        错误输出
        :param error: 错误信息对象
        :param data: 返回数据字典
        :return: 
        """
        out = error
        if data:
            out['data'] = data

        self.write(out)

    def create_token(self, params):
        """
        登录成功, 写token
        :param params: 
        :return: 
        """
        token = self.salt()
        self.redis.hmset(token, params)
        self.set_cookie('token', token)

    def salt(self, salt_len=6, is_num=False):
        """ 
        密码加密字符串
        生成一个固定位数的随机字符串，包含0-9a-z
        @:param salt_len 生成字符串长度
        """

        if is_num:
            chrset = '0123456789'
        else:
            chrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        salt = []
        for i in range(salt_len):
            item = random.choice(chrset)
            salt.append(item)

        return ''.join(salt)

    @tornado.gen.coroutine
    def get(self):
        """
        重写父类get方法，接受GET请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'))

    @tornado.gen.coroutine
    def post(self):
        """
        重写父类post方法，接受POST请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'))

    def _e(self, code):
        """
        返回错误码
        :param code: 
        :return: 
        """
        return self.error_code[code]

    def _gre(self, data):
        """
        tornado.gen.Return
        :param data: 数据
        :return: 
        """
        return tornado.gen.Return(self._e(data))

    def do_service(self, service_path, method, params={}):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        return serviceManager.do_service(service_path, method, params=params, version=config.CONF['version'])

    def params(self, key=''):
        """
        获取参数中指定key的数据
        :param key:
        :return:
        """
        if not key:
            return self.get_params()
        elif key not in self.get_params():
            return ''
        else:
            return self.get_params(key)
