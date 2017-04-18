# -*- coding:utf-8 -*-

"""
@author: delu
@file: CJsonEncoder.py
@time: 17/4/14 下午6:02
"""
import datetime
import json
import decimal
import time


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        FORMAT = '%Y-%m-%d %H:%M:%S'
        if isinstance(obj, (datetime.datetime,)):
            return str(int(time.mktime(time.strptime(obj.strftime(FORMAT), FORMAT))))
        elif isinstance(obj, (decimal.Decimal,)):
            return str(obj)
        else:
            return super.default(obj)
