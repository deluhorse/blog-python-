# -*- coding:utf-8 -*-

"""
@author: delu
@file: cachekey_predix.py
@time: 17/4/13 下午3:01
"""


class CacheKeyPredix(object):

    # 用户管理

    # 管理员账户id
    ACCOUNT_ID = 'account_id'
    # 管理员id
    ADMIN_ID = 'admin_id'
    # 管理员id
    UID = 'uid'
    # 店铺id
    SHOP_ID = 'shop_id'
    # 管理员token前缀
    ADMIN_TOKEN = 'admin_token_'
    # 买家token前缀
    BUYER_TOKEN = 'buyer_token_'
    # 买家地址编号
    BUYER_ADDR_NO = 'buyer_addr_no'
    # 买家id
    BUYER_ID = 'buyer_id'
    # 微信小程序 - code
    MINI_APP_CODE = 'mini_app_code_'
    # 商品SKU库存
    GOODS_SKU_STOCK = 'sku:stock:'
    # 订单基础id，用于生成订单号
    ORDER_BASE_ID = 'order_base_id'
    # 微信小程序，模板消息发送队列
    MINI_APP_MODEL_MESSAGE_USER = 'mini_app_model_message_user_'
    # 微信小程序access_token
    MINI_APP_ACCESS_TOKEN = 'mini_app_access_token'
    # 物流模板编号
    GOODS_FARETMPLT_NO = 'goods_faretmplt_no'
