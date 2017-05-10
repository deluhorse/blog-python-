# -*- coding:utf-8 -*-

"""
@author: delu
@file: error_code.py
@time: 17/4/19 下午3:10
"""

Code = {
    # 成功
    'SUCCESS': {'code': 0, 'msg': '成功'},
    # 用户无权限
    'AUTH_ERROR': {'code': 1006, 'msg': '用户无权限'},
    # 数据库执行失败
    'SQL_EXECUTE_ERROR': {'code': 1002, 'msg': '数据库执行失败'},
    # 请求类型错误
    'REQUEST_TYPE_ERROR': {'code': 1001, 'msg': '请求类型错误'},
    # 缓存执行失败
    'CACHE_EXECUTE_ERROR': {'code': 1003, 'msg': '缓存执行失败'},

    # 2 用户模块
    # 用户关键参数不存在
    'ADMIN_PARAMS_NOT_EXITS': {'code': 2001, 'msg': '关键参数非空'},
    # 账号未找到
    'ACCOUNT_NOT_FIND': {'code': 2003, 'msg': '账号未找到'},
    # 账号密码不匹配
    'ERROR_PASSWORD': {'code': 2004, 'msg': '账号密码不匹配'},
    # 两次密码不匹配
    'PASSWORD_NOT_MATCH': {'code': 2005, 'msg': '两次密码不匹配'},
    # 账号已存在
    'ACCOUNT_EXIST': {'code': 2006, 'msg': '账号已存在'},

    # 3 店铺管理
    'SHOP_NOT_PERMISSION': {'code': 3003, 'msg': '你无权管理该店铺'},

    # 4 买家模块
    'BUYER_CREATE_ERROR': {'code': 4003, 'msg': '创建买家失败'},

    # 5 商品模块
    'GOODS_PARAMS_ERROR': {'code': 5001, 'msg': '参数不正确'},
    'GOODS_NOT_FIND': {'code': 5002, 'msg': '商品未找到'},
    'GOODS_SKU_BUY_VOL_ERROR': {'code': 5003, 'msg': '购买数为0'},
    'GOODS_SKU_STOCK_NOT_ENOUGH': {'code': 5004, 'msg': '库存不足'},
    'GOODS_BUY_NOT_PERMISSION': {'code': 5005, 'msg': '商品不可购买(商品下架,商品金额为0,库存为0,商品金额发生了变动,购买数量超过了库存)'},
    'GOODS_SKU_ERROR': {'code': 5006, 'msg': '商品sku错误'},
    'GOODS_FARE_PARAMS_NOT_EXIST': {'code': 5007, 'msg': '物流模板关键参数不存在'},

    # 6 订单模块
    'ORDER_PARAMS_NOT_EXIST': {'code': 6001, 'msg': '关键参数不存在(商品,订单金额,收货人信息)'},
    'ORDER_RECEIVE_NOT_EXIST': {'code': 6002, 'msg': '收货信息不完善(收货人姓名,收货人地址,收获人手机号,城市编号)'},
    'ORDER_GOODS_DECREASE_STOCK_ERROR': {'code': 6003, 'msg': '扣商品库存失败'},
    'ORDER_STATUS_ERROR': {'code': 6004, 'msg': '订单状态已改变'},
    'ORDER_ADDRESS_CREATE_PARAMS_ERROR': {'code': 6005, 'msg': '订单order_id为空'},
    'ORDER_BUYER_NOT_PERMISSION': {'code': 6006, 'msg': '该买家无权操作当前订单'},
    'ORDER_SEND_PARAMS_NOT_EXIST': {'code': 6007, 'msg': '订单发货关键参数缺失(订单号,物流公司,物流单号)'},
    'ORDER_SHOP_NOT_PERMISSION': {'code': 6008, 'msg': '该商家无法操作当前订单'},
    'ORDER_RECEIVE_PARAMS_NOT_EXIST': {'code': 6009, 'msg': '订单收货关键参数缺失'},
    'ORDER_STATUS_CHANGE_NOT_PERMISSION': {'code': 6010, 'msg': '订单状态无法更改'},
    'ORDER_FARE_MONEY_ERROR': {'code': 6011, 'msg': '计算运费失败'},

    # 7 支付
    'PAY_PARAMS_NOT_ERROR': {'code': '7001', 'msg': '支付关键参数不存在'},
    'PAY_NOTIFY_XML_ERROR': {'code': '7002', 'msg': 'xml数据格式错误'},
    'PAY_PREPAY_ID_ERROR': {'code': '7003', 'msg': '获取预支付数据失败'},

    # 9 微信小程序获取 sessionkey失败
    'MINI_APP_GET_SESSIONKEY_ERROR': {'code': 9003, 'msg': '微信小程序获取sessionkey失败'},
    'MINI_APP_FORM_ID_NOT_EXIST': {'code': 9004, 'msg': 'form_id和goods_id非空'},
    'MINI_APP_ACTIVITY_GOODS_ID': {'code': 9005, 'msg': 'goods_id和start_time非空'},

    # 10 配置
    'CFG_ADMIN_ID_NOT_EXIST': {'code': 10001, 'msg': '管理员id非空'},
    'CFG_ADMIN_QUERY_ERROR': {'code': 10002, 'msg': '查询管理员配置失败'}
}
