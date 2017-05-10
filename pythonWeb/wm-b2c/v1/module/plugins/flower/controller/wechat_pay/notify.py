# -*- coding:utf-8 -*-

"""
微信支付回调
@author: onlyfu
@time: 4/27/2017
"""
from base.base import Base


class Controller(Base):

    def initialize(self):
        Base.initialize(self)

    def index(self):

        params = {
            'xml': self.request.body
        }

        res = self.do_service('plugins.flower.service.notify_service', 'notify', params=params)
        if res['code'] == 0:
            self.write('<xml><return_code><![CDATA[SUCCESS]]>'
                       '</return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
        else:
            self.write('notify failed')
