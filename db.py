import redis
from ip_pool.settings import  REDIS_HOST, REDIS_PORT, REDIS_KEY
from ip_pool.settings import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice
import re
from ip_pool.error import PoolEmptyError

class RedisClient:

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        """
        初始化链接redis数据库
        :param host: Redis 地址
        :param port: 端口
        """
        self.db = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理时初始化分数
        :param proxy: 代理
        :param score: 分数
        :return: 加入redis的有序集合
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy:score})

    def random(self):
        """
        随机获取有效代理,首次尝试获取最高分，如无，则按排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return result[0]
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
         """
         代理值减一分， 小于最小值删除
         :param proxy:代理
         :return: 修改数据库的分数
         """
         score = self.db.zscore(REDIS_KEY, proxy)
         if score and score > MIN_SCORE:
             print('代理', proxy, '当前分数', score, '减4')
             return self.db.zincrby(REDIS_KEY, -4, proxy)
         else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy:
        :return:
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理的分数设置为最大
        :param proxy:
        :return:
        """
        print('代理', proxy, '可用, 分数', MAX_SCORE)
        return self.db.zadd(REDIS_KEY,  {proxy:MAX_SCORE})

    def count(self):
        """
        获取代理队列长度
        :return: 代理的长度
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取代理
        :param start:开始索引
        :param stop: 结束索引
        :return:
        """
        return self.db.zrevrange(REDIS_KEY, start, stop)

# if __name__ == '__main__':
#     conn = RedisClien()
#     a = conn.add('192.168.1.1:8080')
#     # result = conn.batch(680, 688)
#     b = conn.all()
#     print(b)