# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/8/31 14:38
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
    def create_reply(self, params={}):
        """
        创建回复
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['blog_id', 'comment_id', 'nick_name', 'reply_content'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        # 检查评论是否有效
        comment_result = yield self.do_service('blog.comments.service', 'query_comments_single', params)
        if comment_result['code'] != 0:
            raise self._gr(comment_result)

        params['parent_reply_id'] = params.get('parent_reply_id', 0)

        result = yield self.do_model('blog.comments.reply.model', 'create_reply', params)

        if not result:
            raise self._gre('SQL_EXECUTE_ERROR')

        raise self._grs()
