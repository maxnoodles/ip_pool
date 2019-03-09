from ip_pool.getter import Getter
from ip_pool.db import RedisClient
from ip_pool.settings import *
from ip_pool.tester import Tester
from ip_pool.api import app
import time
from multiprocessing import Process


class Schedule:

    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试
        """
        tester = Tester()
        while True:
            print('测试器开始')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__ == '__main__':
    schedule = Schedule()
    schedule.run()