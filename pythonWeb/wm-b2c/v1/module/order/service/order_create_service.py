# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_create_service.py
@time: 17/4/27 上午6:03
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    order_create_service
    """

    order_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.order_model = self.import_model('order.model.order_model')

    def create_order(self, params):
        """
        创建订单
        :param params: 
        :return: 
        """
        # 校验关键参数
        if self.common_utils.is_empty(['goods_list', 'order_money_total', 'shop_id'], params):
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
        if goods_final_result or order_money_total != int(params['order_money_total']):
            result = self._e('GOODS_BUY_NOT_PERMISSION')
            result['data'] = {'goods_list': goods_final_result,
                              'db_order_money_total': order_money_total,
                              'fare_money_total': fare_money_total,
                              'page_order_money_total': int(params['order_money_total'])}
            return result

        # 订单号
        params['order_id'] = self.create_order_id(params['shop_id'])
        params['money_unit'] = params['goods_list'][0]['money_unit']
        params['goods_list'] = self.get_goods_list(goods_result['data'], params['goods_list'])
        params['goodsmoney_discount'] = 0
        params['fare_money_total'] = fare_money_total

        # 扣库存
        error_stock_sku_list = []
        flag = False
        if admin_cfg['data']['cfg_content']['addr_before_order']:
            for goods in params['goods_list']:
                result = self.do_service('goods.service.goods_service', 'decrease_sku_stock', goods)
                if result['code'] != 0:
                    flag = True
                    break
                else:
                    error_stock_sku_list.append({'sku_id': goods['sku_id'], 'buy_vol': goods['buy_vol']})
            if flag:
                # 如果存在扣库存失败的情况，则还原库存
                for goods in error_stock_sku_list:
                    self.do_service('goods.service.goods_service', 'return_sku_stock', goods)
                return self._e('ORDER_GOODS_DECREASE_STOCK_ERROR')

        result = self.order_model.create_order(params)

        if result:
            result = self._e('SUCCESS')
            # 创建订单成功, 获取支付信息
            # 构建请求参数
            pay_params = {
                'out_trade_no': params['order_id'],
                'total_fee': order_money_total,
                'spbill_create_ip': params['client_ip'],
                'body': params['goods_list'][0]['goods_name'],
                'openid': params['buyer_id']
            }
            package = params['package'] if not self.common_utils.is_empty(['package'], params) else 'plugins.mini_app'
            pay_result = self.do_service(package + '.service.wechat_service', 'get_prepay_id', pay_params)
            if pay_result['code'] == 0:
                result['data'] = {
                    'order_id': params['order_id'],
                    'prepay_id': pay_result['data']['prepay_id'],
                    'nonce_str': pay_result['data']['nonce_str'],
                    'sign': pay_result['data']['sign'],
                    'time_stamp': pay_result['data']['time_stamp']
                }
            else:
                result['data'] = {
                    'order_id': params['order_id']
                }
            return result
        else:
            # 如果失败，则还原库存
            if admin_cfg['data']['cfg_content']['addr_before_order']:
                for goods in error_stock_sku_list:
                    self.do_service('goods.service.goods_service', 'return_sku_stock', goods)
            return self._e('SQL_EXECUTE_ERROR')

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
                    goods_source['money_unit'] = goods_target['money_unit']
        return db_goods_list

    def create_order_id(self, shop_id='0'):
        """
        生成订单号 220170426164000987
        店铺号_yyyyMMddHHmmss_五位有序整数
        当有序整数大于等于10000时，重置为1，一般格式为00001
        :return: 
        """
        redis = self.redis.get_conn()
        datestr = self.datetime.datetime.strftime(self.datetime.datetime.now(), '%Y%m%d%H%M%S')
        base_number = redis.incr(self.cache_key_predix.ORDER_BASE_ID)
        length = 5 - len(str(base_number))
        if length >= 5:
            redis.set(self.cache_key_predix.ORDER_BASE_ID, 1)
        count = 1
        tail = ''
        while count <= length:
            tail += '0'
            count = count + 1

        return shop_id + '_' + datestr + '_' + tail + str(base_number)
