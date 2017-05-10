# -*- coding:utf-8 -*-

"""
@author: delu
@file: buyer_service.py
@time: 17/4/24 下午4:02
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    buyer_service
    """

    buyer_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.buyer_model = self.import_model('buyer.model.buyer_model')

    def login(self, params):
        """
        买家登录, 如果买家未注册则创建一个新的买家
        :param params: 
        :return: 
        """
        # 查询买家信息
        buyer_data = self.buyer_model.query_buyer(params)

        if buyer_data is None:
            # 创建买家
            redis = self.redis.get_conn()
            params['buyer_id'] = redis.incr(self.cache_key_predix.BUYER_ID)
            res = self.buyer_model.create_buyer(params)
            if res is None:
                return self._e('BUYER_CREATE_ERROR')
            else:
                result = self._e('SUCCESS')
                result['data'] = params
                return result
        elif buyer_data is False:
            return self._e('SQL_EXECUTE_ERROR')
        else:
            if buyer_data is None:
                return self._e('SQL_EXECUTE_ERROR')
            else:
                result = self._e('SUCCESS')
                result['data'] = buyer_data
                return result

    def create_buyer(self, params):
        """
        创建买家，如果一存在
        :param params: 
        :return: 
        """
        res = self.buyer_model.query_buyer_count(params)
        if res > 0:
            return self._e('SUCCESS')
        else:
            res = self.buyer_model.create_buyer(params)
            if res:
                # 创建成功
                return self._e('SUCCESS')
            else:
                return self._e('SQL_EXECUTE_ERROR')
