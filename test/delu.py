# -*- coding:utf-8 -*-

"""
@author: delu
@file: delu.py
@time: 18/6/13 15:36
"""
from source.redisbase import RedisBase

redis = RedisBase()

redis.publish('channel1', 'hello')
