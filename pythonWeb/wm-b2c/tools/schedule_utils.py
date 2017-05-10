# -*- coding:utf-8 -*-

"""
@author: delu
@file: schedule_utils.py
@time: 17/5/2 下午4:11
"""
from apscheduler.schedulers.background import BackgroundScheduler
from source.system_constants import SystemConstants
import importlib
import time
import conf.config as config


class ScheduleUtils(object):
    scheduler = BackgroundScheduler()
    scheduler.start()

    @staticmethod
    def add_job(params):
        """
        添加任务
        :param params: 
        :return: 
        """
        try:
            model = importlib.import_module(config.CONF['version'] + '.module.' + params['service_path'])
            func = getattr(model.Service(), params['method'])
            ScheduleUtils.scheduler.add_job(func, 'date', run_date=params['start_time'], args=[params])
            return SystemConstants.SUCCESS
        except Exception, e:
            print Exception, ':', e
            return SystemConstants.SCHEDULE_ADD_JOB_ERROR

    def test(self, params):
        print params['name']


if __name__ == '__main__':
    # model = importlib.import_module('tools.schedule_utils')
    # func = getattr(model.ScheduleUtils(), 'test')
    # params = {
    #     ''
    #     'start_time': '2017-05-02 17:14:50',
    #     'name': 'delu'
    # }
    # ScheduleUtils.add_job(params)
    # # scheduler = BackgroundScheduler()
    # # scheduler.add_job(test, 'date', run_date='2017-05-02 16:29:30')
    # # scheduler.start()
    # while True:
    #     time.sleep(1)
    #     print 'sss'
    mytime = time.strptime('2017-05-02 16:30:00', '%Y-%m-%d %H:%M:%S')

    time_array = time.strptime('2017-05-02 16:30:00', '%Y-%m-%d %H:%M:%S')
    mytime = str(time.mktime(time_array)).split('.')[0]
    mytime = int(mytime) - 300

    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mytime))
