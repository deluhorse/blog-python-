# -*- coding:utf-8 -*-

"""
@author: delu
@file: faretmplt_model_test.py
@time: 17/5/9 上午10:14
"""
from module.goods.model.faretmplt.faretmplt_model import Model

model = Model()

params = {
    'faretmplt_no': '5',
    'admin_id': '4',
    'faretmplt_name': '我的模板3',
    'fare_list': [
        {
            'city_no_list': '[0]',
            'init_num': 1,
            'init_fare': 0,
            'incre_num': 1,
            'incre_fare': 0
        },
        {
            'city_no_list': '[1,2,3]',
            'init_num': 1,
            'init_fare': 5,
            'incre_num': 1,
            'incre_fare': 4
        }
    ]
}

print model.create_faretmplt(params)

# params = {
#     'admin_id': '4'
# }
# print model.query_faretmplt_list(params)
