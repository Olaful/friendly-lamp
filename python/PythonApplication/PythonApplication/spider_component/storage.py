from pymongo import MongoClient
import datetime
from bson.binary import Binary
import zlib
try:
    import cPickle as pickle
except ImportError:
    import pickle

import redis
from redis.exceptions import DataError
from .settings import MAX_SCORE,\
MIN_SCORE,\
INITIAL_SCORE,\
REDIS_HOST,\
REDIS_PORT,\
REDIS_PWD,\
REDIS_ZSET_KEY,\
MONGO_URI\

import random
import redis
from redis.exceptions import DataError
from urllib.request import urlsplit
import os
import shutil
import re
from pymongo import errors
import csv
import lxml.html

class MongoHtml:
    def __init__(self, client=None, expires=datetime.timedelta(days=30), compress=False):
        self.client = MongoClient(MONGO_URI) if client is None else client
        self.db = self.client.cache
        # 在某字段上建立索引(字段类型为date)，记录会在指定的时间后过期,过期后会被删除
        # 只能在单个字段上建立索引
        #self.db.webpage.create_index('timestamp', expiresAfterSeconds=expires.total_seconds())
        self.compress = compress

    def __setitem__(self, url, result):
        if self.compress:
            # pickle序列化后压缩
            result = Binary(zlib.compress(pickle.dumps(result)))
        else:
            result = Binary(pickle.dumps(result))
        record = {'result': result, 'timestamp': datetime.datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set':record}, upsert=True)

    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id':url})
        if record:
            print('get from mongodb:',url)
            if self.compress:
                return pickle.loads(zlib.decompress(record['result']))
            return pickle.loads(record['result'])
        else:
            raise KeyError(url + 'dose not exist')

    # 特殊方法，使用 in 迭代类实例时，会自动调用
    def __contains__(self, url):
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True

    def clear(self):
        self.db.webpage.drop()


class RedisProxy():
    """
    代理存储
    """
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, pwd=REDIS_PWD):
        self.db = redis.StrictRedis(host=host, port=port, password=pwd, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        if not self.db.zscore(REDIS_ZSET_KEY, proxy):
            self.db.zadd(REDIS_ZSET_KEY, {proxy:score,})
    
    def random(self):
        rls = self.db.zrangebyscore(REDIS_ZSET_KEY, MAX_SCORE, MAX_SCORE)
        if len(rls):
            return random.choice(rls)
        else:
            rls = self.db.zrevrange(REDIS_ZSET_KEY, 0, 100)
            if len(rls):
                return random.choice(rls)
            else:
                 raise DataError
    
    def decrease(self, proxy):
        score = self.db.zscore(REDIS_ZSET_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理{}分数{}减1'.format(proxy, score))
            self.db.zincrby(REDIS_ZSET_KEY, -1, proxy)
        else:
            print('移除代理{}:{}'.format(proxy, score))
            self.db.zrem(REDIS_ZSET_KEY, proxy)

    def exist(self, proxy):
        return not self.db.zscore(REDIS_ZSET_KEY, proxy) == None
    
    def add_max(self, proxy):
        print('代理{}可用，分数设置为{}'.format(proxy, MAX_SCORE))
        return self.db.zadd(REDIS_ZSET_KEY, {proxy:MAX_SCORE})

    def count(self):
        return self.db.zcard(REDIS_ZSET_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_ZSET_KEY, MIN_SCORE, MAX_SCORE)


class RedisCookie(object):
    """
    cookie存储
    """
    def __init__(self, type, website, host = REDIS_HOST, port=REDIS_PORT, pwd=REDIS_PWD):
        self.db = redis.StrictRedis(host=host, port=port, password=pwd, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        return '{type}:{website}.'.format(type=self.type, website=self.website)

    # 存储格式usrname:hashvalue
    def set(self, usrname, value):
        return self.db.hset(self.name(), usrname, value)

    def get(self, usrname):
        return self.db.hget(self.name(), usrname)

    def delete(self, usrname):
        return self.db.hdel(self.name(), usrname)

    def count(self):
        return self.db.hlen(self.name())

    def random(self):
        return random.choice(self.db.hvals(self.name()))

    def username(self):
        return self.db.hkeys(self.name())

    def all(self):
        return self.db.hgetall(self.name())

class DiskCache:
    """
    磁盘存储html
    compress选择是否压缩文件以节省磁盘空间，但读写文件时速度会变慢点
    """
    def __init__(self, cache_dir='myfile\cache', expires=datetime.timedelta(days=30), compress=False):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    # 设置文件内容
    def __setitem__(self, url, result):
        path = self.url_to_path(url)
        # 获取父目录路径
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 序列化数据与存取的时间,
        # 将数据通过特殊的形式转换为只有python语言认识的字符串
        data = pickle.dumps((result, datetime.datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as f:
            f.write(data)

    # 获取文件内容
    def __getitem__(self, url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            print('get from:',path)
            with open(path, 'rb') as f:
                data = f.read()
                if self.compress:
                    data = zlib.decompress(data)
                    # 序列化数据后获取
                    # 将pickle数据转换为python的数据结构
                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    self.clear()
                    raise KeyError(url + 'has expired')
                return result
        else:
            raise KeyError(url + 'dose not exist')

    def __delitem__(self, url):
        path = self.url_to_path(url)
        try:
            # 删除文件与目录
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass

    # 把url字符串转换成路径格式的字符串
    # 但在处理相似的url路径时可能会出现问题
    # 如/a*b与/a!b在实际中指向不同路径，
    # 但处理后就指向同一个磁盘路径了，而且文件名很多时
    # 会受到存储的限制，如ext4系统只允许同一个目录建立
    # 65535个文件
    def url_to_path(self, url):
        compents = urlsplit(url)
        path = compents.path
        # url目录路径如.com/后面可能是空的
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'

        filename = compents.netloc + path + compents.query
        # 文件名可能包含系统不支持的字符，如* >等符号，需替换掉
        filename = re.sub('[^0-9a-zA-Z\-.,;_]', '_', filename)
        return os.path.join(self.cache_dir, filename)

    # 判断文件数据是否过期
    def has_expired(self, timestamp):
        return datetime.datetime.utcnow() > timestamp + self.expires

    def clear(self):
        if os.path.exists(self.cache_dir):
            # 删除当前底下的所有子目录
            shutil.rmtree(self.cache_dir)

class MongoQueue:
    """
    从MongoDB获取数据队列的类
    url记录状态 0|待处理 1|处理中 2|已完成
    """
    OUTSTANDING, PROCESSING, COMELETE = range(3)

    def __init__(self, client=None, timeout=300):
        self.client = MongoClient() if client is None else client
        self.db = self.client.cache
        self.timeout = timeout

    # 特殊方法，当用类实例进行判断时(如 if MongoQueue() bool(MongoQueue()))
    # 会自动调用，python2.x中的写法为__nonzero__
    # 判断是否所有url都已完成处理
    def __bool__(self):
        try:
            record = None
            record =  self.db.crawl_queue.find_one({'status': {'$ne': self.COMELETE}})
        except Exception as e:
            print(e)
        return True if record else False

    # 把一条url入库，把置状态为待处理
    def push(self, url):
        try:
            self.db.crawl_queue.insert({'_id': url, 'status': self.OUTSTANDING})
        # 重复记录处理
        except errors.DuplicateKeyError as e:
            print(url,e, 'already exist in the database')

    # 取一条处于待处理状态的url，并置其状态为处理中，并加上开始处理的时间
    # 补充'set'待设置的集合，相当于一条记录，'$lt'小于，'$ne'不等于，还有'gt'大于
    def pop(self):
        record =  self.db.crawl_queue.find_and_modify(
                query = {'status': self.OUTSTANDING},
                update = {'$set':{'status': self.PROCESSING, 'timestamp': datetime.datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    # 取一条处于待获取状态的url，但不改变其状态
    def peek(self):
        record = self.db.crawl_queue.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    # 把已经处理过的url状态置为已完成
    def complete(self, url):
        self.db.crawl_queue.update({'_id': url}, {'$set': {'status': self.COMELETE}})

    # 当一条url处理超时并且其状态没有被置为已完成时，
    # 这条url应该当作还没有处理，此时修改其状态为待处理
    def repair(self):
        record = self.db.crawl_queue.find_and_modify(
                query = {'timestamp': {'$lt': datetime.datetime.now()-datetime.timedelta(seconds=-self.timeout)}, 'status': {'$ne': self.COMELETE}},
                update = {'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print('Released', record['_id'])

    # 清空队列
    def clear(self):
        self.db.crawl_queue.drop()

class CsvHtml:
    """
    csv存储
    """
    def __init__(self, file, col_heads):
        self.writer = csv.writer(open(file, 'w'))
        self.fields = col_heads
        self.writer.writerow(self.fields)

    # 特殊方法，csvHtml() 的时候会被自动调用,其中csvHtml是实例化的对象
    def __call__(self, row):
        self.writer.writerow(row)