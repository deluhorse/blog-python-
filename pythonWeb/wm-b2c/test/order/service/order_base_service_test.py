# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_base_service_test.py
@time: 17/5/9 上午10:30
"""
from v1.module.order.service.order_base_service import Service

service = Service()
setattr(service, 'language_code', 'cn')
goods_list = [
    {
        'logistics_template_id': 1,
        'buy_vol': 3
    },
    {
        'logistics_template_id': 2,
        'buy_vol': 3
    },
    {
        'logistics_template_id': 3,
        'buy_vol': 3
    },
    {
        'logistics_template_id': 1,
        'buy_vol': 4
    },
    {
        'logistics_template_id': 2,
        'buy_vol': 5
    },
    {
        'logistics_template_id': 3,
        'buy_vol': 5
    },
]
city_no = '3'
print service.cal_fare_money({'goods_list': goods_list, 'city_no': '3'})
