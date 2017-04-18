# -*- coding:utf-8 -*-

"""
@author: delu
@file: service_manager.py
@time: 17/4/18 下午5:21
service 服务模块
"""
import importlib
from properties import properties


class ServiceManager(object):

    @staticmethod
    def do_localservice(service_path, method, params={}, version=''):
        """
        执行本地服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        model = importlib.import_module(properties.get('base', 'VERSION') + '.service.' + service_path)

        func = getattr(model.Service(), method)

        return func(params)

    @staticmethod
    def do_remoteservice(url, params):
        """
        执行远程服务
        :param url: 
        :param params: 
        :return: 
        """
        pass

    @staticmethod
    def do_service(service_path='', method='', url='', params={}, version=''):
        """
        执行服务
        :param service_path: 
        :param method: 
        :param url: 
        :param params: 
        :return: 
        """
        if True:
            ServiceManager.do_localservice(service_path, method, params, version)
        else:
            ServiceManager.do_remoteservice(url, params)
