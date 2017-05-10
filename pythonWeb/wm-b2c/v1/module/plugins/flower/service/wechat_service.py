# -*- coding:utf-8 -*-

"""
微信支付服务
@author: onlyfu
@time: 4/27/2017
"""
from base.service import ServiceBase
from module.plugins.flower.conf.mini_conf import CONF
import xmltodict
import hashlib
import requests


class Service(ServiceBase):

    def get_prepay_id(self, params):
        """
        获取预支付ID
        :param params: 支付参数，必须要值：
            body: 订单说明
            out_trade_no: 订单号
            total_fee: 订单支付金额
            spbill_create_ip: IP地址
            openid: 用户微信openid
        :return: 
        """
        # 检查参数
        if 'out_trade_no' not in params or 'total_fee' not in params \
                or 'spbill_create_ip' not in params or 'body' not in params or 'openid' not in params:
            return self._e('PAY_PARAMS_NOT_ERROR')

        request_params_key_list = [
            'appid',
            'mch_id',
            'nonce_str',
            'body',
            'out_trade_no',
            'total_fee',
            'spbill_create_ip',
            'notify_url',
            'trade_type',
            'openid'
        ]
        request_params_key_list.sort()

        request_params_data = {
            'appid': CONF['app_id'],
            'mch_id': CONF['mch_id'],
            'nonce_str': self.create_uuid(),
            'body': params['body'].encode('utf-8'),
            'out_trade_no': params['out_trade_no'],
            'total_fee': params['total_fee'],
            'spbill_create_ip': params['spbill_create_ip'],
            'notify_url': self.properties.get("base", 'HOST') + 'api/v1/plugins/flower/wechat_pay/notify/',
            'trade_type': 'JSAPI',
            'openid': params['openid']
        }

        request_params_data_list = []
        for item in request_params_key_list:
            request_params_data_list.append(item + '=' + str(request_params_data[item]))

        params_str = "&".join(request_params_data_list) + "&key=" + CONF['mch_api_key']
        sign = self.md5(params_str).upper()
        request_params_data['sign'] = sign

        request_xml = ['<xml>']
        for (k, v) in request_params_data.items():
            request_xml.append('<' + k + '>' + str(v) + '</' + k + '>')
        request_xml.append('</xml>')

        r = self.requests.post(CONF['get_prepay_id_url'], data=''.join(request_xml))

        try:
            xml_data = xmltodict.parse(r.text)
        except Exception, e:
            print e
            return self._e('PAY_NOTIFY_XML_ERROR')

        xml_data = xml_data['xml']
        print xml_data

        if xml_data['return_code'] == 'SUCCESS' and xml_data['result_code'] == 'SUCCESS':
            # result = self.error_code.SUCCESS
            # result['data'] = xml_data['prepay_id']
            # appId=wxd678efh567hg6787&nonceStr=5K8264ILTKCH16CQ2502SI8ZNMTM67VS
            # &package=prepay_id=wx2017033010242291fcfe0db70013231072&signType=MD5&timeStamp=1490840662&key=qazwsxedcrfvtgbyhnujmikolp111111

            time_stamp = str(self.time.time()).split('.')[0]
            pay_sign_list = [
                'appId=' + CONF['app_id'],
                'nonceStr=' + xml_data['nonce_str'],
                'package=prepay_id=' + xml_data['prepay_id'],
                'signType=MD5',
                'timeStamp=' + time_stamp,
                'key=' + CONF['mch_api_key']
            ]
            print '&'.join(pay_sign_list)
            pay_sign = self.md5('&'.join(pay_sign_list))
            result = self._e('SUCCESS')
            result['data'] = {
                    'prepay_id': xml_data['prepay_id'],
                    'nonce_str': xml_data['nonce_str'],
                    'time_stamp': time_stamp,
                    'sign': pay_sign
                }
            return result
        else:
            return self._e('PAY_PREPAY_ID_ERROR')

    if __name__ == '__main__':
        request_params_key_list = [
            'appid',
            'mch_id',
            'nonce_str',
            'body',
            'out_trade_no',
            'total_fee',
            'spbill_create_ip',
            'notify_url',
            'trade_type',
            'openid'
        ]
        request_params_key_list.sort()

        request_params_data = {
            'appid': CONF['app_id'],
            'mch_id': CONF['mch_id'],
            'nonce_str': 'nonce_str',
            'body': 'body',
            'out_trade_no': 'out_trade_no',
            'total_fee': '1',
            'spbill_create_ip': '127.0.0.1',
            'notify_url': 'notify_url',
            'trade_type': 'JSAPI',
            'openid': 'oyfjq0NbvbBo10CYxe82RpAFV5pg'
        }

        request_params_data_list = []
        for item in request_params_key_list:
            request_params_data_list.append(item + '=' + request_params_data[item])

        params_str = "&".join(request_params_data_list) + "&key=" + CONF['mch_api_key']
        sign = hashlib.md5(params_str).hexdigest().upper()
        request_params_data['sign'] = sign

        request_xml = ['<xml>']
        for (k, v) in request_params_data.items():
            request_xml.append('<' + k + '>' + v + '</' + k + '>')
        request_xml.append('</xml>')
        r = requests.post(CONF['get_prepay_id_url'], ''.join(request_xml))

        print r.text

