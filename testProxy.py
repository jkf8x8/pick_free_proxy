import time
import asyncio
import requests
import testRedis
import json
from aiohttp import ClientSession


class testProxy:
    tasks = []
    loop = asyncio.get_event_loop()
    # proxy_ip_list = [{'ip': '171.35.167.243', 'port': '9999'}, {'ip': '223.199.22.138', 'port': '9999'}, {'ip': '58.212.42.225', 'port': '9999'}, {'ip': '60.167.159.76', 'port': '9999'}, {'ip': '58.212.43.19', 'port': '9999'}, {'ip': '223.199.25.184', 'port': '9999'}, {'ip': '220.249.149.111', 'port': '9999'}, {'ip': '223.199.26.178', 'port': '9999'}, {'ip': '223.199.20.138', 'port': '9999'}, {'ip': '58.253.153.159', 'port': '9999'}, {'ip': '47.98.56.88', 'port': '80'}, {'ip': '223.199.29.108', 'port': '9999'}, {'ip': '218.91.112.61', 'port': '9999'}, {'ip': '36.248.129.159', 'port': '9999'}, {'ip': '223.199.26.7', 'port': '9999'}, {'ip': '114.224.112.109', 'port': '9999'}, {'ip': '60.13.42.253', 'port': '9999'}]
    proxy_ip_list = []

    def __init__(self):
        self.rds = testRedis.redisClient()

    '''
        检测代理是否可用
    '''
    url = "https://www.baidu.com"
    async def detecting(self,url,item):

        proxies = "http://{}:{}".format(item['ip'], item['port'])
        data = json.dumps({'ip': item['ip'], 'port': item['port']})
        #print('proxies',proxies)
        async with ClientSession() as session:
            try:
                async with session.get(url,proxy=proxies,timeout=3) as response:
                    # response = await response.status
                    # print('可用代理-{}'.format(proxies))
                    self.rds.zadd(data,10)

            except Exception as e:
                self.rds.zadd(data, 0)
                pass
                # print("{} connection is failsure".format(proxies))


    def prerun(self):
        while len(self.proxy_ip_list) < 1:
            print('proxy_ip_list is empty,please waiting')
            self.getproxylist()
            time.sleep(10)

        # print("testProxy",self.proxy_ip_list)
        try:
            for item in self.proxy_ip_list:
                task = asyncio.ensure_future(self.detecting(self.url,item))
                self.tasks.append(task)
        except Exception as e:
            pass

    def run(self):
        self.getproxylist()
        self.prerun()
        self.loop.run_until_complete(asyncio.wait(self.tasks))

    def getproxylist(self):
        self.proxy_ip_list = []
        proxy_list = self.rds.zrange()
        for item in proxy_list:
            self.proxy_ip_list.append(json.loads(item))
        print('proxy_ip_list.length', len(self.proxy_ip_list))

