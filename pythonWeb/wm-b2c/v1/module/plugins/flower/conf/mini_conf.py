# -*- coding:utf-8 -*-

"""
@author: delu
@file: mini_conf.py
@time: 17/4/25 上午11:05
"""
CONF = {
    'app_id': 'wxcabb7405816fa0f7',
    'app_secret': 'a4a382593ef29d232aca55a3ea261ac4',
    'mch_id': '1217992201',
    'mch_app_id': 'wx828cdea70d986606',
    'mch_app_secret': '5541b1334753fe24a9a6e0ccec40ae51',
    'mch_api_key': '63ad41676cfa7d2dce6075d0bc6c704c',
    # code  失效时间1个半小时
    'code_expire_seconds': 5400,
    # 获取sessionKey
    'get_sessionkey_url': 'https://api.weixin.qq.com/sns/jscode2session?'
                          'appid=wxcabb7405816fa0f7'
                          '&secret=a4a382593ef29d232aca55a3ea261ac4'
                          '&js_code=${js_code}'
                          '&grant_type=authorization_code',
    # 获取
    'get_prepay_id_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder',
    # 获取access_token
    'get_access_token': 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
                        '&appid=wxcabb7405816fa0f7&secret=a4a382593ef29d232aca55a3ea261ac4',
    # 发送模板消息
    'send_model_message_url': 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?'
                              'access_token=${access_token}',
    # 活动预热模板内容
    'activity_content': '{"touser":"${open_id}", '
                        '"template_id":"7d0XZRTd_pLYGs2M1k83VmFKHBlBWEKc6OH6H0hKcDA", '
                        '"page":"/pages/index/index", "form_id":"${form_id}", '
                        '"data":{"keyword1":{"value":"${goods_name}", "color":"#173177"}, '
                        '"keyword2":{"value":"{{商品名称}}将在 5 分钟后开始抢购！", "color":"#173177"}, '
                        '"keyword3":{"value":"${start_time}", "color":"#173177"}, '
                        '"keyword4":{"value":"location", "color":"#173177"} }}'
}
