from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy, Fault
import sys
from os.path import isfile, join, abspath
from urllib.parse import urlparse

# 服务器重启后可以立即使用断开前的端口
SimpleXMLRPCServer.allow_reuse_address = True

# 自定义一些返回异常
UNHANDLE = 100
ACCESS_DENIED = 200

# 无法查询异常
class UnhandledQuery(Fault):
    def __init__(self, message="Couldn't handle the query"):
        Fault.__init__(self, UNHANDLE, message)

# 访问不在指定的目录中的文件时返回的异常，
# 因为客户端可能指定../filename之类的文件名去访问非指定的目录下的文件
class AccessDenied(Fault):
    def __init__(self, message="Access Denied"):
        Fault.__init__(self, ACCESS_DENIED, message)

# 判断指定文件夹中是否有指定文件，文件名包含完整路径的文件名
def inside(dir, fullfilename):
    dir = abspath(dir)
    filename = abspath(fullfilename)
    return filename.startswith(join(dir, ''))

# 定义最多寻找多少个节点，节点中间的联系点一般不超过6个
MAX_FIND_NODE = 6

# 从命令行参数中提取port
def getPort(url):
    ipPort = urlparse(url)[1]
    ll = ipPort.split(':')
    return int(ll[-1])


# 定义一个P2P网络中的节点，功提供给对外查询的功能并返回数据
class Node:
    # 一个节点包含文件存放目录，节点地址，查询文件方法，将请求广播至其它节点的基本要素
    def __init__(self, url, dirname, secret):
        self.url = url
        self.secret = secret
        self.dirname = dirname
        self.known = set()

    # 查询文件主功能，查询顺序为本地->网络中的其它已知节点
    def query(self, query, history = []):
        # 先从本机开始查询文件
        try: return self._handle(query)
        except UnhandledQuery:
            history = history + [self.url]
            # 如果寻找超过最大寻找节点数，则停止查找
            if len(history) >= MAX_FIND_NODE:
                # 重抛异常
                raise
            # 请求发送到其它节点
            return self._brocast(query, history)

    # 把其它节点添加到已知节点，可能会遍历这些节点寻找文件
    def hello(self, other):
        self.known.add(other)
        return 0

    # 寻找节点文件并写入本地文件
    def fetch(self, query, secret):
        # 校验节点密语
        if secret != self.secret: return ACCESS_DENIED
        result = self.query(query)
        f = open(join(self.dirname, query), 'w')
        f.write(result)
        f.close()
        return 0

    # 将自身注册为服务器的特性,并开启服务器
    def _start(self):
        server = SimpleXMLRPCServer(('', getPort(self.url)), logRequests=False)
        # 注册特性
        server.register_instance(self)
        # 注册方法
        #server.register_function(func)
        server.serve_forever()

    # 提取内部文件,该方法不对其它节点开放
    def _handle(self, query):
        file = join(self.dirname, query)
        if not isfile(file): raise UnhandledQuery
        if not inside(self.dirname, file): raise ACCESS_DENIED
        return open(file).read()

    def _brocast(self, query, history):
        # 遍历拷贝的副本，由于遍历真实的节点可能会对节点产生不必要的操作
        for other in self.known.copy():
            if other in history: continue
            try:
                # 获取服务器的实例，这样也就获取了服务器中注册的实例或者方法
                server = ServerProxy(other)
                return server.query(query, history)
            # 如果节点不能访问，则不必要记录该节点，避免下一个节点重复访问该节点
            except Fault as f:
                if f.faultCode == UNHANDLE: pass
                else:
                    self.known.remove(other)
            except:
                # 如果不能访问该节点，下一次就不再遍历该节点了
                self.known.remove(other)
        raise UnhandledQuery