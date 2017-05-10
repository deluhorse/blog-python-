# -*- coding:utf-8 -*-

"""
@author: delu
@file: goods_service_test.py
@time: 17/5/9 上午10:40
"""
from v1.module.goods.service.goods_service import Service

service = Service()
setattr(service, 'language_code', 'cn')
# params = {
#     'sku_id': ['S003NAKSHX', 'S0067PWWLD', 'S006LNBDSM', 'S007TWALQG', 'S008CSAGNV', 'S00YOPNYIV']
# }
# print service.get_sku(params)

params = {
    '': ''
}


service.create(params)
