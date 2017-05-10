# -*- coding:utf-8 -*-

"""
@author: delu
@file: constants.py
@time: 17/4/12 下午2:22
"""


class Constants(object):

    SELLER_TYPE = 'seller'
    BUYER_TYPE = 'buyer'
    SUPER_ADMIN_TYPE = 'super_admin'
    ADMIN_TYPE = 'admin'

    SCEN_TYPE_WECHAT = 2

    # 支付
    PAY_TYPE_WECHAT = 3
    PAY_SUB_TYPE_WECHAT = 1

    # 订单状态
    # 未支付
    ORDER_WAIT_PAY = 1
    # 未发货
    ORDER_PAY_SUCCESS = 2
    # 已发货
    ORDER_SEND = 3
    # 已收货
    ORDER_RECEIVED = 4

