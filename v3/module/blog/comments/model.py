# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/8/31 14:31
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def create_comments(self, params):
        """
        创建评论
        """
        key = 'blog_id, nick_name, comment_content'
        value_tuple = (params['blog_id'], params['nick_name'], params['comment_content'])
        result = yield self.insert(
            'tbl_blog_comments',
            {
                self.sql_constants.KEY: key
            },
            value_tuple
        )

        raise self._gr(result)

    @tornado.gen.coroutine
    def query_comments_single(self, params):
        """
        查询单条回复
        :param params: 
        :return: 
        """
        condition = ' comment_id = %s '
        value_tuple = (params['comment_id'], )
        result = yield self.find('tbl_blog_comments', {self.sql_constants.CONDITION: condition}, value_tuple)

        raise self._gr(result)

    @tornado.gen.coroutine
    def query_blog_comment_list(self, params):
        """
        查询博文的所有评论
        :param params: 
        :return: 
        """
        condition = ' blog_id = %s '
        value_tuple = (params['blog_id'],)
        comment_list = yield self.find(
            'tbl_blog_comments',
            {
                self.sql_constants.CONDITION: condition
            },
            value_tuple,
            self.sql_constants.LIST
        )

        if comment_list:
            # 查询每条评论对应的回复
            reply_list = yield self._query_reply_list({
                'comment_id_list': [comment['comment_id'] for comment in comment_list]
            })

            comment_dict = {}

            if reply_list:

                for reply in reply_list:

                    comment_id = reply['comment_id']

                    if comment_id in comment_dict:

                        comment_dict[comment_id].append(reply)
                    else:
                        comment_dict[comment_id] = [reply]

            for comment in comment_list:

                comment_id = comment['comment_id']

                if comment_id in comment_dict:

                    comment['reply_list'] = comment_dict[comment_id]

                else:
                    comment['reply_list'] = []

        raise self._gr(comment_list)

    @tornado.gen.coroutine
    def _query_reply_list(self, params):
        """
        查询评论对应的回复
        :param params: 
        :return: 
        """

        condition = ' 1 = 1 '
        value_list = []

        if 'comment_id_list' in params and params['comment_id_list']:

            condition += ' and comment_id ' + self.build_in(len(params['comment_id_list']))

            value_list.extend(params['comment_id_list'])

        result = yield self.find(
            'tbl_blog_comments_reply',
            {
                self.sql_constants.CONDITION: condition
            },
            tuple(value_list),
            self.sql_constants.LIST
        )

        raise self._gr(result)
