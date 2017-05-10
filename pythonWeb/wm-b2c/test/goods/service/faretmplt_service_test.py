# -*- coding:utf-8 -*-

"""
@author: delu
@file: faretmplt_service_test.py
@time: 17/5/9 上午10:25
"""
from module.goods.service.faretmplt.faretmplt_service import Service

service = Service()

params = {
    'admin_id': '4'
}

print service.query_faretmplt_for_admin(params)
