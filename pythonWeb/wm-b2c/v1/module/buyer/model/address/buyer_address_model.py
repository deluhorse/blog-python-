# -*- coding:utf-8 -*-

"""
@author: delu
@file: buyer_address_model.py
@time: 17/4/27 下午3:29
"""

from source.model import ModelBase


class Model(ModelBase):
    def create_address(self, params):
        """
        创建买家收货地址
        :param params: 
        :return: 
        """
        # key
        key = 'addr_no,city_no,district,street_addr,name,mobile_no,scen_type,  scen_id,buyer_id'
        # val
        val = '%s,%s,%s,%s,%s,  %s,%s,%s,%s'
        # value
        value_tuple = (params['addr_no'], params['city_no'], params['district'], params['street_addr'],
                       params['name'], params['mobile_no'], params['scen_type'], params['scen_id'], params['buyer_id'])
        return self.insert('tbl_um_buyeraddrlist', {self.sql_constants.KEY: key,
                                                    self.sql_constants.VAL: val}, value_tuple)

    def query_address_list(self, params):
        """
        查询买家地址列表
        :param params: 
        :return: 
        """
        # 查询范围
        fields = ['addr_no', 'city_no', 'district', 'street_addr', 'name',
                  'mobile_no', 'scen_type', 'scen_id', 'buyer_id']
        # 查询的条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []
        if 'buyer_id' in params:
            condition += ' and buyer_id = %s '
            value_list.append(params['buyer_id'])
        if 'addr_no' in params:
            condition += ' and addr_no = %s '
            value_list.append(params['addr_no'])
        if 'scen_type' in params:
            condition += ' and scen_type = %s '
            value_list.append(params['scen_type'])
        if 'scen_id' in params:
            condition += ' and scen_id = %s '
            value_list.append(params['scen_id'])
        return self.find('tbl_um_buyeraddrlist',
                         {self.sql_constants.FIELDS: fields,
                          self.sql_constants.CONDITION: condition},
                         tuple(value_list),
                         self.sql_constants.LIST)

    def query_default_addr(self, params):
        """
        查询买家默认地址
        :param params: 
        :return: 
        """
        # 查询范围
        fields = ['addr.*']
        # 查询条件
        condition = ' buyer.buyer_id = %s '
        # 查询的值
        value_tuple = (params['buyer_id'],)
        # 链接条件
        join = [{self.sql_constants.TABLE_NAME: 'tbl_um_buyeraddrlist as addr',
                 self.sql_constants.JOIN_CONDITION: ' buyer.default_addr = addr.addr_no '}]

        return self.find('tbl_um_buyer as buyer', {self.sql_constants.FIELDS: fields,
                                                   self.sql_constants.CONDITION: condition,
                                                   self.sql_constants.JOIN: join}, value_tuple)

    def update_default_addr(self, params):
        """
        修改买家默认地址
        :param params: 
        :return: 
        """
        # 修改范围
        fields = ['default_addr = %s']
        # 查询条件
        condition = ' buyer_id = %s '
        # 查询的值
        value_tuple = (params['addr_no'], params['buyer_id'])
        return self.update('tbl_um_buyer', {self.sql_constants.FIELDS: fields,
                                            self.sql_constants.CONDITION: condition}, value_tuple)
