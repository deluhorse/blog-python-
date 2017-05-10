# -*- coding:utf-8 -*-

"""
@author: delu
@file: faretmplt_service.py
@time: 17/5/8 下午2:47
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    faretmplt_service
    """

    faretmplt_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.faretmplt_model = self.import_model('goods.model.faretmplt.faretmplt_model')

    def query_faretmplt_list(self, params):
        """
        根据商品id列表查询物流模板列表
        :param faretmplt_no_list: 
        :return: 
        """
        data_result = {}
        fare_result = self.faretmplt_model.get_fare_by_faretmplt_no_list(params['faretmplt_no_list'])
        if fare_result:
            for fare_item in fare_result:
                if self.common_utils.is_empty([fare_item['faretmplt_no']], data_result):
                    data_result[fare_item['faretmplt_no']] = {}
                    data_result[fare_item['faretmplt_no']]['goods_nums'] = 0
                data_result[fare_item['faretmplt_no']][fare_item['city_no']] = fare_item
            result = self._e('SUCCESS')
            result['data'] = data_result
            return result
        else:
            return self._e('SQL_EXECUTE_ERROR')

    def create(self, params):
        """
        创建物流模板
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['faretmplt_name', 'fare_list'], params):
            self._e('GOODS_FARE_PARAMS_NOT_EXIST')
        redis = self.redis.get_conn()
        params['faretmplt_no'] = redis.incr(self.cache_key_predix.GOODS_FARETMPLT_NO)
        result = self.faretmplt_model.create_faretmplt(params)
        if result is None:
            return self._e('SQL_EXECUTE_ERROR')
        else:
            return self._e('SUCCESS')

    def query_faretmplt_for_admin(self, params):
        """
        查询物流模板(管理员)
        :param params: 
        :return: 
        """
        data_result = {}
        fare_result = self.faretmplt_model.query_faretmplt_list(params)
        if fare_result is None:
            return self._e('SQL_EXECUTE_ERROR')
        for fare in fare_result:
            if fare['faretmplt_no'] not in data_result:
                data_result[fare['faretmplt_no']] = {
                    'faretmplt_name': fare['faretmplt_name'],
                    'admin_id': fare['admin_id'],
                    'fare_list': []
                }
            data_result[fare['faretmplt_no']]['fare_list'].append({
                'init_num': fare['init_num'],
                'init_fare': fare['init_fare'],
                'incre_num': fare['incre_num'],
                'incre_fare': fare['incre_fare'],
                'city_no_list': fare['citys'].split(',')
            })
        return data_result

    def update(self, params):
        """
        更新物流模板
        :param params: 
        :return: 
        """
        pass
