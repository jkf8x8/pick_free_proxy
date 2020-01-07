'''
中控
'''

import testProxy
import getProxy
import testRedis
import multiprocessing
import time

class Controller():
    def __init__(self):
        # self.rds = testRedis.redisClient()
        print("Controller init")


    def get_proxy(self):
        getproxy = getProxy.getProxy()
        getproxy.run()

    def test_proxy(self):
        while True:
            tp = testProxy.testProxy()
            tp.run()
            time.sleep(30)

    def random(self):
        rds = testRedis.redisClient()
        lists = rds.zrangebyscorerandom()
        print("rangdom",lists)


    def run(self):
        print("Controller run")
        multiprocessing.Process(target=self.get_proxy).start()
        multiprocessing.Process(target=self.test_proxy).start()
        self.random()
        # self.test_proxy()

