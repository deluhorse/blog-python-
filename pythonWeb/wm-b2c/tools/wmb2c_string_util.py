# -*- coding:utf-8 -*-

"""
@author: delu
@file: wmb2c_string_util.py
@time: 17/4/14 上午11:01
"""


class StringUtils(object):
    @staticmethod
    def is_empty(text=''):
        if text is None or text.strip() == '':
            return True
        else:
            return False

    @staticmethod
    def is_not_empty(text=''):
        return not StringUtils.is_empty(text)
