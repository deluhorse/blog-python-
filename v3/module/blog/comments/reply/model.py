# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/8/31 14:38
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def create_reply(self, params):
        """
        创建回复
        """
        key = 'parent_reply_id, comment_id, blog_id, nick_name, reply_content'
        value_tuple = (params['parent_reply_id'], params['comment_id'], params['blog_id'],
                       params['nick_name'], params['reply_content'])
        result = yield self.insert(
            'tbl_blog_comments_reply',
            {
                self.sql_constants.KEY: key
            },
            value_tuple
        )

        raise self._gr(result)
