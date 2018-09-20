# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/5/6 14:21
"""
import os

import tornado.gen

from base.service import ServiceBase


class Service(ServiceBase):
    """
    service
    """
    file_path = '/opt/delu/'

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        pass

    @tornado.gen.coroutine
    def upload_file(self, params={}):
        """
        保存文件至本地
        :param params: 
        :return: 
        """
        # 对文件进行64解码
        for file_item in params['files']:
            file_name = file_item['filename']
            file_key = self.md5(self.create_uuid())
            temp_file_path = self.file_path + file_key
            body = file_item['body']
            if params['need_chunk_decode']:
                body = self.common_utils.decode_chunked(body)
            with open(temp_file_path, 'wb') as f:
                f.write(body)

            result = yield self.do_service('plugins.qiniu.service', 'upload_file', {
                'key': file_key,
                'file_path': temp_file_path
            })
            # 删除临时文件
            os.remove(temp_file_path)

            result = yield self.do_service(
                'photo.service',
                'create_photo',
                {
                    'user_id': params['user_id'],
                    'nick_name': file_name,
                    'key': file_key,
                    'host': 1
                }
            )

        raise self._grs()

if __name__ == '__main__':
    content = ''
    with open('/opt/delu/test.jpg', 'rb') as f:
        content = f.read()

    with open('/opt/delu/testx.jpg', 'wb') as f:
        f.write(content)
