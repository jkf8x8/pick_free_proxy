import requests,Helper
from pyquery import PyQuery as pq
import asyncio
from aiohttp import ClientSession
import testRedis
import json

'''
爬取免费Ip代理
'''
class getProxy:
    def __init__(self):
        # self.proxy_ip_list = [{'ip': '171.35.167.243', 'port': '9999'}, {'ip': '223.199.22.138', 'port': '9999'}]
        self.spider_01_url = [
            'http://www.89ip.cn/index_3.html'
        ]
        self.spider_01_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36','Referer':'http://www.89ip.cn/index.html'}
        self.spider_02_url = []
        self.proxies = '127.0.0.1:8080'

    #     init redis
        self.rds = testRedis.redisClient()

    '''
        获取 free proxy
    '''
    def run(self):
        self.spider_01()

    def Show(self):
        print('self.proxy_ip_list_leng',len(self.proxy_ip_list))
        print("freeproxy show",self.proxy_ip_list)


    '''
        http://www.89ip.cn/index_1.html
        抓取代理ip 存redis
    '''
    def spider_01(self):
        for urlitem in self.spider_01_url:
            httpres = requests.get(urlitem,headers=self.spider_01_headers)
            if httpres.status_code != 200:
                Helper.write_logs("info")
                return None
            body = pq(httpres.content)
            tritem = body('table>tbody tr').items()

            for item in tritem:
                ip = item('td:first').text()
                port = item('td:eq(1)').text()
                if ip =='' or port =='':
                    print('ip or port no empty')
                    continue
                obj = {'ip':ip,'port':port}
                member = json.dumps(obj)
                self.rds.zadd(member,0)

    '''
        redis save
    '''
    def save(self,item):
        pass