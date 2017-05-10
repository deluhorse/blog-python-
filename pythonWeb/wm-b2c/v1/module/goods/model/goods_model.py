# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 4/25/2017
"""

from source.model import ModelBase


class Model(ModelBase):
    def create(self, params):
        """
        创建商品
        :param params: 
        :return: 
        """
        sql_list = []
        # 商品数据
        goods_data = params['goods']
        account_key = 'goods_id, admin_id, goods_name, images, create_time, pre_buy_time'
        account_val = '%s,%s,%s,%s,%s,%s'
        account_value_tuple = (goods_data['goods_id'], params['admin_id'], goods_data['goods_name'],
                               goods_data['images'], params['create_time'], goods_data['pre_buy_time'])
        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
                         self.sql_constants.TABLE_NAME: 'tbl_gm_goods',
                         self.sql_constants.DICT_DATA: {self.sql_constants.KEY: account_key,
                                                        self.sql_constants.VAL: account_val},
                         self.sql_constants.VALUE_TUPLE: account_value_tuple})

        sku_list = params['sku_list']
        for sku in sku_list:
            key = 'sku_id, goods_id, stock, price, origin_price, properties'
            val = '%s, %s, %s, %s, %s, %s'
            value_tuple = (sku['sku_id'], sku['goods_id'], sku['stock'], sku['price'], sku['origin_price'],
                           sku['properties'])
            sql_list.append({'sql_type': self.sql_constants.INSERT,
                             'table_name': 'tbl_gm_goods_sku',
                             'dict_data': {'key': key, 'val': val},
                             'value_tuple': value_tuple})

        return self.do_sqls(sql_list)

    def query_goods(self, goods_id):
        """
        查询商品
        :param goods_id: 
        :return: 
        """
        # 请求字段
        fields = []
        # 请求条件
        condition = ' 1 = 1 '
        # 请求的值
        value_list = []

        condition += " and goods_id = %s "
        value_list.append(goods_id)

        return self.find('tbl_gm_goods', {self.sql_constants.FIELDS: fields,
                                          self.sql_constants.CONDITION: condition}, tuple(value_list))

    def query_one_sku(self, sku_id):
        """
        查询一个SKU
        :param sku_id: 
        :return: 
        """
        # 请求字段
        fields = [
            'sku.goods_name as sku_goods_name',
            'sku_id',
            'stock',
            'price',
            'origin_price',
            'properties',
            'img_id',
            'goods.goods_name as goods_name',
            'goods.goods_id as goods_id',
            'goods.images as images',
            'goods.pre_buy_time as pre_buy_time'
        ]
        # 请求条件
        condition = ' 1 = 1 '
        # 请求的值
        value_list = []

        condition += " and sku_id = %s "
        value_list.append(sku_id)

        # 表链接
        join = [
            {self.sql_constants.TABLE_NAME: 'tbl_gm_goods AS goods',
             self.sql_constants.JOIN_CONDITION: 'sku.goods_id = goods.goods_id'}
        ]

        return self.find('tbl_gm_goods_sku as sku', {self.sql_constants.FIELDS: fields,
                                                     self.sql_constants.JOIN: join,
                                                     self.sql_constants.CONDITION: condition}, tuple(value_list))

    def query_goods_sku_by_goods_id(self, goods_id):
        """
        获取商品所有sku
        :param goods_id: 商品ID
        :return: 
        """
        # 请求字段
        fields = []
        # 请求条件
        condition = ' 1 = 1 '
        # 请求的值
        value_list = []

        condition += " and goods_id = %s "
        value_list.append(goods_id)

        return self.find('tbl_gm_goods_sku',
                         {self.sql_constants.FIELDS: fields,
                          self.sql_constants.CONDITION: condition},
                         tuple(value_list),
                         self.sql_constants.LIST)

    def query_goods_sku_by_sku_id(self, sku_id_list):
        """
        通过sku_id获取sku及goods信息
        :param sku_id_list: 
        :return: 
        """
        # 请求字段
        fields = [
            'sku.goods_name as sku_goods_name',
            'sku_id',
            'stock',
            'price',
            'origin_price',
            'properties',
            'img_id',
            'goods.goods_name as goods_name',
            'goods.goods_id as goods_id',
            'goods.images as images',
            'goods.onshelf as onshelf',
            'goods.admin_id as admin_id',
            'goods.logistics_template_id as logistics_template_id'
        ]
        # 请求条件
        condition = [' 1 = 1 ']
        # 请求的值
        value_list = []

        condition.append(" and sku_id in (")
        # condition += " and sku_id in (%s) "
        in_list = []
        for item in sku_id_list:
            in_list.append("%s")
            value_list.append(item)

        condition.append(','.join(in_list))
        condition.append(")")
        condition = ''.join(condition)
        # value_list.append(sku_id)

        # 表链接
        join = [
            {self.sql_constants.TABLE_NAME: 'tbl_gm_goods AS goods',
             self.sql_constants.JOIN_CONDITION: 'sku.goods_id = goods.goods_id'}
        ]

        return self.find('tbl_gm_goods_sku as sku',
                         {self.sql_constants.FIELDS: fields,
                          self.sql_constants.JOIN: join,
                          self.sql_constants.CONDITION: condition},
                         tuple(value_list),
                         self.sql_constants.LIST)
