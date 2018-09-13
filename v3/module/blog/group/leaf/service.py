# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/9/13 10:00
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
    def query_leafs(self, params={}):
        """
        查询叶子分组
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['user_id'], params):

            raise self._gre('PARAMS_NOT_EXIST')

        group_result = yield self.do_service('blog.group.service', 'query_group', params)

        if group_result['code'] != 0:

            raise self._gr(group_result)

        leaf_group_list = self.__get_leafs(group_result['data'], [])

        raise self._grs(leaf_group_list)

    def __get_leafs(self, group_list, path_list):
        """
        查询所有叶子分组并记录下节点访问路径
        :param group_list: 
        :return: 
        """

        temp_path_list = list(path_list)

        leaf_list = []

        for group in group_list:

            if group['sub_group_list']:

                temp_path_list.append(group['group_name'])

                leaf_list.extend(self.__get_leafs(group['sub_group_list'], temp_path_list))

            else:

                group['path'] = '-->'.join(path_list) + '-->' + group['group_name']

                leaf_list.append(group)

        return leaf_list
