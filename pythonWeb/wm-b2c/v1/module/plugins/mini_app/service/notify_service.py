# -*- coding:utf-8 -*-

"""
支付回调service
@author: onlyfu
@time: 4/27/2017
"""
from base.service import ServiceBase
import xmltodict


class Service(ServiceBase):

    order_model = None

    def __init__(self):
        self.order_model = self.import_model('order.model.order_model')

    def notify(self, params):
        """
        回调通知
        :param xml: 
        :return: 
        """
        try:
            xml_data = xmltodict.parse(params['xml'])
        except Exception, e:
            print e
            return self._e('PAY_NOTIFY_XML_ERROR')

        xml_data = xml_data['xml']
        print xml_data

        if xml_data['return_code'] == 'SUCCESS':
            # 支付成功
            # 检查订单状态
            params = {
                'order_id': xml_data['out_trade_no']
            }
            order = self.do_service('order.service.order_query_service', 'query_order', params=params)
            if order['code'] == 1002:
                return order
            else:
                order_data = order['data'][0]
                if order_data['order_status'] != 1:
                    return self._e('ORDER_STATUS_ERROR')
                #
                data = {
                    'payment': {
                        'payorder_id': self.create_uuid(),
                        'shop_id': order_data['shop_id'],
                        'order_id': xml_data['out_trade_no'],
                        'pay_type': self.constants.PAY_TYPE_WECHAT,
                        'paysub_type': self.constants.PAY_SUB_TYPE_WECHAT,
                        'money_unit': order_data['money_unit'],
                        'money_total': xml_data['total_fee'],
                        'trade_no': xml_data['transaction_id'],
                    },
                    'order_data': {
                        'order_id': xml_data['out_trade_no'],
                        'order_status': self.constants.ORDER_PAY_SUCCESS
                    }
                }
                return self.order_model.pay_success(data)

