# -*- coding:utf-8 -*-

"""
@author: delu
@file: error_code.py
@time: 17/4/19 下午3:10
"""

Code = {
    # 1 通用
    'SUCCESS': {'code': 0, 'msg': '成功'},
    'REQUEST_TYPE_ERROR': {'code': 1001, 'msg': '请求类型错误'},
    'SQL_EXECUTE_ERROR': {'code': 1002, 'msg': '数据库执行失败'},
    'CACHE_EXECUTE_ERROR': {'code': 1003, 'msg': '缓存执行失败'},
    'PARAMS_NOT_EXIST': {'code': 1004, 'msg': '参数错误'},
    'PARAMS_TYPE_ERROR': {'code': 1005, 'msg': '参数类型错误'},
    'AUTH_ERROR': {'code': 1006, 'msg': '用户无权限'},
    'NOT_LOGIN': {'code': 1007, 'msg': '用户未登录'},
    'DATA_EXIST': {'code': 1008, 'msg': '数据已存在'},
    'DATA_NOT_EXIST': {'code': 1009, 'msg': '数据不存在'},
    'PARAMS_DATE_ERROR': {'code': 1010, 'msg': '时间类型错误'},
    'JSON_DATA_FORMAT_ERROR': {'code': 1011, 'msg': 'JSON数据格式错误'},
    'DATA_FORMAT_ERROR': {'code': 1012, 'msg': '数据错误'},
    'AMOUNT_TYPE_ERROR': {'code': 1013, 'msg': '金额类型错误'},
    'EMAIL_SEND_ERROR': {'code': 1014, 'msg': '邮件发送失败'},
    'AUTH_SET_ERROR': {'code': 1015, 'msg': '权限设置错误'},
    'SIGN_VERIFY_FAILED': {'code': 1016, 'msg': '验签失败'},
    'HTTP_REQUEST_FAILED': {'code': 1017, 'msg': 'HTTP请求失败'},
    'METHOD_NOT_EXIST': {'code': 1018, 'msg': '方法未找到'},
    'FILE_UPLOAD_FAILED': {'code': 1019, 'msg': '上传文件错误'},
    'SECRET_KEY_NOT_EXIST': {'code': 1020, 'msg': '密钥不存在'},

    # 2 图片
    'PHOTO_CREATE_PARAMS_NOT_EXIST': {'code': 2001, 'msg': '创建图片,参数丢失'},
    'PHOTO_NOT_FOUND': {'code': 2002, 'msg': '照片未找到'},
    # 3 博客
    'BLOG_NOT_FOUND': {'code': 3001, 'msg': '博客未找到'},
    # 4 用户
    'USER_NOT_FOUND': {'code': 3002, 'msg': '用户未找到'},
    'ACCOUNT_REPEAT': {'code': 3003, 'msg': '该用户已存在'},
    'ACCOUNT_NOT_FOUND': {'code': 3004, 'msg': '账户未找到'},
    'PASSWORD_ERROR': {'code': 3005, 'msg': '密码错误'}
}
