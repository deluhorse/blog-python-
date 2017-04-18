#!usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import random
import time
import math
import string

from source.controller import Controller
from source.redisbase import RedisBase
import conf.config as config
from tools.date_json_encoder import CJsonEncoder
from tools.wmb2c_string_util import StringUtils
from source.service_manager import ServiceManager as serviceManager
from constants.cachekey_predix import CacheKeyPredix


class Base(Controller):
    """ 基类
    """
    signPass = True  # 是否通过签名验证
    isAuth = False  # 是否使用登录验证
    json = json
    time = time
    logged_user = {}
    redis = RedisBase().get_conn()
    user_data = {}
    version = config.CONF['version']
    cache_key_predix = CacheKeyPredix

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

    def auth(self):
        """ 
        登录认证
        读取cookie值，判断是否登录

        @params strUserName string 用户名
        """

        if not self.current_user['user_id']:
            self.redirect(self.config['login_url'])
            return
        else:
            self.login_user()

    def auth_second(self):
        """ 
        登录认证
        读取cookie值，判断是否具有权限

        @params strUserName string 用户名
        """
        token = self.get_secure_cookie('token')

        if token is None:
            return False

        cache_key = self.md5(token)

        user_data = self.redis.get(cache_key)

        if user_data is None:
            return False
        user_data = eval(user_data)
        self.user_data = user_data

        if 'user_type' in user_data:
            if user_data['user_type'] in self.user_type or user_data['user_type'] == 'super_admin':
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

    def salt(self, salt_len=6 , is_num=False):
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

    def out(self, status_code, msg='', data={}):
        """ 
        输出结果
        @:param status_code 状态值
        @:param msg 说明文字
        @:param data 返回数据字典
        """
        out = {
            'status': status_code,
            'msg': msg,
            'data': data
        }

        self.write(json.dumps(out, cls=CJsonEncoder, ensure_ascii=False))

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
                num = int(math.ceil(float(page/10) + 1 if page/10 == 1 else float(page)/10) - 1)
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

    def get_current_user(self):
        """ 
        获取cookie值
        """
        user_id = self.get_secure_cookie('user_id')
        user_id = int(user_id) if user_id else 0

        return {
            'user_id': user_id,
            'nickname': self.get_secure_cookie('user_nickname'),
            'avatar': self.get_avatar_url(self.get_secure_cookie('user_avatar'))
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

        if self.isAuth:
            self.auth()

        if not self.signPass:
            return

        if self.user_type is None:
            if not self.auth_second():
                self.out(1006, '用户无权限')
                return

        Controller.get(self)

    def post(self):
        """ 
        重写父类post方法，接受POST请求
        增加登录验证判断
        固定参数a，如果a有值，调用同名方法，如果a没有值，调用index方法
        """

        if self.isAuth:
            self.auth()

        if not self.signPass:
            return

        if StringUtils.is_not_empty(self.user_type):
            if not self.auth_second():
                self.out(1006, '用户无权限')
                return

        Controller.post(self)

    def do_service(self, service_path, method, params={}):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        return serviceManager.do_service('user.user_service', 'create', params=params, version=config.CONF['version'])

