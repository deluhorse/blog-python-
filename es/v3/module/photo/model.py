# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/5/7 20:18
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def create_photo(self, params):
        """
        创建图片库记录
        """
        try:
            cfg_photo_key = 'host_type, img_key'
            cfg_photo_value_tuple = (params['host'], params['key'])
            cfg_photo = yield self.insert('tbl_cfg_photo', {self.sql_constants.KEY: cfg_photo_key},
                                          cfg_photo_value_tuple, auto_commit=False)
            if not cfg_photo:
                raise self._gr(False)
            user_photo_key = 'user_id, photo_id'
            user_photo_value_tuple = (params['user_id'], cfg_photo['last_id'])
            yield self.insert('tbl_um_photo', {self.sql_constants.KEY: user_photo_key},
                              user_photo_value_tuple, auto_commit=False)
            yield self.tx.commit()
        except Exception:
            yield self.tx.rollback()
            raise self._gr(False)
        raise self._gr(True)

    @tornado.gen.coroutine
    def query_photo_list(self, params):
        """
        查询图片列表
        :param params: 
        :return: 
        """
        fields = [
            'user_photo.*',
            'cfg_photo.host_type',
            'cfg_photo.img_key'
        ]
        condition = ' cfg_photo.img_key is not null '
        value_list = []

        join = [{self.sql_constants.TABLE_NAME: 'tbl_cfg_photo as cfg_photo',
                 self.sql_constants.JOIN_CONDITION: ' user_photo.photo_id = cfg_photo.photo_id '}]
        if 'user_photo.user_id' in params and params['user_id']:
            condition += ' and user_photo.user_id = %s '
            value_list.append(params['user_id'])
        result = yield self.find('tbl_um_photo as user_photo', {self.sql_constants.CONDITION: condition,
                                                                self.sql_constants.FIELDS: fields,
                                                                self.sql_constants.JOIN: join},
                                 tuple(value_list),
                                 self.sql_constants.LIST)
        raise self._gr(result)
