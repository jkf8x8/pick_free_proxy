import redis
import json
import random

R_HOST='localhost'
R_PORT=6379

class redisClient():

    def __init__(self):
        self.rdb = redis.Redis(host=R_HOST,port=R_PORT,decode_responses=True)
        self.proxylist="proxylist9"

    '''
        存数据
    '''
    def zadd(self,member,score):
        # print(red.zadd('proxy',{"{'member2":33}))
        st = self.rdb.zadd(self.proxylist,{member:score})
        # print('redis存{},status {}'.format(member,st))

    '''
        取全部数据
    '''
    def zrange(self):
        proxylist = self.rdb.zrange(self.proxylist,0,-1)
        return proxylist
        for item in proxylist:
            print(item)

    '''
        取有效proxy
    '''
    def zrangebyscore(self):
        proxylist = self.rdb.zrangebyscore(self.proxylist,1,11)
        return proxylist

    '''
            随机取一个有效proxy
    '''
    def zrangebyscorerandom(self):
        proxylist = self.zrangebyscore()
        length = len(proxylist)
        if length > 0:
            index = random.randint(0, len(proxylist))
            return proxylist[index]
        else:
            return "error"
