# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/5/14 11:49
"""
from base.service import ServiceBase
import tornado.gen


class Service(ServiceBase):
    """
    service
    """

    blog_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.blog_model = self.import_model('blog.model')

    @tornado.gen.coroutine
    def query_blog(self, params={}):
        """
        查询博客记录
        :param params: 
        :return: 
        """
        result = yield self.do_model('blog.model', 'query_blog', params)
        if not result:
            raise self._gre('BLOG_NOT_FOUND')
        # 查询用户信息, 获取昵称
        user_result = yield self.do_service('user.service', 'query_user', params)
        if user_result['code'] != 0:
            raise self._gr(user_result)
        for blog in result:
            blog['create_time'] = self.date_utils.time_to_str(blog['create_time'])
        result = {
            'blog_list': result,
            'user_info': user_result['data']
        }
        raise self._grs(result)

    @tornado.gen.coroutine
    def create_blog(self, params):
        """
        创建博客记录
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['user_id', 'title', 'content'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        result = yield self.do_model('blog.model', 'create_blog', params)
        if not result:
            raise self._gre('SQL_EXECUTE_ERROR')
        raise self._grs()