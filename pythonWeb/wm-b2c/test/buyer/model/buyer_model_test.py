# -*- coding:utf-8 -*-

"""
@author: delu
@file: buyer_model_test.py
@time: 17/5/9 下午3:12
"""
from v1.module.buyer.model.buyer_model import Model

model = Model()
params = {
    'mobile': '18817337826'
}
print model.query_buyer(params)
