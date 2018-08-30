# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/5/6 14:21
"""
import tornado.gen
import base64
from base.service import ServiceBase


class Service(ServiceBase):
    """
    service
    """
    file_path = '/opt/delu/'

    user_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.user_model = self.import_model('user.user_model')

    @tornado.gen.coroutine
    def upload_file(self, params={}):
        """
        保存文件至本地
        :param params: 
        :return: 
        """
        # 对文件进行64解码
        base64_index = params['data'].index('base64,')
        file_data = params['data'][base64_index:].replace('base64,', '')
        with open(self.file_path + params['file_name'], 'wb') as f:
            f.write(base64.b64decode(file_data))
        # for file_item in params['files']:
        #     file_name = file_item['filename']
        #     body = file_item['body']
        #     if params['need_chunk_decode']:
        #         body = self.common_utils.decode_chunked(body)
        #     with open(self.file_path + file_name, 'wb') as f:
        #         f.write(body)
        raise self._grs()

if __name__ == '__main__':
    content = ''
    with open('/opt/delu/test.jpg', 'rb') as f:
        content = f.read()

    with open('/opt/delu/testx.jpg', 'wb') as f:
        f.write(content)
