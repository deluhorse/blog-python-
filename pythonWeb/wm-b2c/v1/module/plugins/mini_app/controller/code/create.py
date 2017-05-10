# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 17/4/25 上午11:08
"""
from v1.base.base import Base
from v1.module.plugins.mini_app.conf.mini_conf import CONF


class Controller(Base):

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'code': self.params('code')
        }
        res = self.do_service('plugins.mini_app.service.mini_app_service', 'get_sesstionkey', params=params)
        buyer_token = {}
        if res['code'] == 0:
            # 创建sessionkey的缓存，同时生成buyer_token
            res['data']['scen_type'] = self.constants.SCEN_TYPE_WECHAT
            res['data']['scen_id'] = CONF['app_id']
            res['data']['expire'] = CONF['code_expire_seconds']
            res['data']['buyer_id'] = res['data']['openid']
            res['data']['mobile_no'] = ''
            result = self.do_service('buyer.service.buyer_service', 'create_buyer', res['data'])
            if result['code'] == 0:
                buyer_token = self.create_cookie_and_token_for_buyer(res['data'])
                res['data'] = buyer_token
            else:
                res = result
        self.out(res)
