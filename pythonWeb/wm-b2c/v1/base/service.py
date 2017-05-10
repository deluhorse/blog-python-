# -*- coding:utf-8 -*-

import hashlib
import json
import random
import time
import datetime
import importlib
import tornado.escape
import requests

import conf.config as config
from constants.constants import Constants
from constants.error_code import Code
from constants.cachekey_predix import CacheKeyPredix
from source.properties import properties
from source.redisbase import RedisBase
from source.service_manager import ServiceManager as serviceManager
from tools.httputils import HttpUtils
from tools.schedule_utils import ScheduleUtils
from tools.date_utils import DateUtils
from tools.common_util import CommonUtil


class ServiceBase(object):
    dicConfig = config.CONF
    time = time
    datetime = datetime
    json = json
    hashlib = hashlib
    constants = Constants
    error_code = Code
    cache_key_predix = CacheKeyPredix
    requests = requests
    properties = properties
    redis = RedisBase()
    httputils = HttpUtils
    schedule_utils = ScheduleUtils
    date_utils = DateUtils
    common_utils = CommonUtil

    def md5(self, text):
        """
        md5加密
        :param text: 
        :return: 
        """
        result = hashlib.md5(text)
        return result.hexdigest()

    def import_model(self, model_name):
        """
        加载数据类
        :param model_name: string 数据类名
        :return: 
        """
        try:
            model = importlib.import_module('module.' + model_name)
            return model.Model()
        except Exception, e:
            print e
            return None

    def salt(self, salt_len=6):
        """
        随机字符串
        :param salt_len: int 字符串长度
        :return: 
        """
        chrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        chrset_list = []
        for i in range(salt_len):
            item = random.choice(chrset)
            chrset_list.append(item)

        return ''.join(chrset_list)

    def create_uuid(self):
        """
        声称随机字符串
        :return: 
        """
        m = hashlib.md5()
        m.update(bytes(str(time.time()) + self.salt(12)))
        return m.hexdigest()

    def escape_string(self, data, un=None):
        """
        特殊字符转义
        :param data: string, tuple, list, dict 转义数据
        :param un: 
        :return: 
        """
        if isinstance(data, str):
            return tornado.escape.xhtml_escape(data) if not un else tornado.escape.xhtml_unescape(data)
        elif isinstance(data, tuple) or isinstance(data, list):
            lisData = []
            for item in data:
                lisData.append(
                    tornado.escape.xhtml_escape(str(item)) if not un else tornado.escape.xhtml_unescape(str(item)))

            return lisData
        elif isinstance(data, dict):
            for key in data:
                data[key] = tornado.escape.xhtml_escape(str(data[key])) if not un else tornado.escape.xhtml_unescape(
                    str(data[key]))

            return data

    def do_service(self, service_path, method, params={}):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        return serviceManager.do_service(service_path, method, params=params, version=config.CONF['version'])

    def _e(self, error_key):
        """
        :param error_key: 
        :return: 
        """
        data = {}
        for key in self.error_code[error_key]:
            data[key] = self.error_code[error_key][key]
        if error_key in self.language_code:
            data['msg'] = self.language_code[error_key]

        return data


if __name__ == '__main__':
    string = "G110"

    print string[0]
