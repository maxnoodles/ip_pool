from ip_pool.crawler import Crawler
from ip_pool.db import RedisClient
from ip_pool.settings import POOL_UPPER_THRESHOLD


class Getter():

    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        :return:
        """
        if self.redis.count() > POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始')
        n=0
        if not self.is_over_threshold():
            for callback_lable in range(self.crawler.__CrawlFuncCount__):
                callback= self.crawler.__CrawlFunc__[callback_lable]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                for proxy in  proxies:
                    self.redis.add(proxy)





