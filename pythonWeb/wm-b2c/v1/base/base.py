#!usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import math
import random
import string
import time

import conf.config as config
from constants.cachekey_predix import CacheKeyPredix
from constants.constants import Constants
from constants.error_code import Code
from source.controller import Controller
from source.properties import properties as properties
from source.redisbase import RedisBase
from source.service_manager import ServiceManager as serviceManager
from tools.common_util import CommonUtil
from tools.date_json_encoder import CJsonEncoder


class Base(Controller):
    """ 基类
    """
    json = json
    time = time
    logged_user = {}
    redis = RedisBase()
    user_data = {}
    buyer_user_data = {}
    version = config.CONF['version']
    cache_key_predix = CacheKeyPredix
    error_code = Code
    constants = Constants
    properties = properties
    auth = None

    def initialize(self):
        """ 
        初始化
        初始化数据类
        """
        Controller.config = config.CONF
        Controller.initialize(self)
        self.view_data['title'] = self.config['title']

        # 用户登录信息
        # self.login_user()

    def login_user(self):
        """ 
        获取用户登录信息
        """

        self.logged_user = self.current_user

        self.view_data['login_user'] = self.logged_user

    def auth_second(self):
        """ 
        登录认证
        读取cookie值，判断是否具有权限

        @params strUserName string 用户名
        """
        token = self.get_cookie('token')
        buyer_token = self.get_cookie('buyer_token')
        if not buyer_token:
            buyer_token = self.params('buyer_token')
        if not token:
            token = self.params('token')

        # 如果管理员的登录信息不存在，则验证买家的登录信息
        if token:
            cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(token)
            redis = self.redis.get_conn()
            user_data = redis.hgetall(cache_key)
            if user_data:
                self.user_data = user_data
                if 'user_type' in user_data:
                    if not self.auth[0] or user_data['user_type'] in self.auth[0] or user_data[
                        'user_type'] == 'super_admin':
                        return True
        if buyer_token:
            buyer_cache_key = self.cache_key_predix.BUYER_TOKEN + self.md5(buyer_token)
            redis = self.redis.get_conn()
            user_data = redis.hgetall(buyer_cache_key)
            if user_data:
                self.user_data = user_data
                if 'user_type' in user_data:
                    if not self.auth[0] or user_data['user_type'] in self.auth[0] or user_data[
                        'user_type'] == 'super_admin':
                        return True

        return False

    def auth_request(self, request_type):
        """
        请求类型检查
        :param request_type: 请求类型
        :return: 
        """
        if not self.auth[1] or request_type in self.auth:
            return True

        return False

    def api_sign(self, data, post_url):
        """ 
        API签名请求
        @params dic_data dict 发送数据字典
        @params str_post_url string 请求地址
        """

        # 将数据json
        data = self.json.dumps(data)

        # 生成请求时间
        request_time = str(self.time.time())

        # 进行签名加密
        sign = self.md5('%s%s%s' % (data, request_time, self.config['bag_api_key']))

        # 发送请求
        response = self.request(post_url, 'POST', {'data': data, 'tamp': request_time, 'hash': sign})
        # print strResult.encode('utf8')

        try:
            result = self.json.loads(response)
        except Exception, e:
            print e
            return False

        return result

    def md5(self, text):
        """ 
        MD5加密
        @:param text 需加密字符串
        @return 加密后字符串
        """
        result = hashlib.md5(text)
        return result.hexdigest()

    def create_uuid(self):
        """
        声称随机字符串
        :return: 
        """
        m = hashlib.md5()
        m.update(bytes(str(time.time()), encoding='utf-8'))
        return m.hexdigest()

    def create_random_text(self, number):
        """
        创建随机定长字符串
        :param number: 
        :return: 
        """
        salt = ''.join(random.sample(string.ascii_letters + string.digits, number))

        return salt

    def sha1(self, text):
        """ 
        sha1 加密
        @:param text 需加密字符串
        @return 加密后字符串
        """
        return hashlib.sha1(text).hexdigest()

    def salt(self, salt_len=6, is_num=False):
        """ 
        密码加密字符串
        生成一个固定位数的随机字符串，包含0-9a-z
        @:param salt_len 生成字符串长度
        """

        if is_num:
            chrset = '0123456789'
        else:
            chrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        salt = []
        for i in range(salt_len):
            item = random.choice(chrset)
            salt.append(item)

        return ''.join(salt)

    def out(self, data):
        """ 
        输出结果
        :param code: 错误信息对象
        :param data: 返回数据字典
        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self.json.dumps(data, cls=CJsonEncoder))

    def error_out(self, error, data={}):
        """
        错误输出
        :param error: 错误信息对象
        :param data: 返回数据字典
        :return: 
        """
        out = error
        if data:
            out['data'] = data

        self.write(out)

    def page(self, page, page_data_num, data_count, page_url):
        """ 
        分页处理
        @:param page 当前页码
        @:param page_data_num 每页多少条数据
        @:param data_count 共有多少条数据
        @:param page_url 分页链接
        <nav>
            <ul class="pagination pull-right">
                <li><a href="#">&laquo;</a></li>
                <li class="active"><a href="#">1</a></li>
                <li><a href="#">2</a></li>
                <li><a href="#">3</a></li>
                <li><a href="#">4</a></li>
                <li><a href="#">5</a></li>
                <li><a href="#">&raquo;</a></li>
            </ul>
        </nav>
        """
        page_html = []
        page_count = int(math.ceil(float(data_count) / float(page_data_num)))

        if page_count > 1:
            page_html.append('<nav><ul class="pagination">')
            if page > 1:
                page_html.append('<li><a href="%s&page=%d">&laquo;</a></li>' % (page_url, 1))

            if page_count < 10:
                for i in range(1, page_count + 1):
                    class_name = 'active' if i == page else ''
                    page_num = '<li class="%s"><a href="%s&page=%d">%d</a></li>' % (class_name, page_url, i, i)
                    page_html.append(page_num)
            else:
                num = int(math.ceil(float(page / 10) + 1 if page / 10 == 1 else float(page) / 10) - 1)
                if num == 0:
                    start_page_num = 1
                    end_page_num = 9 if page_count >= 9 else page_count
                else:
                    start_page_num = num * 10
                    end_page_num = num * 10 + 9 if page_count >= (num * 10 + 9) else page_count
                    more_pre_page_num = start_page_num - 1
                    page_html.append('<li><a href="%s&page=%d">...</a></li>' % (page_url, more_pre_page_num))

                for i in range(start_page_num, end_page_num + 1):
                    class_name = 'active' if i == page else ''
                    page_num = '<li class="%s"><a href="%s&page=%d">%d</a></li>' % (class_name, page_url, i, i)
                    page_html.append(page_num)

                if page_count >= (num * 10 + 9):
                    more_next_page_num = end_page_num + 1
                    page_html.append('<li><a href="%s&page=%d">...</a></li>' % (page_url, more_next_page_num))

            if page < page_count:
                page_html.append('<li><a href="%s&page=%d">&raquo;</a></li>' % (page_url, page_count))

            page_html.append('</ul></nav>')

        return ''.join(page_html)

    def format_time(self, timestamp, time_format='%Y-%m-%d %H:%I:%M'):
        """ 
        将时间戳格式化为时间
        """
        return self.time.strftime(time_format, self.time.localtime(timestamp))

    def time_to_str(self, date):
        """ 
        将日期时间转为时间戳
        @:param strDate 日期时间
        """
        return self.time.mktime(date.timetuple())

    def time_now(self):
        """
        获取当前时间，yyyy-mm-dd H:i:s
        :return: 
        """
        return self.format_time(time.time())

    def get_current_user(self):
        """ 
        获取cookie值
        """
        user_id = self.get_cookie('user_id')
        user_id = int(user_id) if user_id else 0

        return {
            'user_id': user_id,
            'nickname': self.get_cookie('user_nickname'),
            'avatar': self.get_avatar_url(self.get_cookie('user_avatar'))
        }

    def get_avatar_url(self, code):
        """ 
        """
        return '%s%s%s' % (self.config['PIC']['HOST'], code, '-avatar')

    def clear_template_cache(self):
        """ 清除模板缓存
        """

        self._template_loaders.clear()

    def get(self, **params):
        """ 
        重写父类get方法，接受GET请求
        增加登录验证判断
        固定参数a，如果a有值，调用同名方法，如果a没有值，调用index方法
        """

        if self.auth:
            if self.auth[0] is not None:
                if not self.auth_second():
                    self.error_out(self._e('AUTH_ERROR'))
                    return

            if not self.auth_request("get"):
                self.error_out(self._e('REQUEST_TYPE_ERROR'))
                return

        # 刷新token
        self.refresh_token()
        Controller.get(self)

    def post(self):
        """ 
        重写父类post方法，接受POST请求
        增加登录验证判断
        固定参数a，如果a有值，调用同名方法，如果a没有值，调用index方法
        """
        if self.auth:
            if self.auth[0] is not None:
                if not self.auth_second():
                    self.error_out(self._e('AUTH_ERROR'))
                    return

            if not self.auth_request("post"):
                self.error_out(self._e('REQUEST_TYPE_ERROR'))
                return

        # 刷新token
        self.refresh_token()
        Controller.post(self)

    def do_service(self, service_path, method, params={}):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        token = self.get_cookie('token')
        buyer_token = self.get_cookie('buyer_token')
        language = self.get_cookie('language')
        if not token:
            token = self.params('token')
        if not buyer_token:
            buyer_token = self.params('buyer_token')
        if not language:
            language = self.params('language')
        params['token'] = token if token else ''
        params['buyer_token'] = buyer_token if buyer_token else ''
        params['language'] = language if language else 'cn'

        return serviceManager.do_service(service_path, method, params=params, version=config.CONF['version'])

    def create_cookie_and_token(self, params={}):
        """
        创建cookie 和 token 记录用户登录信息
        :param params: 
        :return: 
        """
        params = CommonUtil.remove_element(params, ['salt', 'password'])

        admin_token = self.cache_key_predix.ADMIN_TOKEN + self.salt(salt_len=32)
        cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(admin_token)
        # 新增
        params['user_type'] = self.constants.ADMIN_TYPE
        redis = self.redis.get_conn()
        redis.hmset(cache_key, params)
        redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))
        self.set_cookie('token', admin_token)

        print 'token: %s, cache_key: %s' % (admin_token, cache_key)
        return {'token': admin_token}

    def update_cookie_and_token(self, params={}):
        """
        更新cookie 和 token 记录用户登录信息
        :param params: 
        :return: 
        """

        token = self.get_cookie('token')
        if not token:
            token = self.params('token')
        cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(token)
        redis = self.redis.get_conn()
        cache_value = redis.hgetall(cache_key)
        if 'shop_id' in params:
            cache_value['shop_id'] = params['shop_id']
            cache_value['user_type'] = self.constants.SELLER_TYPE
            redis.delete(cache_key)
            redis.hmset(cache_key, cache_value)
            redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))
            self.set_cookie('token', token)

    def create_cookie_and_token_for_buyer(self, params={}):
        """
        创建cookie 和 token 记录买家登录信息
        :param params: 
        :return: 
        """

        buyer_token = self.cache_key_predix.BUYER_TOKEN + self.salt(salt_len=32)
        buyer_cache_key = self.cache_key_predix.BUYER_TOKEN + self.md5(buyer_token)
        # 新增
        params['user_type'] = self.constants.BUYER_TYPE
        redis = self.redis.get_conn()
        redis.hmset(buyer_cache_key, params)
        if 'scen_type' in params and params['scen_type'] == self.constants.SCEN_TYPE_WECHAT:
            # 如果是微信登录，则采用微信过期时间
            redis.expire(buyer_cache_key, params['expire'])
            self.set_cookie('buyer_token', buyer_token)
        else:
            redis.expire(buyer_cache_key, int(self.properties.get('expire', 'BUYER_EXPIRE')))
            self.set_cookie('buyer_token', buyer_token)
        print 'buyer_token: %s, cache_key: %s' % (buyer_token, buyer_cache_key)
        return {'buyer_token': buyer_token}

    def quit_shop(self):
        """
        店铺管理员退出
        :param params: 
        :return: 
        """
        token = self.get_cookie('token')
        if not token:
            token = self.params('token')
        cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(token)
        redis = self.redis.get_conn()
        cache_value = redis.hgetall(cache_key)
        cache_value = CommonUtil.remove_element(cache_value, ['shop_id'])
        cache_value['user_type'] = self.constants.ADMIN_TYPE
        redis.delete(cache_key)
        redis.hmset(cache_key, cache_value)
        redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))

    def refresh_token(self):
        """
        刷新token
        :return: 
        """
        token = self.get_cookie('token')
        buyer_token = self.get_cookie('buyer_token')
        if not token:
            token = self.params('token')
        if not buyer_token:
            buyer_token = self.params('buyer_token')

        redis = self.redis.get_conn()
        if token:
            cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(token)
            left_seconds = int(redis.ttl(cache_key))
            # 获取用户登录数据
            self.user_data = redis.hgetall(cache_key)
            if (int(self.properties.get('expire', 'ADMIN_EXPIRE')) - left_seconds) >= \
                    int(self.properties.get('expire', 'ADMIN_REFRESH_EXPIRE')):
                # 如果token的总生命秒数 － 剩余生命秒数 <= 刷新秒数，则重新设置token的生命秒数
                redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))
        if buyer_token:
            buyer_cache_key = self.cache_key_predix.BUYER_TOKEN + self.md5(buyer_token)
            left_seconds = int(redis.ttl(buyer_cache_key))
            # 获取用户登录数据
            self.buyer_user_data = redis.hgetall(buyer_cache_key)
            if (int(self.properties.get('expire', 'BUYER_EXPIRE')) - left_seconds) >= \
                    int(self.properties.get('expire', 'BUYER_REFRESH_EXPIRE')):
                # 如果token的总生命秒数 － 剩余生命秒数 <= 刷新秒数，则重新设置token的生命秒数
                redis.expire(buyer_cache_key, int(self.properties.get('expire', 'BUYER_EXPIRE')))

    def delete_token(self):
        """
        删除token
        :return: 
        """
        token = self.get_cookie('token')
        if not token:
            token = self.params('token')

        if token:
            cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(token)
            redis = self.redis.get_conn()
            redis.delete(cache_key)
            self.clear_cookie('token')

    def _e(self, error_key):
        """
        :param params: 
        :return: 
        """
        language = self.get_cookie('language')
        if not language:
            language = self.params('language')
        language = language if language else 'cn'
        language_module = self.importlib.import_module('language.' + language).Code
        data = {}
        for key in self.error_code[error_key]:
            data[key] = self.error_code[error_key][key]
        if error_key in language_module:
            data['msg'] = language_module[error_key]

        return data


if __name__ == '__main__':
    result = hashlib.md5('buyer_token_dSObQNpGGukKcq7w95YAH2bhBRLNGhxn')
    print CacheKeyPredix.BUYER_TOKEN + result.hexdigest()
