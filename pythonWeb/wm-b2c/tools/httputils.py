# -*- coding:utf-8 -*-

"""
@author: delu
@file: httputils.py
@time: 17/5/2 上午10:36
"""
import urllib
import urllib2
import json
from tools.date_json_encoder import CJsonEncoder

class HttpUtils(object):

    @staticmethod
    def do_get(url, params={}):
        """
        发送get请求
        :param url: 
        :param params: 
        :return: 
        """
        print '发送请求 url: %s, params: %s' % (url, json.dumps(params, cls=CJsonEncoder))
        url_params = '?'
        if len(params) > 0:
            for key in params:
                url_params += '%s=%s&' % (key, params[key])
            url += url_params + 'x=1'
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print '请求结果 %s' % res
        return res

    @staticmethod
    def do_post(url, params={}, headers={}):
        """
        发送post请求
        :param url: 
        :param params: 
        :return: 
        """
        print '发送请求 url: %s, params: %s' % (url, json.dumps(params, cls=CJsonEncoder))
        params_urlencode = urllib.urlencode(params)
        if headers:
            req = urllib2.Request(url=url, data=json.dumps(params), headers=headers)
        else:
            req = urllib2.Request(url=url, data=params_urlencode)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print '请求结果 %s' % res
        return res
