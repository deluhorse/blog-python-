# -*- coding:utf-8 -*-

"""
@author: delu
@file: mini_app_service.py
@time: 17/4/25 上午11:09
"""
from base.service import ServiceBase
from module.plugins.flower.conf.mini_conf import CONF


class Service(ServiceBase):
    """
    mini_app_service
    """

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        pass

    def get_sesstionkey(self, params):
        """
        查询session_key 和open_id
        :param params: 
        :return: 
        """
        try:
            url = CONF['get_sessionkey_url'].replace('${js_code}', params['code'])
            print url
            result = self.requests.get(url)
            print result.text
            data = self.json.loads(result.text)
            if 'errcode' in data:
                return self._e('MINI_APP_GET_SESSIONKEY_ERROR')
            else:
                final_result = self._e('SUCCESS')
                final_result['data'] = data
                return final_result
        except Exception, e:
            print Exception, ':', e
            return self._e('MINI_APP_GET_SESSIONKEY_ERROR')

    def create_form_id(self, params):
        """
        创建form_id
        :param params: 
        :return: 
        """
        if 'form_id' not in params or not params['form_id'] or 'goods_id' not in params or not params['goods_id']:
            return self._e('MINI_APP_FORM_ID_NOT_EXIST')
        try:
            redis = self.redis.get_conn()
            redis.sadd(self.cache_key_predix.MINI_APP_MODEL_MESSAGE_USER + params['goods_id'], params['buyer_id'])
            redis.set(self.cache_key_predix.MINI_APP_MODEL_MESSAGE_USER + params['goods_id'] + '_' + params['buyer_id'],
                      params['form_id'])
            return self._e('SUCCESS')
        except Exception, e:
            print Exception, ':', e
            return self._e('CACHE_EXECUTE_ERROR')

    def send_model_message(self, params):
        """
        发送模版消息
        :param params: 
        :return: 
        """
        access_token = self.get_access_token()
        if not access_token:
            print 'access_token失效，无法发送模板消息'
            return
        send_model_message_url = CONF['send_model_message_url'].replace('${access_token}', access_token)
        redis = self.redis.get_conn()
        buyer_id_list = redis.smembers(self.cache_key_predix.MINI_APP_MODEL_MESSAGE_USER + params['goods_id'])
        for buyer_id in buyer_id_list:
            # 遍历set发送模板消息
            try:
                form_id = self.json.loads(redis.get(self.cache_key_predix.MINI_APP_MODEL_MESSAGE_USER
                                                    + params['goods_id'] + '_' + buyer_id))
                redis.delete(self.cache_key_predix.MINI_APP_MODEL_MESSAGE_USER + params['goods_id'] + '_' + buyer_id)
                post_params = self.json.loads(CONF['activity_content'])
                post_params['touser'] = buyer_id
                post_params['form_id'] = form_id
                post_params['data']['keyword1']['value'] = params['goods_name']
                goods_name = params['goods_name'].encode('utf-8') + '将在 5 分钟后开始抢购!'
                post_params['data']['keyword2']['value'] = goods_name

                my_timestamp = self.date_utils.str_to_time(params['activity_start_time'])
                post_params['data']['keyword3']['value'] = \
                    self.date_utils.format_time(my_timestamp, time_format='%Y年%m月%d日 %H:%M')
                post_params['start_time'] = params['activity_start_time']

                self.httputils.do_post(send_model_message_url, post_params, {'Content-Type': 'application/json'})
            except Exception, e:
                print Exception, ':', e
        redis.delete(self.cache_key_predix.MINI_APP_MODEL_MESSAGE_USER + params['goods_id'])

    def create_activity(self, params):
        """
        创建闪购schedule
        :param params: 
        :return: 
        """
        if 'goods_id' not in params or not params['goods_id']:
            return self._e('MINI_APP_ACTIVITY_GOODS_ID')
        params['id'] = params['goods_id']
        # 查询商品信息
        result = self.do_service('goods.service.detail', 'detail', params)
        if result['code'] != 0:
            return self._e('SQL_EXECUTE_ERROR')

        start_time = self.date_utils.format_time(result['data']['pre_buy_time'])
        # 创建schedule
        return self.schedule_utils.add_job({
            'service_path': 'plugins.mini_app.service.mini_app_service',
            'method': 'send_model_message',
            'start_time': self.date_utils.add_minute(start_time, format_date='%Y-%m-%d %H:%M:%S',
                                                     minutes=-1 * params['limit_time']),
            'goods_id': params['goods_id'],
            'goods_name': result['data']['goods_name'],
            'activity_start_time': start_time
        })

    def get_access_token(self):
        """
        获取小程序access_token
        :param params: 
        :return: 
        """
        redis = self.redis.get_conn()
        access_token = redis.get(self.cache_key_predix.MINI_APP_ACCESS_TOKEN)

        if not access_token:
            # 如果access_token失效，则重新请求
            res = self.json.loads(self.httputils.do_get(CONF['get_access_token']))
            if 'access_token' in res:
                redis.set(self.cache_key_predix.MINI_APP_ACCESS_TOKEN, res['access_token'])
                redis.expire(self.cache_key_predix.MINI_APP_ACCESS_TOKEN, 5400)
                return res['access_token']
            else:
                return None
        else:
            return access_token


if __name__ == '__main__':

    my_service = Service()
    # my_service.send_model_message({'goods_id': 'gd11'})
    # post_params = my_service.json.loads(CONF['activity_content'])
    # print post_params

    # my_timestamp = my_service.date_utils.str_to_time('2017-05-02 16:00:00')
    # print my_service.date_utils.format_time(my_timestamp, time_format='%Y年%m月%d日 %H:%M')
    # redis = my_service.redis.get_conn()
    #
    # buyer_id_list = redis.smembers(my_service.cache_key_predix.MINI_APP_MODEL_MESSAGE_USER + 'gd11')
    #
    # for buyer_id in buyer_id_list:
    #     print redis.delete(my_service.cache_key_predix.MINI_APP_MODEL_MESSAGE_USER
    #                        + 'gd11' + '_' + buyer_id)
    my_goods = u'试试'
    goods_name = u'%s将在 5 分钟后开始抢购！' % my_goods
    print goods_name