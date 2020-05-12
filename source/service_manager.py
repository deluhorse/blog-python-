# -*- coding:utf-8 -*-

"""
@author: delu
@file: service_manager.py
@time: 17/4/18 下午5:21
service 服务模块
"""
import importlib

from source.redisbase import RedisBase
from tools.httputils import HttpUtils

redis = RedisBase()
redis_conn = redis.get_conn()


class ServiceManager(object):

    @staticmethod
    def do_local_service(service_path, method, params={}, version=''):
        """
        执行本地服务
        :param service_path: 
        :param method: 
        :param params: 
        :param version: 
        :return: 
        """
        model = importlib.import_module(version + '.module.' + service_path)
        service = model.Service()
        func = getattr(service, method)

        result = func(params)
        return result

    @staticmethod
    def do_remote_service(url, params, http_type='get'):
        """
        执行远程服务
        :param url: 
        :param params: 
        :return: 
        """
        try:
            if http_type == 'post':
                # 发送post请求
                HttpUtils.do_post(url, params)
            else:
                # 发送get请求
                HttpUtils.do_get(url, params)
        except Exception as e:
            # return SystemConstants.REMOTE_SERVICE_ERROR
            pass

    @staticmethod
    def do_service(service_path='', method='', params={}, version=''):
        """
        执行服务
        :param service_path: 
        :param method: 
        :param params: 
        :param version: 
        :return: 
        """
        return ServiceManager.do_local_service(service_path, method, params, version)
