
# redis
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PWD = '123456'
REDIS_ZSET_KEY = 'proxies'

# mongodb
MONGO_URI = 'mongodb://tbq:tbq@192.168.1.102:27017'
MONGO_DATABASE = 'CSDN'

# download
TIME_SLEEP = 1

# 代理存储
POOL_UPPER__THRESHOLD = 10000

# 测试代理
VALID_STATUS_CODE = [200]
TEST_URL = 'https://www.dytt8.net'
BATCH_TEST_SIZE = 100

# 代理调度器
TEST_CYCLE = 1
GET_CYCLE = 1
TEST_ENABLED = True
GET_ENABLED = False
API_ENABLED = False
API_IP = '127.0.0.1'
API_PORT = 1026

# cookie
GENERATOR_MAP = {'12306': 'CookieGenerator12306'}
TESTER_MAP = {'12306':'Test12306'}
COOKIEGENERATOR_ENABLED = True
COOKIETESTER_ENABLED = False