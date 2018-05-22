# -*- coding:utf-8 -*-

"""
@author: delu
@file: model_manager.py
@time: 18/5/5 15:17
"""
import importlib

from source.redisbase import RedisBase
from system_constants import SystemConstants
from tools.httputils import HttpUtils

redis = RedisBase()
redis_conn = redis.get_conn()


class ModelManager(object):

    @staticmethod
    def do_local_model(model_path, method, params={}, version=''):
        """
        执行本地服务
        :param model_path: 
        :param method: 
        :param params: 
        :param version: 
        :return: 
        """
        model = importlib.import_module(version + '.module.' + model_path)
        my_model = model.Model()
        func = getattr(my_model, method)
        result = func(params)
        return result

    @staticmethod
    def do_remote_model(url, params, http_type='get'):
        """
        执行远程服务
        :param url: 
        :param params: 
        :return: 
        """
        try:
            if cmp(http_type, 'post') == 0:
                # 发送post请求
                HttpUtils.do_post(url, params)
            else:
                # 发送get请求
                HttpUtils.do_get(url, params)
        except Exception, e:
            print Exception, ':', e
            return SystemConstants.REMOTE_SERVICE_ERROR

    @staticmethod
    def do_model(model_path='', method='', params={}, version=''):
        """
        执行服务
        :param model_path: 
        :param method: 
        :param params: 
        :param version: 
        :return: 
        """
        return ModelManager.do_local_model(model_path, method, params, version)
