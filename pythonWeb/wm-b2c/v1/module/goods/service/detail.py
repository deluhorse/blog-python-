# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 4/28/2017
"""
from base.service import ServiceBase


class Service(ServiceBase):

    goods_model = None
    images_model = None

    def __init__(self):
        self.goods_model = self.import_model('goods.model.goods_model')
        self.images_model = self.import_model('user.model.images.images_model')

    def detail(self, params):
        """
        查询商品详情
        :param params: dict 参数
            dict['goods_id']或dict['sku_id'] 必须要一个有值
        :return: 
        """
        # 检查参数
        # error_code = self.error_code.GOODS_PARAMS_ERROR
        return_data = self._e('GOODS_PARAMS_ERROR')

        if 'id' not in params:
            return_data['msg'] = "id不能为空"
            return return_data

        goods_id = params['id'].upper()
        goods_type = goods_id[0]

        if goods_type == 'G':
            data = self.goods_model.query_goods(params['id'])
        elif goods_type == 'S':
            data = self.goods_model.query_one_sku(params['id'])
        else:
            return_data['msg'] = "id格式错误"
            return return_data

        if not data:
            return self._e('GOODS_NOT_FIND')

        result = self._e('SUCCESS')
        result['data'] = {
            'goods_id': data['goods_id'],
            'goods_name': data['goods_name'],
            'images': [],
            'pre_buy_time': data['pre_buy_time'],
            'sku_properties': {},
            'sku_data': {}
        }

        # 处理图片
        try:
            image_id_list = self.json.loads(data['images'])
            image_list = self.images_model.get_many(image_id_list)
            if image_list:
                for item in image_list:
                    image_host = self.properties.get('images', 'HOST_TYPE_' + str(item['host_type']))
                    result['data']['images'].append(image_host + item['img_key'])
        except Exception, e:
            print e

        # 获取所有sku
        sku_list = self.goods_model.query_goods_sku_by_goods_id(data['goods_id'])
        if sku_list:
            sku_properties = {}
            sku_data = {}
            for sku in sku_list:
                properties = self.json.loads(sku['properties']) if sku['properties'] else ''
                sku_id_list = []
                for item in properties:
                    if item['id'] not in sku_properties:
                        sku_properties[item['id']] = {}
                        sku_properties[item['id']]['value'] = []

                    sku_properties[item['id']]['name'] = item['name']
                    sku_properties[item['id']]['value'].append(item['value'])
                    sku_id_list.append(str(item['value']['id']))

                stock_list = self.do_service('goods.service.goods_service', 'get_sku_stock', params={'sku_id': [sku['sku_id']]})

                sku_data[":".join(sku_id_list)] = {
                    'sku_id': sku['sku_id'],
                    'price': sku['price'],
                    'origin_price': sku['origin_price'],
                    'stock': stock_list[0],
                    'img_id': sku['img_id'],
                }

            result['data']['sku_properties'] = sku_properties
            result['data']['sku_data'] = sku_data

        return result

