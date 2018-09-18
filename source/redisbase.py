# -*- coding:utf-8 -*-

import redis
from source.properties import Properties

properties = Properties()


class RedisBase(object):

    pool = redis.ConnectionPool(
        host=properties.get("redis", "REDIS_HOST"),
        port=properties.get("redis", "REDIS_PORT"),
        password=properties.get("redis", "REDIS_PASS"),
        max_connections=1000
    )

    def get_conn(self):
        return redis.StrictRedis(connection_pool=self.pool)

    def set_value(self, key, value):
        try:
            resource = self.get_conn()
            resource.set(key, value)
        except Exception, e:
            print Exception, ':', e

    def set(self, key, value, second=0):
        try:
            resource = self.get_conn()
            if second > 0:
                resource.setex(key, second, value)
            else:
                resource.set(key, value)
        except Exception, e:
            print Exception, ':', e

    def get(self, key):
        try:
            resource = self.get_conn()
            return resource.get(key)
        except Exception, e:
            print Exception, ':', e

    def delete(self, *key):
        result = None
        try:
            resource = self.get_conn()
            result = resource.delete(*key)
        except Exception, e:
            print Exception, ':', e
        return result

    def hmset(self, key, value, second=0):
        try:
            resource = self.get_conn()
            with resource.pipeline() as pipe:
                pipe.hmset(key, value)
                if second > 0:
                    pipe.expire(key, int(second))
                pipe.execute()
        except Exception, e:
            print e

    def hincr(self, key, field, increment=1):
        try:
            resource = self.get_conn()
            return resource.hincrby(key, field, increment)
        except Exception as e:
            print e

    def hgetall(self, key):
        try:
            resource = self.get_conn()
            return resource.hgetall(key)
        except Exception, e:
            print e

    def mget(self, key):
        try:
            resource = self.get_conn()
            return resource.mget(key)
        except Exception, e:
            print e

    def ttl(self, key):
        try:
            resource = self.get_conn()
            return resource.ttl(key)
        except Exception, e:
            print e

    def expire(self, key, second=0):
        try:
            resource = self.get_conn()
            return resource.expire(key, int(second))
        except Exception, e:
            print e

    def exist(self, key):
        try:
            resource = self.get_conn()
            return resource.exists(key)
        except Exception, e:
            print e

    def incr(self, key, amount=1):
        try:
            resource = self.get_conn()
            return resource.incr(key, amount)
        except Exception, e:
            print e

    def decr(self, key, amount=1):
        try:
            resource = self.get_conn()
            return resource.decr(key, amount)
        except Exception, e:
            print e

    def sadd(self, key, value):
        try:
            resource = self.get_conn()
            return resource.sadd(key, value)
        except Exception, e:
            print e

    def smembers(self, key):
        try:
            resource = self.get_conn()
            return resource.smembers(key)
        except Exception, e:
            print e

    def spop(self, key):
        try:
            resource = self.get_conn()
            return resource.spop(key)
        except Exception, e:
            print e

    def lpush(self, key, value):
        try:
            resource = self.get_conn()
            return resource.lpush(key, value)
        except Exception, e:
            print e

    def rpop(self, key):
        try:
            resource = self.get_conn()
            return resource.rpop(key)
        except Exception, e:
            print e

    def llen(self, key):
        try:
            resource = self.get_conn()
            return resource.llen(key)
        except Exception, e:
            print e

    def hincrby(self, key, field, increment=1):
        try:
            resource = self.get_conn()
            return resource.hincrby(key, field, increment)
        except Exception, e:
            print e

    def hget(self, key, field):
        try:
            resource = self.get_conn()
            return resource.hget(key, field)
        except Exception, e:
            print e

    def subsribe(self, channel_list):
        try:
            resource = self.get_conn()
            p = resource.pubsub()
            p.subscribe(channel_list)
            return p
        except Exception as e:
            print e
            return None

    def publish(self, channel, message):
        try:
            resource = self.get_conn()
            resource.publish(channel, message)
        except Exception as e:
            print e

if __name__ == '__main__':

    r = RedisBase()
    p = r.subsribe(['channel1'])

    for item in p.listen():

        if item['type'] == 'pmessage' or item['type'] == 'message':

            print(item['channel'])

            print(item['data'])
