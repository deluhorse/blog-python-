# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_model.py
@time: 17/4/27 上午5:48
"""

from source.model import ModelBase


class Model(ModelBase):
    def create_order(self, params):
        """
        创建订单
        :param params: 
        :return: 
        """
        sql_list = []
        # 订单key
        order_key = 'order_id, shop_id, scen_type, scen_id, buyer_id,' \
                    'money_unit, goodsmoney_discount, money_total, fare_total, receiver,' \
                    'receiver_phone, receiver_addr, city_no'
        # 订单val
        order_val = '%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,  %s,%s,%s'
        # 订单value
        order_value_tuple = (params['order_id'], params['shop_id'], params['scen_type'], params['scen_id'],
                             params['buyer_id'], params['money_unit'], params['goodsmoney_discount'],
                             params['order_money_total'], params['fare_money_total'], params['receive']['name'],
                             params['receive']['mobile_no'], params['receive']['address'], params['receive']['city_no'])
        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
                         self.sql_constants.TABLE_NAME: 'tbl_om_order',
                         self.sql_constants.DICT_DATA: {self.sql_constants.KEY: order_key,
                                                        self.sql_constants.VAL: order_val},
                         self.sql_constants.VALUE_TUPLE: order_value_tuple})

        for sku_item in params['goods_list']:
            # order_sku key
            order_sku_key = 'order_id, goodssku_id, goods_id, money_unit, buy_vol, sku_price, goods_name, skuimage_id'
            # order_sku val
            order_sku_val = '%s,%s,%s,%s,%s,%s,%s,%s'
            # order_sku value
            order_sku_value_tuple = (params['order_id'], sku_item['sku_id'], sku_item['goods_id'],
                                     params['money_unit'], sku_item['buy_vol'], sku_item['price'],
                                     sku_item['goods_name'], sku_item['img_id'])
            sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
                             self.sql_constants.TABLE_NAME: 'tbl_om_ordergoodssku',
                             self.sql_constants.DICT_DATA: {self.sql_constants.KEY: order_sku_key,
                                                            self.sql_constants.VAL: order_sku_val},
                             self.sql_constants.VALUE_TUPLE: order_sku_value_tuple})
        return self.do_sqls(sql_list)

    def query_order(self, params):
        """
        查询订单
        :param params: 
        :return: 
        """
        # 查询的范围
        fields = [
            'odr.*',
            'sku.goodssku_id as sku_id',
            'sku.goods_id as goods_id',
            'sku.buy_vol as buy_vol',
            'sku.sku_price as sku_price',
            'sku.goods_name as goods_name'
        ]
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []
        if 'buyer_id' in params and params['buyer_id']:
            condition += ' and odr.buyer_id = %s '
            value_list.append(params['buyer_id'])
        if 'shop_id' in params and params['shop_id']:
            condition += ' and odr.shop_id = %s '
            value_list.append(params['shop_id'])
        if 'order_id' in params and params['order_id']:
            condition += ' and odr.order_id = %s '
            value_list.append(params['order_id'])
        if 'start_time' in params and params['start_time']:
            condition += ' and odr.create_time >= %s '
            value_list.append(params['start_time'])
        if 'end_time' in params and params['end_time']:
            condition += ' and odr.create_time <= %s '
            value_list.append(params['end_time'])

        # 表关联
        join = [{self.sql_constants.TABLE_NAME: 'tbl_om_ordergoodssku as sku',
                 self.sql_constants.JOIN_CONDITION: 'odr.order_id = sku.order_id'}]
        order = 'odr.create_time DESC '
        dict_data = {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
            self.sql_constants.JOIN: join,
            self.sql_constants.ORDER: order
        }
        # 分页
        if 'page_index' in params and 'page_size' in params:
            dict_data[self.sql_constants.LIMIT] = [str(params['page_index']), str(params['page_size'])]

        return self.find('tbl_om_order as odr', dict_data, tuple(value_list), self.sql_constants.LIST)

    def pay_success(self, params):
        """
        支付成功回调
        :param params: 
        :return: 
        """
        sql_list = []
        # 支付流水数据
        payment_data = params['payment']
        account_key = 'payorder_id, shop_id, order_id, pay_type, paysub_type, money_unit, money_total, trade_no'
        account_val = '%s,%s,%s,%s,%s,%s,%s,%s'
        account_value_tuple = (payment_data['payorder_id'], payment_data['shop_id'], payment_data['order_id'],
                               payment_data['pay_type'], payment_data['paysub_type'],
                               payment_data['money_unit'], payment_data['money_total'], payment_data['trade_no'])
        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
                         self.sql_constants.TABLE_NAME: 'tbl_om_orderpayment',
                         self.sql_constants.DICT_DATA: {self.sql_constants.KEY: account_key,
                                                        self.sql_constants.VAL: account_val},
                         self.sql_constants.VALUE_TUPLE: account_value_tuple})

        # 订单状态
        order_data = params['order_data']
        fields = ['order_status = %s']
        condition = ' order_id = %s '
        value_tuple = (order_data['order_status'], order_data['order_id'])
        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.UPDATE,
                         self.sql_constants.TABLE_NAME: 'tbl_om_order',
                         self.sql_constants.DICT_DATA: {
                             self.sql_constants.FIELDS: fields,
                             self.sql_constants.CONDITION: condition
                         },
                         self.sql_constants.VALUE_TUPLE: value_tuple})

        return self.do_sqls(sql_list)

    def query_order_count(self, params):
        """
        查询订单数量
        :param params: 
        :return: 
        """
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []

        if 'buyer_id' in params and params['buyer_id']:
            condition += ' and buyer_id = %s '
            value_list.append(params['buyer_id'])
        if 'order_id' in params and params['order_id']:
            condition += ' and order_id = %s '
            value_list.append(params['order_id'])
        if 'shop_id' in params and params['shop_id']:
            condition += ' and shop_id = %s '
            value_list.append(params['shop_id'])
        if 'order_status' in params and params['order_status']:
            condition += ' and order_status = %s '
            value_list.append(params['order_status'])

        return self.get_rows('tbl_om_order', {self.sql_constants.CONDITION: condition}, tuple(value_list))
