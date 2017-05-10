# -*- coding:utf-8 -*-

"""
@author: delu
@file: common_util.py
@time: 17/4/24 上午11:31
"""


class CommonUtil(object):
    @staticmethod
    def remove_element(my_dict, element_list):
        """
        移除字典中的元素
        :param my_dict: 
        :param element_list: 
        :return: 
        """
        for element in element_list:

            if element in my_dict:
                my_dict.pop(element)
        return my_dict

    @staticmethod
    def is_empty(key_list, my_dict):
        """
        判断key_list中的元素是否存在为空的情况
        :param key_list: 
        :param my_dict: 
        :return: 
        """
        for key in key_list:
            if key not in my_dict or not my_dict[key]:
                return True
        return False
