# -*- coding:utf-8 -*-

"""
@author: delu
@file: test_base.py
@time: 17/5/5 下午5:37
"""
from tools.httputils import HttpUtils
class TestBase(object):

    base_api = 'http://localhost:9000/api/v1/'

    def do_service(self, module_name, params, http_type):
        """
        :param module_name: 
        :param params: 
        :return: 
        """
        try:
            url = '%s%s' % (self.base_api, module_name.replace('.', '/'))
            if cmp(http_type, 'post') == 0:
                # 发送post请求
                return HttpUtils.do_post(url, params)
            else:
                # 发送get请求
                return HttpUtils.do_get(url, params)
        except Exception, e:
            print Exception, ':', e
