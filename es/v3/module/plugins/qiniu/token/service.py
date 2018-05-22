# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/5/7 14:04
"""
from base.service import ServiceBase
import tornado.gen
from qiniu import Auth


class Service(ServiceBase):
    """
    service
    """

    @tornado.gen.coroutine
    def create_token(self, params={}):
        """
        生成七牛token
        :param params: 
        :return: 
        """
        # 构建鉴权对象
        q = Auth(self.properties.get('qiniu', 'AK'), self.properties.get('qiniu', 'SK'))
        # 要上传的空间
        bucket_name = self.properties.get('qiniu', 'bucket_name')
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, expires=7200)

        result = self._e('SUCCESS')
        result['upDomain'] = bucket_name
        result['uptoken'] = token
        raise self._gr(result)
