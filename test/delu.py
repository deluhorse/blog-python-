# -*- coding:utf-8 -*-

"""
@author: delu
@file: delu.py
@time: 18/6/13 15:36
"""


def hello(*xxx):
    print(xxx)


def hello1(fields):
    hello(*fields)


hello1(1, 2, 3)
