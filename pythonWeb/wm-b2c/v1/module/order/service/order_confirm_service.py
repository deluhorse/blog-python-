# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_confirm_service.py
@time: 17/5/9 下午5:47
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    order_confirm_service
    """

    def get_order_confirm(self, params):
        """
        订单确认页计算
        :param params: 
        :return: 
        """
        # 校验关键参数
        if self.common_utils.is_empty(['goods_list', 'shop_id'], params):
            return self._e('ORDER_PARAMS_NOT_EXIST')
        # 查询商品信息，用来校验订单金额是否正确
        goods_final_result = []
        goods_result = self.do_service('goods.service.goods_service', 'get_sku',
                                       {'sku_id': [sku_id['sku_id'] for sku_id in params['goods_list']]})
        if goods_result['code'] != 0:
            return goods_result
        if not goods_result['data']:
            return self._e('GOODS_NOT_FIND')
        if len(goods_result['data']) != len(params['goods_list']):
            # 错误的sku_id传递给后台
            result = self._e('GOODS_SKU_ERROR')
            result['data'] = {'db_sku_id_list': [sku_id_item['sku_id'] for sku_id_item in goods_result['data']],
                              'page_sku_id_list': [sku_id['sku_id'] for sku_id in params['goods_list']]}
            return result
        order_money_total = 0
        fare_money_total = 0
        goods_result['data'] = self.get_goods_list(goods_result['data'], params['goods_list'])
        # 查询管理员配置
        params['admin_id'] = goods_result['data'][0]['admin_id']
        admin_cfg = self.do_service('cfg.user.service.cfg_user_service', 'get_admin_cfg', params)
        if admin_cfg['code'] != 0:
            return self._e('CFG_ADMIN_QUERY_ERROR')
        elif admin_cfg['data']['cfg_content']['addr_before_order']:
            # 检查订单收货信息
            if self.common_utils.is_empty(['receive'], params) \
                    or self.common_utils.is_empty(['name', 'mobile_no', 'city_no'], params['receive']) \
                    or int(params['receive']['city_no']) == 0:
                return self._e('ORDER_RECEIVE_NOT_EXIST')
            fare_result = self.do_service('order.service.order_base_service', 'cal_fare_money',
                                          {'goods_list': goods_result['data'], 'city_no': params['receive']['city_no']})
            if fare_result['code'] != 0:
                return self._e('ORDER_FARE_MONEY_ERROR')
            else:
                fare_money_total = fare_result['data']
        order_money_total += fare_money_total
        for goods in goods_result['data']:
            order_money_total = order_money_total + (goods['buy_vol'] * goods['price'])
            if goods['onshelf'] == 0 or goods['price'] == 0 or goods['stock'] == 0:
                # 商品发生了变动，提示买家生成订单失败
                goods_final_result.append({'goods_id': goods['goods_id'], 'sku_id': goods['sku_id'],
                                           'onshelf': goods['onshelf'], 'price': goods['price'],
                                           'stock': goods['stock'], 'goods_name': goods['goods_name']})
        # 商品发生了变动，提示买家生成订单失败
        if goods_final_result:
            result = self._e('GOODS_BUY_NOT_PERMISSION')
            result['data'] = {'goods_list': goods_final_result,
                              'db_order_money_total': order_money_total,
                              'fare_money_total': fare_money_total,
                              'page_order_money_total': int(params['order_money_total'])}
            return result

        result = self._e('SUCCESS')
        result['data'] = {
            'order_money': order_money_total,
            'fare_total': fare_money_total,
            'goods_list': goods_result['data']
        }
        return result

    def get_goods_list(self, db_goods_list, page_goods_list):
        """
        生成商品用于创建订单
        :param goods:
        :return:
        """
        for goods_source in db_goods_list:
            for goods_target in page_goods_list:
                if cmp(goods_source['sku_id'], goods_target['sku_id']) == 0:
                    goods_source['buy_vol'] = goods_target['buy_vol']
        return db_goods_list
