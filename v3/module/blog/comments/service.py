# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/8/31 14:35
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
    def create_comments(self, params={}):
        """
        创建评论
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['blog_id', 'nick_name', 'comment_content'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        params['nick_name'] = self.common_utils.escape_html(params['nick_name'])
        params['comment_content'] = self.common_utils.escape_html(params['comment_content'])

        # 检查博文是否有效
        blog_result = yield self.do_service('blog.service', 'query_blog_detail', params)
        if blog_result['code'] != 0:
            raise self._gr(blog_result)

        result = yield self.do_model('blog.comments.model', 'create_comments', params)
        if not result:
            raise self._gre('SQL_EXECUTE_ERROR')
        raise self._grs()

    @tornado.gen.coroutine
    def query_comments_single(self, params):
        """
        查询单条评论
        :param params: 
        :return: 
        """
        result = yield self.do_model('blog.comments.model', 'query_comments_single', params)
        if not result:
            raise self._gre('BLOG_COMMENT_NOT_FOUND')
        raise self._grs(result)

    @tornado.gen.coroutine
    def query_blog_comment_list(self, params):
        """
        查询博文的评论列表
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['blog_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        result = yield self.do_model('blog.comments.model', 'query_blog_comment_list', params)

        if not result:
            raise self._gre('BLOG_COMMENT_NOT_FOUND')

        raise self._grs(result)
