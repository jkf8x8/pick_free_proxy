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
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    ]
    def __init__(self):
        # self.proxy_ip_list = [{'ip': '171.35.167.243', 'port': '9999'}, {'ip': '223.199.22.138', 'port': '9999'}]
        self.spider_01_headers = {'User-Agent':self.user_agent[0],'Referer':'http://www.89ip.cn/index.html'}
        self.spider_01_url = [
            'http://www.89ip.cn/index_1.html',
            'http://www.89ip.cn/index_2.html',
            'http://www.89ip.cn/index_3.html'
        ]
        self.spider_02_headers = {'User-Agent':self.user_agent[0],'Referer':'https://www.kuaidaili.com/free/'}
        self.spider_02_url = [
            'https://www.kuaidaili.com/free/inha/1',
            'https://www.kuaidaili.com/free/inha/2',
            'https://www.kuaidaili.com/free/inha/3',
            'https://www.kuaidaili.com/free/inha/4'
        ]
        self.spider_03_headers = {'User-Agent':self.user_agent[0],'Referer':'http://www.ip3366.net/?stype=1&page=1'}
        self.spider_03_url = [
            'http://www.ip3366.net/?stype=1&page=1',
            'http://www.ip3366.net/?stype=1&page=2',
            'http://www.ip3366.net/?stype=1&page=3',
            'http://www.ip3366.net/?stype=1&page=4',
        ]

        # https://www.xicidaili.com/wt/1
        self.spider_04_headers = {'User-Agent': self.user_agent[0], 'Referer': 'https://www.xicidaili.com/wt/1'}
        self.spider_04_url = [
            'https://www.xicidaili.com/wt/1',
            'https://www.xicidaili.com/wt/2',
        ]


        self.proxies = '127.0.0.1:8080'

    #     init redis
        self.rds = testRedis.redisClient()

    '''
        获取 free proxy
    '''
    def run(self):
        self.spider_01()
        self.spider_02()
        self.spider_03()
        self.spider_04()

    def Show(self):
        print('self.proxy_ip_list_leng',len(self.proxy_ip_list))
        print("freeproxy show",self.proxy_ip_list)


    '''
        http://www.89ip.cn/index_1.html
        抓取代理ip 存redis
    '''
    def spider_01(self):
        # loopnum =0
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
        https://www.kuaidaili.com/free/inha/1
    '''
    def spider_02(self):
        for urlitem in self.spider_02_url:
            httpres = requests.get(urlitem, headers=self.spider_02_headers)
            if httpres.status_code != 200:
                Helper.write_logs("info")
                return None
            body = pq(httpres.content)
            tritem = body('table>tbody tr').items()

            for item in tritem:
                ip = item('td:first').text()
                port = item('td:eq(1)').text()
                if ip == '' or port == '':
                    print('ip or port no empty')
                    continue
                obj = {'ip': ip, 'port': port}
                member = json.dumps(obj)
                self.rds.zadd(member, 0)

    '''
        http://www.ip3366.net/?stype=1&page=1
    '''
    def spider_03(self):
        for urlitem in self.spider_03_url:
            httpres = requests.get(urlitem, headers=self.spider_03_headers)
            if httpres.status_code != 200:
                Helper.write_logs("info")
                return None
            body = pq(httpres.content)
            tritem = body('table>tbody tr').items()

            for item in tritem:
                ip = item('td:first').text()
                port = item('td:eq(1)').text()
                if ip == '' or port == '':
                    print('ip or port no empty')
                    continue
                obj = {'ip': ip, 'port': port}
                # print('spider ',obj)
                member = json.dumps(obj)
                self.rds.zadd(member, 0)

    '''
        https://www.xicidaili.com/wt/1
    '''
    def spider_04(self):
        for urlitem in self.spider_04_url:
            httpres = requests.get(urlitem, headers=self.spider_04_headers)
            if httpres.status_code != 200:
                Helper.write_logs("info")
                return None
            body = pq(httpres.content)
            tritem = body('table tr:gt(0)').items()

            for item in tritem:
                # print(item)
                ip = item('td:eq(1)').text()
                port = item('td:eq(2)').text()
                if ip == '' or port == '':
                    print('ip or port no empty')
                    continue
                obj = {'ip': ip, 'port': port}
                member = json.dumps(obj)
                self.rds.zadd(member, 0)



    '''
        redis save
    '''
    def save(self,item):
        pass

if __name__ == '__main__':
    g = getProxy()
    g.run()
