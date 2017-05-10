# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 4/25/2017
"""
from base.service import ServiceBase


class Service(ServiceBase):

    goods_model = None
    redis_conn = None

    def __init__(self):
        self.goods_model = self.import_model('goods.model.goods_model')
        self.redis_conn = self.redis.get_conn()

    def create(self, params):
        """
        创建商品
        :param params: dict 参数
            dict['shop_id'] 必须
            dict['goods_name'] 必须
            dict['sku_json'] 必须
            dict['images'] 必须
        :return: 
        """
        # 检查参数
        return_data = self._e('GOODS_PARAMS_ERROR')
        if 'admin_id' not in params:
            return_data['msg'] = "店铺ID不能为空"
            return return_data
        if 'goods_name' not in params:
            return_data['msg'] = "商品名称不能为空"
            return return_data

        try:
            sku_list = self.json.loads(params['sku_json'])
            if len(sku_list) == 0:
                return_data['msg'] = "sku不能为空"
                return return_data
        except Exception, e:
            print e
            return_data['msg'] = "sku数据格式错误，必须为json格式"
            return return_data

        try:
            images_list = self.json.loads(params['images'])
            if len(images_list) == 0:
                return_data['msg'] = "商品图片不能为空"
                return return_data
        except Exception, e:
            print e
            return_data['msg'] = "图片格式错误，必须为json格式"
            return return_data

        # 准备数据
        goods_id = self.create_goods_id()
        goods_data = {
            "admin_id": params['admin_id'],
            "goods": {
                "goods_id": goods_id,
                "goods_name": params['goods_name'],
                "images": params['images'],
                "pre_buy_time": "0"
            },
            "sku_list": [],
            "create_time": self.date_utils.time_now()
        }

        if 'pre_buy_time' in params:
            if params['pre_buy_time']:
                goods_data['goods']['pre_buy_time'] = self.date_utils.time_to_str(params['pre_buy_time'])

        for sku in sku_list:
            if 'price' not in sku:
                return_data['msg'] = "sku价格不能为空"
                return return_data
            if 'stock' not in sku:
                return_data['msg'] = "sku库存不能为空"
                return return_data

            stock = sku['stock'] if sku['stock'] else 0
            price = sku['price'] if sku['price'] else 0
            origin_price = sku['origin_price'] if 'origin_price' in sku else 0
            bar_code = sku['bar_code'] if 'bar_code' in sku else ''
            img_id = sku['img_id'] if 'img_id' in sku else ''
            sku_data = {
                "sku_id": self.create_sku_id(),
                "goods_id": goods_id,
                "stock": stock,
                "price": price,
                "origin_price": origin_price,
                "bar_code": bar_code,
                "img_id": img_id
            }
            if 'properties' in sku:
                sku_data['properties'] = self.json.dumps(sku['properties'])

            goods_data['sku_list'].append(sku_data)

        data = self.goods_model.create(goods_data)
        if data:
            # 设置库存
            redis = self.redis.get_conn()
            for sku in goods_data['sku_list']:
                sku_stock_cache_key = self.cache_key_predix.GOODS_SKU_STOCK + sku['sku_id']
                redis.set(sku_stock_cache_key, sku['stock'])
            return data
        else:
            return self._e('SQL_EXECUTE_ERROR')

    def get_sku(self, params):
        """
        获取sku信息
        :param params: 
        :return: 
        """
        if 'sku_id' not in params:
            return self._e('GOODS_PARAMS_ERROR')

        if isinstance(params['sku_id'], str):
            sku_id_list = params['sku_id'].split(',')
        elif isinstance(params['sku_id'], list):
            sku_id_list = params['sku_id']
        else:
            return self._e('GOODS_PARAMS_ERROR')

        sku_list = self.goods_model.query_goods_sku_by_sku_id(sku_id_list)
        if not sku_list:
            return self._e('GOODS_NOT_FIND')
        else:
            sku_list_result = []
            for sku in sku_list:
                stock_list = self.get_sku_stock([sku['sku_id']])
                sku_data = sku
                sku_data['stock'] = stock_list[0]
                sku_list_result.append(sku_data)

            result = self._e('SUCCESS')
            result['data'] = sku_list_result
            return result

    def decrease_sku_stock(self, params):
        """
        扣库存
        :param params: 
        :return: 
        """
        sku_id = params['sku_id']
        buy_vol = params['buy_vol']
        if not buy_vol:
            return self._e('GOODS_SKU_BUY_VOL_ERROR')

        cache_key = self.cache_key_predix.GOODS_SKU_STOCK + sku_id
        sku_stock = self.redis_conn.get(cache_key)
        if sku_stock < 0 or buy_vol > sku_stock:
            return self._e('GOODS_SKU_STOCK_NOT_ENOUGH')

        sku_stock_left = self.redis_conn.decr(cache_key, buy_vol)
        if sku_stock_left < 0:
            # 库存不足，将扣除的数据返回
            self.redis_conn.incrby(cache_key, buy_vol)
            return self._e('GOODS_SKU_STOCK_NOT_ENOUGH')
        else:
            return self._e('SUCCESS')

    def return_sku_stock(self, params):
        """
        还原库存
        :param params: 
        :return: 
        """
        sku_id = params['sku_id']
        buy_vol = params['buy_vol']
        if not buy_vol:
            return self._e('GOODS_SKU_BUY_VOL_ERROR')

        cache_key = self.cache_key_predix.GOODS_SKU_STOCK + sku_id
        self.redis_conn.incrby(cache_key, buy_vol)

    def get_sku_stock(self, params):
        """
        获取sku库存
        :param params: 
        :return: 
        """
        if isinstance(params, list):
            sku_id_list = params
        elif isinstance(params, dict):
            if 'sku_id' not in params:
                return self._e('GOODS_PARAMS_ERROR')

            if isinstance(params['sku_id'], list):
                sku_id_list = params['sku_id']
            else:
                return self._e('GOODS_PARAMS_ERROR')
        else:
            return self._e('GOODS_PARAMS_ERROR')

        cache_key_list = []
        for item in sku_id_list:
            cache_key_list.append(self.cache_key_predix.GOODS_SKU_STOCK + item)

        return_list = []
        stock_list = self.redis_conn.mget(cache_key_list)
        if stock_list:
            for stock in stock_list:
                return_list.append(stock if stock > 0 else 0)
        else:
            return_list = [0]

        return return_list

    def create_goods_id(self, cat_id='00'):
        """
        生成商品ID
        示例：G01M2CD78L，总长为10位，第一位为G，二三们为分类ID,后7位为随机字符串（字母+数字）
        :param cat_id: 分类ID
        :return: 
        """

        goods_id = 'G' + cat_id
        random_str = self.salt(7).upper()

        return goods_id + random_str

    def create_sku_id(self, cat_id='00'):
        """
        生成sku ID
        示例：S01M2CD78L，总长为10位，第一位为S，二三们为分类ID,后7位为随机字符串（字母+数字）
        :param cat_id: 分类ID
        :return: 
        """

        goods_id = 'S' + cat_id
        random_str = self.salt(7).upper()

        return goods_id + random_str
