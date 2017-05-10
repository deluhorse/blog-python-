# -*- coding:utf-8 -*-

"""
@author: delu
@file: faretmplt_model.py
@time: 17/5/8 下午3:04
"""

from source.model import ModelBase


class Model(ModelBase):
    def get_many_by_faretmplt_no_list(self, faretmplt_no_list):
        """
        根据商品id列表查询物流模板
        :param faretmplt_no_list: 
        :return: 
        """
        # 查询范围
        fields = []
        # 查询条件
        condition = 'faretmplt_no ' + self.build_in(len(faretmplt_no_list))
        # 查询的值
        value_tuple = tuple(faretmplt_no_list)

        return self.find('tbl_gm_faretmplt', {self.sql_constants.FIELDS: fields,
                                              self.sql_constants.CONDITION: condition},
                         value_tuple,
                         self.sql_constants.LIST)

    def get_fare_by_faretmplt_no_list(self, faretmplt_no_list):
        """
        根据物流模板编号列表查询物流费用
        :param faretmplt_no_list: 
        :return: 
        """
        # 查询范围
        fields = []
        # 查询条件
        condition = 'faretmplt_no ' + self.build_in(len(faretmplt_no_list))
        # 查询的值
        value_tuple = tuple(faretmplt_no_list)

        return self.find('tbl_gm_fare', {self.sql_constants.FIELDS: fields,
                                         self.sql_constants.CONDITION: condition},
                         value_tuple,
                         self.sql_constants.LIST)

    def query_faretmplt_list(self, params):
        """
        查询物流模板
        :param params: 
        :return: 
        """
        # 查询范围
        fields = ['faretmplt.*, fare.init_num, fare.init_fare, fare.incre_num, fare.incre_fare,'
                  ' group_concat(CONVERT(fare.city_no,CHAR(4))) as citys']
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []
        # 链接条件
        join = [
            {self.sql_constants.TABLE_NAME: 'tbl_gm_fare as fare',
             self.sql_constants.JOIN_CONDITION: 'faretmplt.faretmplt_no = fare.faretmplt_no'},
            {self.sql_constants.TABLE_NAME: '', }
        ]
        # 分组条件
        group_by = ' faretmplt.faretmplt_no, fare.init_num, fare.init_fare, fare.incre_num, fare.incre_fare '

        if 'admin_id' in params and params['admin_id']:
            condition += ' and faretmplt.admin_id = %s '
            value_list.append(params['admin_id'])
        return self.find('tbl_gm_faretmplt as faretmplt', {self.sql_constants.FIELDS: fields,
                                                           self.sql_constants.CONDITION: condition,
                                                           self.sql_constants.JOIN: join,
                                                           self.sql_constants.GROUP_BY: group_by},
                         tuple(value_list),
                         self.sql_constants.LIST)

    def create_faretmplt(self, params):
        """
        创建物流模板
        :param params: 
        :return: 
        """
        sql_list = []

        # 物流模板
        faretmplt_key = 'faretmplt_no, admin_id, faretmplt_name'
        faretmplt_val = '%s, %s, %s'
        faretmplt_value_tuple = (params['faretmplt_no'], params['admin_id'], params['faretmplt_name'])

        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
                         self.sql_constants.TABLE_NAME: 'tbl_gm_faretmplt',
                         self.sql_constants.DICT_DATA: {self.sql_constants.KEY: faretmplt_key,
                                                        self.sql_constants.VAL: faretmplt_val},
                         self.sql_constants.VALUE_TUPLE: faretmplt_value_tuple})

        # 物流明细
        fare_key = 'faretmplt_no, city_no, init_num, init_fare, incre_num, incre_fare'
        fare_batch_val = []
        fare_value_list = []
        for fare_item in params['fare_list']:
            fare_batch_val.append('(%s,%s,%s,%s,%s,%s)')
            fare_value_list.append(params['faretmplt_no'])
            fare_value_list.append(fare_item['city_no_list'])
            fare_value_list.append(fare_item['init_num'])
            fare_value_list.append(fare_item['init_fare'])
            fare_value_list.append(fare_item['incre_num'])
            fare_value_list.append(fare_item['incre_fare'])
        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.BATCH_INSERT,
                         self.sql_constants.TABLE_NAME: 'tbl_gm_fare',
                         self.sql_constants.DICT_DATA: {self.sql_constants.KEY: fare_key,
                                                        self.sql_constants.BATCH_VAL: fare_batch_val},
                         self.sql_constants.VALUE_TUPLE: tuple(fare_value_list)})
        return self.do_sqls(sql_list)
