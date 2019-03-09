import asyncio
import aiohttp
import time
import sys
from ip_pool.db import RedisClient
from ip_pool.settings import TEST_URL, VALID_STATUS_CODES, BATCH_TEST_SIZE
from aiohttp import ClientError, ClientProxyConnectionError
from asyncio import TimeoutError


class Tester:

    def __init__(self):
        self.redis = RedisClient()

    async def test_singe_proxy(self, proxy):
        """
        用异步http测试单个代理
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', real_proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
            except(ClientError, ClientProxyConnectionError, TimeoutError, AttributeError, aiohttp.client_exceptions.ClientConnectorError):
                self.redis.decrease(proxy)
                print('代理请求失败',proxy)

    def run(self):
        """
        用协程启动测试函数
        :return:
        """
        print('测试开始')
        try:
            count = self.redis.count()
            print('当前剩余', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i+BATCH_TEST_SIZE, count)
                print('正在测试第', start+1, '--', stop, '个代理')
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                task = [self.test_singe_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(task))
                time.sleep(3)

        except Exception as e:
            print("测试器发生错误", e.args)


# a = Tester()
# a.run()

