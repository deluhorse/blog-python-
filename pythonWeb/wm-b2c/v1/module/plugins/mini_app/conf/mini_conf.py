# -*- coding:utf-8 -*-

"""
@author: delu
@file: mini_conf.py
@time: 17/4/25 上午11:05
"""
CONF = {
    'app_id': 'wx4eaece735a1b888b',
    'app_secret': '2c36cefa18f59f06a728555ac59b066d',
    'mch_id': '1217992201',
    'mch_app_id': 'wx828cdea70d986606',
    'mch_app_secret': '5541b1334753fe24a9a6e0ccec40ae51',
    'mch_api_key': '63ad41676cfa7d2dce6075d0bc6c704c',
    # code  失效时间1个半小时
    'code_expire_seconds': 5400,
    # 获取sessionKey
    'get_sessionkey_url': 'https://api.weixin.qq.com/sns/jscode2session?'
                          'appid=wx4eaece735a1b888b'
                          '&secret=2c36cefa18f59f06a728555ac59b066d'
                          '&js_code=${js_code}'
                          '&grant_type=authorization_code',
    # 获取
    'get_prepay_id_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder',
    # 获取access_token
    'get_access_token': 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
                        '&appid=wx4eaece735a1b888b&secret=2c36cefa18f59f06a728555ac59b066d',
    # 发送模板消息
    'send_model_message_url': 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?'
                              'access_token=${access_token}',
    # 活动预热模板内容
    'activity_content': '{"touser":"${open_id}", '
                        '"template_id":"7d0XZRTd_pLYGs2M1k83VmFKHBlBWEKc6OH6H0hKcDA", '
                        '"page":"", "form_id":"${form_id}", '
                        '"data":{"keyword1":{"value":"${goods_name}", "color":"#173177"}, '
                        '"keyword2":{"value":"{{商品名称}}将在 5 分钟后开始抢购！", "color":"#173177"}, '
                        '"keyword3":{"value":"${start_time}", "color":"#173177"}, '
                        '"keyword4":{"value":"location", "color":"#173177"} }}'
}
