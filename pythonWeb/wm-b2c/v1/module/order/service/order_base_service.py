# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_base_service.py
@time: 17/5/5 下午3:26
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    order_base_service
    """

    order_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.order_model = self.import_model('order.model.order_model')

    def check_order(self, params):
        """
        检查该订单是否属于该角色
        order_id, shop_id, buyer_id
        :param params: 
        :return: 
        """
        result = self.order_model.query_order_count(params)
        if not result:
            return False
        else:
            return True

    def cal_fare_money(self, params):
        """
        计算运费
        :param params: 
        :return: 
        """
        total_fare_money = 0
        # 查询运费模板
        fare_result = self.do_service('goods.service.faretmplt_service', 'query_faretmplt_list',
                                      {'faretmplt_no_list': [goods['logistics_template_id'] for goods in params['goods_list']]})
        if fare_result['code'] != 0:
            return self._e('ORDER_FARE_MONEY_ERROR')
        # 构建运费计算对象
        for goods in params['goods_list']:
            fare_result['data'][int(goods['logistics_template_id'])]['goods_nums'] += goods['buy_vol']
        for key, value in fare_result['data'].items():
            if int(params['city_no']) in value:
                fare = value[int(params['city_no'])]
                goods_nums = value['goods_nums']
                # # 首n件
                # fare['init_num']
                # # 首n件运费
                # fare['init_fare']
                # # 续n件
                # fare['incre_num']
                # # 续n件运费
                # fare['incre_fare']
                """
                案例说明
                已知:首1件，首一件5元运费，续2件，续2件运费8元，商品数量为6
                解:
                    首1件，5元。剩余5件，则满足三次续2件，则3次续2件的运费为8 * 3 = 24,
                    5 + 24 = 29
                """

                total_fare_money += fare['init_fare']
                goods_nums -= fare['init_num']
                if goods_nums <= 0:
                    continue
                else:
                    length = (goods_nums / int(fare['incre_num'])) + 1
                    count = 0
                    while count < length:
                        count += 1
                        total_fare_money += fare['incre_fare']
        result = self._e('SUCCESS')
        result['data'] = total_fare_money
        return result
