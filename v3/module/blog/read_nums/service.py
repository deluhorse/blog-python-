# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/8/31 14:08
"""
from base.service import ServiceBase
import tornado.gen


class Service(ServiceBase):
    """
    service
    """

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        pass

    @tornado.gen.coroutine
    def update_read_nums(self, params={}):
        """
        更新博文阅读人数
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['blog_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        result = yield self.do_model('blog.read_nums.model', 'update_read_nums', params)
        if not result:
            raise self._gre('SQL_EXECUTE_ERROR')

        # 更新成功，返回更新后的数字
        blog_result = yield self.do_service('blog.service', 'query_blog_detail', params)
        raise self._gr(blog_result)
