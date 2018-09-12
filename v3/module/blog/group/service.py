# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/9/6 11:50
"""
import tornado.gen

from base.service import ServiceBase


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
    def create_group(self, params={}):
        """
        创建分组
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['parent_group_id', 'group_name', 'user_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        result = yield self.do_model('blog.group.model', 'create_group', params)

        if not result:
            raise self._gre('SQL_EXECUTE_ERROR')

        raise self._grs(result)

    @tornado.gen.coroutine
    def query_group(self, params):
        """
        查询分组及所有子分组
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['user_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        group_list = yield self.do_model('blog.group.model', 'query_group_list', params)

        if not group_list:
            raise self._gre('GROUP_NOT_FOUND')

        # 构造一个树
        # 转成group字典
        parent_group_dict = {}
        for group in group_list:

            parent_group_id = group['parent_group_id']

            if parent_group_id in parent_group_dict:

                parent_group_dict[parent_group_id].append(group)
            else:
                parent_group_dict[parent_group_id] = [group]

        # 从根节点开始构造整棵树
        root_group_list = self.__build_group_tree_list(-1, parent_group_dict)

        raise self._grs(root_group_list)

    def __build_group_tree_list(self, parent_group_id, parent_group_dict):
        """
        从group_list中构造一颗树
        :param parent_group_id: 
        :param parent_group_dict: 
        :return: 
        """
        final_group_list = []

        if parent_group_id not in parent_group_dict:
            return []

        child_group_list = parent_group_dict[parent_group_id]

        for group in child_group_list:
            group['sub_group_list'] = self.__build_group_tree_list(group['group_id'], parent_group_dict)

            final_group_list.append(group)

        return final_group_list

    @tornado.gen.coroutine
    def update_group(self, params):
        """
        更新分组
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['group_id', 'group_name', 'user_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        result = yield self.do_model('blog.group.model', 'update_group', params)

        if not result:
            raise self._gre('SQL_EXECUTE_ERROR')

        raise self._grs()

    @tornado.gen.coroutine
    def delete_group(self, params):
        """
        删除分组
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['group_id', 'user_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        group_list = yield self.do_model('blog.group.model', 'query_group_list', params)

        if not group_list:
            raise self._gre('GROUP_NOT_FOUND')

        # 构造一个树
        # 转成group字典
        parent_group_dict = {}
        for group in group_list:

            parent_group_id = group['parent_group_id']

            if parent_group_id in parent_group_dict:

                parent_group_dict[parent_group_id].append(group)
            else:
                parent_group_dict[parent_group_id] = [group]

        root_group_list = self.__build_group_tree_list(int(params['group_id']), parent_group_dict)

        final_group_list = self.__tree_parse_list(root_group_list)

        group_id_list = [group['group_id'] for group in final_group_list]

        group_id_list.append(params['group_id'])

        result = yield self.do_model(
            'blog.group.model',
            'delete_group',
            {
                'group_id_list': group_id_list,
                'user_id': params['user_id']
            })

        raise self._grs(result)

    def __tree_parse_list(self, group_list):
        """
        将树形结构转换成列表结构
        :param group_list: 
        :return: 
        """
        final_group_list = []

        for group in group_list:

            final_group_list.append(group)

            final_group_list.extend(self.__tree_parse_list(group['sub_group_list']))

        return final_group_list
