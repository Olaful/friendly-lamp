import pymysql
import json
import os
from functools import wraps
import logging
from logging.handlers import RotatingFileHandler


_CONFIG = {}
_DB_CACHE = {}
_LOGGER = None


def _use_default_cursor(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._default_cursor_init()
        return func(self, *args, **kwargs)
    return wrapper


class MysqlClient(object):
    def __init__(self,
                 host='localhost',
                 port=3306,
                 user='root',
                 password='',
                 database=None,
                 charset='utf8mb4',
                 cursorclass=pymysql.cursors.DictCursor,
                 autocommit=True):

        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    password=password,
                                    database=database,
                                    charset=charset,
                                    cursorclass=cursorclass,
                                    autocommit=autocommit)

        self.default_cursor = None  # type:pymysql.cursors.Cursor

        self.autocommit = autocommit

    @property
    def connection(self) -> pymysql.Connection:
        return self.conn

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.alive():
            self.conn.close()

    def rollback(self):
        self.conn.rollback()

    def alive(self):
        return self.conn.open

    def cursor(self, cursor=None):
        return self.conn.cursor(cursor)

    def _default_cursor_init(self):
        if self.default_cursor is None:
            self.default_cursor = self.cursor()

    @_use_default_cursor
    def execute(self, query, args=None):
        return self.default_cursor.execute(query, args)

    @_use_default_cursor
    def executemany(self, query, args):
        return self.default_cursor.executemany(query, args)

    @_use_default_cursor
    def fetchone(self):
        return self.default_cursor.fetchone()

    @_use_default_cursor
    def fetchall(self):
        return self.default_cursor.fetchall()

    @_use_default_cursor
    def fetchmany(self):
        return self.default_cursor.fetchmany()

    @_use_default_cursor
    def to_sql(self, query, args=None):
        return self.default_cursor.mogrify(query, args)


def init_config(file):
    global _CONFIG
    path = os.path.dirname(os.path.abspath(__file__))
    full_name = os.path.join(path, 'config', f"{file}.json")
    with open(full_name, 'r', encoding='utf8') as f:
        _CONFIG[file] = json.load(f)


def init_logger():
    global _LOGGER

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'logs')
    os.makedirs(path, exist_ok=True)
    logFile = os.path.join(path, 'strategy.log')

    _LOGGER = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    rHandler = RotatingFileHandler(logFile, maxBytes=5 * 1024 * 1024, backupCount=10)
    rFormatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s')
    rHandler.setFormatter(rFormatter)
    rHandler.setLevel(logging.DEBUG)
    _LOGGER.addHandler(rHandler)


def create_mysql(name):
    db_config = get_config('database', 'database', name)
    mysql_client = MysqlClient(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

    _DB_CACHE[name] = mysql_client


def get_config(*args):
    tmp_config = _CONFIG[args[0]]

    for i in range(1, len(args)):
        if isinstance(tmp_config, dict):
            tmp_config = tmp_config.get(args[i], None)
    return tmp_config


def get_mysql(name):
    return _DB_CACHE.get(name, None)


def get_logger():
    return _LOGGER


def distrib_weight(d_type='decre', num=10, per=0.3, front_num=5, is_round=False, aligh_obj=None):
    total = 1
    com = []

    if d_type == 'avg':
        com = [1 / num] * num
    elif d_type == 'decre':
        for i in range(num - 2):
            com.append(total * per)
            total -= total * per
        left = 1 - sum(com)
        com.append(left * (1 - per))
        com.append(left * per)
    elif d_type == 'decre_avg':
        for i in range(front_num):
            com.append(total * per)
            total -= total * per
        left = 1 - sum(com)
        back_num = num - front_num
        com.extend([left / back_num] * back_num)

    if is_round:
        com = list(map(lambda x: round(x, 4), com))
    if aligh_obj and isinstance(aligh_obj, (dict, list, tuple)):
        new_aligh_dict = dict(zip(aligh_obj, com))
        new_aligh_json = json.dumps(new_aligh_dict)
        new_aligh_json = new_aligh_json.replace(',', ',\n')

        return new_aligh_json

    return com
