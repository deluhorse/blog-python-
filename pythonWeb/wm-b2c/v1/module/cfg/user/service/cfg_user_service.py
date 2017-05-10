# -*- coding:utf-8 -*-

"""
@author: delu
@file: cfg_user_service.py
@time: 17/5/8 下午1:06
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    cfg_user_service
    """

    cfg_user_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.cfg_user_model = self.import_model('cfg.user.model.cfg_user_model')

    def get_admin_cfg(self, params):
        """
        查询管理员配置
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['admin_id'], params):
            return self._e('CFG_ADMIN_ID_NOT_EXIST')
        data = self.cfg_user_model.get_one(params['admin_id'])
        if not data:
            # 如果该店铺没有配置信息，则获取默认配置信息
            data = self.cfg_user_model.get_one()
            if not data:
                return self._e('SQL_EXECUTE_ERROR')
        result = self._e('SUCCESS')
        data['cfg_content'] = self.json.loads(data['cfg_content'])
        result['data'] = data
        return result
