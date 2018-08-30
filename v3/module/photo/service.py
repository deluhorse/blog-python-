# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/5/7 14:58
"""
from base.service import ServiceBase
import tornado.gen


class Service(ServiceBase):
    """
    service
    """

    photo_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.photo_model = self.import_model('photo.model')

    @tornado.gen.coroutine
    def create_photo(self, params):
        """
        创建图片记录
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['user_id', 'key'], params):
            raise self._gre('PHOTO_CREATE_PARAMS_NOT_EXIST')
        result = yield self.photo_model.create_photo(params)
        if result:
            raise self._grs()
        else:
            raise self._gre('SQL_EXECUTE_ERROR')

    @tornado.gen.coroutine
    def query_list(self, params={}):
        """
        查询图片记录
        :param params: 
        :return: 
        """
        photo_result = yield self.photo_model.query_photo_list(params)
        if not photo_result:
            raise self._gre('PHOTO_NOT_FOUND')
        for photo in photo_result:
            photo['img_url'] = self.properties.get('qiniu', 'domain') + photo['img_key']
        raise self._grs(photo_result)
