# -*- coding:utf-8 -*-

import redis
from source.properties import properties


class RedisBase(object):

    pool = redis.ConnectionPool(
        host=properties.get("redis", "REDIS_HOST"),
        port=properties.get("redis", "REDIS_PORT")
    )

    def get_conn(self):
        return redis.StrictRedis(connection_pool=self.pool)

    def set(self, key, value):

        resource = None

        try:
            resource = self.get_conn()

            resource.setex(key, value)

        except Exception, e:

            print Exception, ':', e

    def set(self, key, value, second):

        resource = None

        try:
            resource = self.get_conn()

            resource.setex(key, value, ex=second)

        except Exception, e:

            print Exception, ':', e

    def get(self, key):

        """
        根据key获取value
        :param key: 
        :return: 
        """

        resource = None

        try:
            resource = self.get_conn()

            return resource.get(key)
        except Exception, e:

            print Exception, ':', e

    def delete(self, key):

        """
        根据删除对应的key
        :param key: 
        :return: 
        """
        resource = None

        try:
            resource = self.get_conn()

            resource.delete(key)
        except Exception, e:

            print Exception, ':', e
