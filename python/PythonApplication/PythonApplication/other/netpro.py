#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygeocoder import Geocoder
import requests
import http.client
import json
from urllib.parse import quote_plus
import socket
import argparse
from datetime import datetime
import time, timeit
import sys, random
import dns.resolver
import struct
import ssl
import ctypes
import sys
import textwrap
from threading import Thread
from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn
import select
import asyncio
import asyncore, asynchat
import memcache
import hashlib
import zmq


def getlltitude():
    """
    协议层次api<-url<-http<-tcp/ip
    :return:
    """

    address1 = '207 N. Defiance St, Archbold, OH'
    address2 = 'shenzhen'
    coordinates = Geocoder.geocode(address2)[0].coordinates
    print(coordinates)


def getlltitude2():
    """
    通过requests库请求
    :return:
    """
    address = '207 N. Defiance St, Archbold, OH'
    param = {'address': address, 'sensor': False}
    url = 'http://maps.googleapis.com/maps/api/geocode/json'
    resp = requests.get(url, params=param)
    answer = resp.json()
    rls = answer['result'][0]['geometry']['location']


def getlltitude3():
    """
    直接使用http请求
    :return:
    """
    base_url = 'maps/api/geocode/json'
    address = '207 N. Defiance St, Archbold, OH'
    path = f'{base_url}?address={quote_plus(address)}&sensor=false'
    conn = http.client.HTTPConnection('maps.google.com')
    conn.request('GET', path)
    rawreply = conn.getresponse().read()
    # 接收导的是网络字节，需要解码
    reply = json.loads(rawreply.decode('utf-8'))
    rls = reply['result'][0]['geometry']['location']


def getlltitude4():
    address = '207 N. Defiance St, Archbold, OH'
    request_txt = f"""GET /maps/api/geocode/json?address={address}&sensor=false HTTP/1.1\r\n
                    Host: maps.google.com:80\r\n
                    User-Agent: netpro.py (Fundations of Python Network Programming)\r\n
                    Connetion: close\r\n\r\n"""
    sock = socket.socket()
    sock.connect(('maps.google.com', 80))
    sock.sendall(request_txt.encode('ascii'))
    raw_reply = b''
    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more
    rls = raw_reply.decode('utf-8')


def decode_encode():
    input_bytes = b'\xff\xfe4\x001\x003\x00\ \x00i\x00s\x00 \x00i\x00n\x00.\x00'
    # input_characters = input_bytes.decode('utf-16')
    # rep_str = repr(input_characters)

    output_characters = 'We copy you down, Eagle.\n'
    output_bytes = output_characters.encode('utf-8')

    print(output_bytes)


def get_ip_with_hostname():
    """
    根据主机名获取ip地址
    :return:
    """
    hostname = 'www.python.org'
    # 实际上通过操作系统的域名解析服务(dns)来进行解析的
    addr = socket.gethostbyname(hostname)
    # port = socket.getservbyname(hostname)
    print(addr)


def udpserver(port):
    """
    udp服务器
    :return:
    """
    # 每一次最大接收65535字节长度的内容
    max_bytes = 65535

    # AF_INET说明使用的网络类型，几乎使用，还有posix系统上使用的AF_UNIX
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 127.0.0.1只接收本机发送的数据包，''空白则不限制
    # (ip, port)为套接字地址
    sock.bind(('127.0.0.1', port))
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(max_bytes)
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, data))
        text = 'Your data was {} bytes long'.format(len(data))
        data = text.encode('ascii')
        sock.sendto(data, address)


def udpclient(port):
    """
    udp客户端
    :param port:
    :return:
    """
    max_bytes = 65535

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = 'The time is {}'.format(datetime.now())
    data = text.encode('ascii')
    sock.sendto(data, ('127.0.0.1', port))
    print('The OS assiged me the address {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(max_bytes)
    text = data.decode('ascii')
    print('The server {} replied {!r}'.format(address, text))


def udpserver2(interface, port):
    """
    simulate drop packet
    :param interface:
    :param port:
    :return:
    """
    MAX_BYTES = 65535

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 如果服务器绑定的IP地址是外部分配的话，如以太网上的ip地址
    # 那么客户端连接的时候也要connect到指定的的ip上(除非是在不同于服务器
    # 的机子上连接，这时可以通过指定服务器主机名进行连接)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        # 模仿丢包现象
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        text = data.decode('ascii')
        print('The clien at {} say {!r}'.format(address, text))
        message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'), address)


def udpclient2(hostname, port):
    MAX_BYTES = 655635
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))

    delay = 0.1
    text = 'This is another message'
    data = text.encode('ascii')
    while True:
        sock.send(data)
        print('Waitting up to {} seconds for a reply'.format(delay))
        # 指数退避法，重发的时间间隔逐渐增加，如果到达服务器的时间是200毫秒，
        # 那么就得至少发送两次，因为第一次等待的时间只有100毫秒
        # 由于无法知道服务器是否宕机了或者网络的原因导致长时间没有收到消息
        # 所以有必要设置套接字接收请求的最大的等待时间
        # 但延迟太久也不是很好，因为如果马上再次重发时，计算可能已经连上网了
        # 此时还不如重发结束前一次的等待
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout:
            delay *= 2
            if delay > 2.0:
                raise RuntimeError('I think the server is down')
        else:
            # already receive message from server
            break
    print('The server say {!r}'.format(data.decode('ascii')))


def udpserver3(interface, port):
    max_bytes = 65535

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening for datagrams at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(max_bytes)
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))


def udpclient3(network, port):
    """
    broadcast
    :param network:
    :param port:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # SO_BROADCAST选项为允许广播，即允许向多台服务器发送数据包
    # 广播的IP为类似xxx.xxx.xxx.255,或者IP可为"<broadcast>"
    # 广播也是UDP最为强大的功能
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    text = 'Brocast datagram'
    sock.sendto(text.encode('ascii'), (network, port))


def recvall(sock, length):
    # 由于接收客户端并不知道要接收多大数据，
    # 只有不停接收直到接收缓冲区没有数据为止
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed' % (length, len(data)))
        data += more

    return data


def tcpserver1(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 如果没有设置SO_REUSEADDR，那么bind的地址需要在客户端断开连接几分钟才可使用
    # 正常情况下，关闭了连接后连接套接字还是保存几分钟，因为要响应FIN数据包
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind绑定时并不代表这个程序要作为服务端使用，只是声明该程序使用那个固定的
    # 端口进行通信
    sock.bind((interface, port))
    # listen的调用决定了该程序作为服务端来使用，使套接字成为监听套接字
    # 设置为1，如果accept还没有调用，新的连接送入栈中等待，并且栈中最多
    # 接收一个连接，其他连接会被丢弃
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Waiting to accept a new connection')
        # 监听套接字调用accept后会返回一个连接套接字
        # 监听套接字是不参与通信的，只有连接套接字才会参与通信
        sc, sockname = sock.accept()
        print('We have accepted ad connection from', sockname)
        print(' Socket name', sc.getsockname())
        print(' Socket peer', sc.getpeername())
        message = recvall(sc, 16)
        print(' Incoming sixteen-octet message:', repr(message))
        sc.sendall(b'Farewell, client')
        # 发送FIN数据包的三次握手来关闭连接
        sc.close()
        print(' Reply sent, socket closed')


def tcpclient1(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    # 如果使用send方法，则可能由于发送缓冲区已满，导致发送数据不全，使用sendall则会
    # 循环把数据发送完全
    sock.sendall(b'Hi there, server')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))
    sock.close()


def tcpserver2(host, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())

    while True:
        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()
        print('Process up to 1024 bytes at a time from', sockname)
        n = 0
        while True:
            # 接收一定大小的数据并处理返回，而不是一次接收完并处理完返回，
            # 减少内存占用过多
            data = sc.recv(1024)
            if not data:
                break
            output = data.decode('ascii').upper().encode('ascii')
            sc.sendall(output)
            n += len(data)
            print('\r %d bytes processed so far' % (n,), end=' ')
            sys.stdout.flush()
        print()
        sc.close()
        print(' Socket closed')


def tcpclient2(host, port, bytecount):
    """
    dead lock
    :param host:
    :param port:
    :param bytecount:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bytecount = (bytecount + 15) // 16 * 16
    message = b'capitalize this!'

    print('Sending', bytecount, 'bytes of data, in chunks of 16 bytes')
    sock.connect((host, port))
    sent = 0
    # 如果发送的数据量太大，服务端处理后放在客户端接收缓冲区中，由于客户端
    # 没有调用recv，导致缓冲区数据大小超过系统限定，，sendall被禁用，这时服务端程序就会被系统停止，
    # 服务端recv也就没有被执行，导致客户端无法发送数据，也会被停止
    # 造成死锁，相互等待
    # 但如果是send的话在发现不能发送时直接返回
    while sent < bytecount:
        sock.sendall(message)
        sent += len(message)
        print('\r %d bytes sent' % (sent, ), end=' ')
        sys.stdout.flush()

    # 创建文件对象
    # f = sock.makefile()
    # 写入的时候会调用sock的send方法
    # json.dump('{"k":1}', f)

    print()
    # SHUT_WR表示客户端不再发送数据，而服务端也不再接收数据
    # SHUT_RD表示关闭接收方向的套接字流
    # SHUT_RDWR表示关闭双向套接字
    # 多个进程共用一个套接字时，close关闭后，则只是调用close
    # 的进程结束了与套接字的关系，而调用shut_down则该套接字对
    # 所有进程都生效
    sock.shutdown(socket.SHUT_WR)

    print('Receiving all the data the server sends back')

    received = 0
    while True:
        data = sock.recv(42)
        if not received:
            print(' The first data received says', repr(data))
        if not data:
            break
        received += len(data)
        print('\r %d bytes received' % (received, ), end=' ')

    print()
    sock.close()


def tcpserver3(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print("Run this script in another window with '-c' to connect")
    print("Listening at ", sock.getsockname())

    sc, sockname = sock.accept()
    print("Accept connect from ", sockname)
    # close the write direction
    sc.shutdown(socket.SHUT_WR)
    message = b''

    # will get a full data from client that not split
    while True:
        more = sc.recv(8192)
        # sock has closed
        if not more:
            print("Received zero bytes - end of file")
            break
        print("Received {} bytes".format(len(more)))
        message += more
    print("Message: \n")
    print(message.decode('ascii'))
    sc.close()
    sock.close()


def tcpclient3(address):
    """
    set a full frame
    :param address:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    # close the read direction
    sock.shutdown(socket.SHUT_RD)
    # seal several frame
    sock.sendall(b"Beautiful is better than ugly.\n")
    sock.sendall(b"Explicit is better than implicit.\n")
    sock.sendall(b"Simple is better than complex.\n")
    # will send a empty str to server to express the end of send
    sock.close()


def tcpserver4(address):
    """
    use struct to block msg
    :param address:
    :return:
    """
    # message up to 2 * 32 - 1 in length
    header_struct = struct.Struct('!I')

    def recvall(sock, length):
        blocks = []
        while length:
            block = sock.recv(length)
            print('length..:', len(block))
            if not block:
                raise EOFError("sock closed with {0} bytes left"
                               " in this block".format(length))
            length -= len(block)
            blocks.append(block)
        return b''.join(blocks)

    def get_block(sock):
        # receive length info, header_struct.size: every frame up size
        data = recvall(sock, header_struct.size)
        (block_length, ) = header_struct.unpack(data)
        print('block length:', block_length)
        # receive the real data
        return recvall(sock, block_length)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print("Run this script in another window with '-c' to connect")
    print("Listening at ", sock.getsockname())

    sc, sockname = sock.accept()
    print("Accept connect from ", sockname)
    # close the write direction
    sc.shutdown(socket.SHUT_WR)

    # will get a full data from client that not split
    while True:
        print('get block...')
        block = get_block(sc)
        # sock has closed
        if not block:
            break
        print("Block says:", repr(block))
    sc.close()
    sock.close()


def tcpclient4(address):
    header_struct = struct.Struct('!I')

    def put_block(sock, message):
        block_length = len(message)
        # first send the length info
        sock.send(header_struct.pack(block_length))
        sock.send(message)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    # close the read direction
    sock.shutdown(socket.SHUT_RD)
    # seal several block
    put_block(sock, b"Beautiful is better than ugly.")
    put_block(sock, b"Explicit is better than implicit.")
    # mean the end
    put_block(sock, b'')
    # will send a empty str to server to express the end of send
    sock.close()


def tcpserver5(host, port, certfile, cafile=None):
    """
    use TLS
    :param host:
    :param port:
    :param certfile:
    :param cafile:
    :return:
    """
    purpose = ssl.Purpose.CLIENT_AUTH
    # create TLS obj, opt may change when new python edition release
    # cafile: trust CA agency, None: load the sys's CA
    # if openssl is enough new, the encode algorithm may support PFS
    # PFS: perfect forward security
    context = ssl.create_default_context(purpose=purpose, cafile=cafile)
    context.load_cert_chain(certfile=certfile)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((host, port))
    listener.listen(1)

    print(f"Listening at interface {host} and port {port}")

    raw_sock, address = listener.accept()
    print("Connecting from host {} and port".format(*address))
    # wrap sock, then will use TLS to communicate
    ssl_sock = context.wrap_socket(raw_sock, server_side=True)

    ssl_sock.sendall("Simple is better than complex".encode('ascii'))
    ssl_sock.close()


def tcpclient5(host, port, cafile=None):
    purpose = ssl.Purpose.SERVER_AUTH
    # if server have a cerfile, cafile must use to signature it
    context = ssl.create_default_context(purpose=purpose, cafile=cafile)

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    print(f"Connecting to host {host} and port {port}")
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)

    while True:
        data = ssl_sock.recv(1024)
        if not data:
            break
        print(repr(data))


class TCPServerClient6:
    """
    display the detail of TLS config
    """
    class PySSLSocket(ctypes.Structure):
        """
        The first few field of a PySSLSocket
        """
        _fields = [('ob_refcnt', ctypes.c_ulong), ('ob_type', ctypes.c_void_p),
                   ('Socket', ctypes.c_void_p), ('ssl', ctypes.c_void_p)]

    def open_tls(self, context, address, server=False):
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if server:
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            raw_sock.bind(address)
            raw_sock.listen(1)
            self.say("Interface we are listening", address)
            raw_client_sock, client_address = raw_sock.accept()
            self.say("Client has connected from address", address)
            return context.wrap_socket(raw_client_sock, server_side=True)
        else:
            self.say("Address we want to talk to", address)
            raw_sock.connect(address)
            return context.wrap_socket(raw_sock)

    def describe(self, ssl_sock, context, hostname, server=False, debug=False):
        cert = ssl_sock.getpeercert()
        if cert is None:
            self.say("Peer certificate", "None")
        else:
            self.say("Peer certificate", "provided")
            subject = cert.get('subject', [])
            names = [name for names in subject for (key, name) in names if key == 'commonName']

            if 'subjectAltName' in cert:
                names.extend(name for (key, name) in cert['subjectAltName'] if key == 'DNS')
            self.say("Name(s) on peer certificate", *names or ['none'])

            if not server and names:
                try:
                    ssl.match_hostname(cert, hostname)
                except ssl.CertificateError as e:
                    message = str(e)
                else:
                    message = 'yes'
                self.say("Whether name(s) match the hostname", message)
            for category, count in sorted(context.cert_store_stats().items()):
                self.say("Certificate loaded of type {}".format(category), count)

        try:
            protocol_version = self.SSL_get_version(ssl_sock)
        except Exception:
            if debug:
                raise
        else:
            self.say("Protocol negotiated", protocol_version)

        cipher, version, bits = ssl_sock.cipher()
        compression = ssl_sock.compression()

        self.say("Cipher chosen for this connection", cipher)
        self.say("Cipher defined in TLS version", version)
        self.say("Cipher this has many bits", bits)
        self.say("Compress algorithm in use", compression or 'none')

        return cert

    def SSL_get_version(self, ssl_sock):
        """
        Reach behind the scenes for a socket's TLS protocol version.
        :param ssl_sock:
        :return:
        """
        lib = ctypes.CDLL(ssl._ssl.__file__)
        lib.SSL_get_version.restype = ctypes.c_char_p
        address = id(ssl_sock.__sslobj)
        struct = ctypes.cast(address, ctypes.POINTER(self.PySSLSocket)).contents
        version_bytestring = lib.SSL_get_version(struct.ssl)
        return version_bytestring.decode('ascii')

    def look_up(self, prefix, name):
        if not name.startswith(prefix):
            name = prefix + name
        try:
            return getattr(ssl, name)
        except AttributeError:
            matching_names = (s for s in dir(ssl) if s.startwith(prefix))
            message = "Error: {!r} is not one of the available names: \n{}" \
                      "".format(name, ' '.join(sorted(matching_names)))
            print(self.fill(message), file=sys.stderr)
            sys.exit(2)

    def say(self, title, *words):
        print(self.fill(title.ljust(36, '.') + ' ' + ' '.join(str(w) for w in words)))

    @staticmethod
    def fill(text):
        return textwrap.fill(text, subsequent_indent=' ', break_long_words=False, break_on_hyphens=False)


class TCPUtils:
    aphorisms = {
        b"Beautiful is better than?": b"Ugly.",
        b"Explicit is better than?": b"Implicit.",
        b"Simple is better than?": b"Complex.",
    }

    def get_answer(self, aphorism):
        time.sleep(0.0)
        return self.aphorisms.get(aphorism, b"Error: unknown aphorism: " + aphorism + b'.')

    @staticmethod
    def parse_command_line(description):
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('placeholder', help='no use')
        parser.add_argument('host', help='IP address or hostname')
        parser.add_argument('p', metavar='port', type=int, default=1060,
                            help='TCP port number(default: %(default)s)')
        args = parser.parse_args()
        address = (args.host, args.p)
        return address

    @staticmethod
    def create_srv_socket(address):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(address)
        listener.listen(64)
        print("listening at {}".format(address))
        return listener

    def accept_connections_forever(self, listener):
        while True:
            # first connection will contain client request data, so first recv will be fast
            sock, address = listener.accept()
            print("Accept connection from {}".format(address))
            # will not accept other client util current session completed
            self.hand_conversation(sock, address)

    def hand_conversation(self, sock, address):
        try:
            while True:
                self.handle_request(sock)
        # self raise error
        except EOFError:
            print("Client socket to {} has closed".format(address))
        except Exception as e:
            print("Client {} error: {}".format(address, e))
        finally:
            sock.close()

    def handle_request(self, sock):
        aphorism = self.recv_until(sock, b'?')
        answer = self.get_answer(aphorism)
        sock.sendall(answer)

    @staticmethod
    def recv_until(sock, suffix):
        message = sock.recv(4096)
        print(message)
        if not message:
            raise EOFError("socket closed")
        while not message.endswith(suffix):
            data = sock.recv(4096)
            if not data:
                raise IOError('Received {!r} then socket closed'.format(message))
            message += data

        return message

    @asyncio.coroutine
    def hand_conversation_coroutine(self, reader, writer):
        address = writer.get_extra_info('peername')
        print("Accepted connection from {}".format(address))
        while True:
            data = b''
            while not data.endswith(b'?'):
                # not blocking
                more_data = yield from reader.read(4096)
                if not more_data:
                    if data:
                        print('Client {} sent {!r} but then closed'.format(address, data))
                    else:
                        print('Client {} closed socket normally'.format(address))
                    return
                data += more_data
            answer = self.get_answer(data)
            writer.write(answer)


def tcpclient7():
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('placeholder', help='no use')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-e', action='store_true', help='cause a error')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port default(%(default))')

    args = parser.parse_args()
    address = (args.host, args.p)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    tcp_util = TCPUtils()

    aphorisms = list(tcp_util.aphorisms)
    if args.e:
        sock.sendall(aphorisms[0][:1])
        return
    for aphorism in random.sample(aphorisms, 3):
        sock.sendall(aphorism)
        print(aphorism, tcp_util.recv_until(sock, b'.'))
    sock.close()


def tcpserver10(listener):
    """
    register socket to poll event
    :param listener:
    :return:
    """
    def all_events_forever(poll_obj):
        while True:
            # always poll
            for fd, event in poll_obj.poll():
                yield fd, event

    sockets = {listener.fileno(): listener}
    addresses = {}
    bytes_received = {}
    bytes_to_sends = {}

    poll_obj = select.poll()
    poll_obj.register(listener, select.POLLIN)

    tcp_util = TCPUtils()

    for fd, event in all_events_forever(poll_obj):
        sock = sockets[fd]

        if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            address = addresses.pop(sock)
            rb = bytes_received.pop(sock, b'')
            sb = bytes_to_sends.pop(sock, b'')
            if rb:
                print('Client {} sent {} but then closed'.format(address, rb))
            elif sb:
                print('Client {} closed before we send {}'.format(address, sb))
            else:
                print('Client {} closed socket normally'.format(address))
            poll_obj.unregister(fd)
            del sockets[sock]
        # there is new client to connect
        elif sock is listener:
            sock, address = listener.accept()
            print('Accept connection from {}'.format(address))
            # set no blocking mode
            sock.setblocking(False)
            sockets[sock.fileno()] = sock
            addresses[sock] = address

            # register in poll, and thus sock will not block with recv and send method
            poll_obj.register(sock, select.POLLIN)
        elif event & select.POLLIN:
            more_data = sock.recv(4096)
            if not more_data:
                # next poll() will POLLNVAL, and thus clean up
                sock.close()
                continue

            data = bytes_received.pop(sock, 'b') + more_data
            if data.endswith(b'?'):
                bytes_to_sends[sock] = tcp_util.get_answer(data)
                poll_obj.modify(sock, select.POLLOUT)
            else:
                bytes_received[sock] = data
        elif event & select.POLLOUT:
            data = bytes_to_sends.pop(sock)
            n = sock.send(data)

            if n < len(data):
                bytes_to_sends[sock] = data[n:]
            else:
                poll_obj.modify(sock, select.POLLIN)


class TcpServer11(asyncio.Protocol):
    tcp_util = TCPUtils()

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.data = b''
        print('Accepted connection from {}'.format(self.address))

    # recv and send hide in this method
    def data_received(self, data: bytes) -> None:
        self.data += data
        if self.data.endswith(b'?'):
            # operate may be more complex, such as read db
            # so the asyncio should deal both connection between server and client
            # and connection between server and db
            answer = self.tcp_util.get_answer(self.data)
            self.transport.write(answer)
            self.data = b''

    def connection_lost(self, exc) -> None:
        if exc:
            print("Client {} error: {}".format(self.address, exc))
        elif self.data:
            print("Client {} sent {} but closed".format(self.address, self.data))
        else:
            print("Client {} closed socket".format(self.address))


class TcpServer13(asyncore.dispatcher):
    class ReqHandler(asynchat.async_chat):
        tcp_util = TCPUtils()

        def __init__(self, sock):
            asynchat.async_chat.__init__(self, sock)
            # data not contain terminator
            self.set_terminator(b'?')
            self.data = b''

        def collect_incoming_data(self, more_data):
            self.data += more_data

        def found_terminator(self):
            answer = self.tcp_util.get_answer(self.data + b'?')
            self.push(answer)
            self.initiate_send()
            self.data = b''

    def handle_accept(self) -> None:
        sock, address = self.accept()
        # every accept will deliver to new handler
        self.ReqHandler(sock)


def getaddr():
    # get the addrinfo of server, may return not only addr, aim to disbute press
    addr_info = socket.getaddrinfo('baidu', 'www')
    # can know which ip and port can use to transfer of smtp, 0: general pair protocol
    addr_info2 = socket.getaddrinfo('127.0.0.1', 'smtp', 0, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    # AI_ADDRCONFIG: filer the invalid addr, AI_V4MAPPED: map ipv4 to ipv6
    addr_info3 = socket.getaddrinfo('baidu.com', 'www', 0, socket.SOCK_STREAM, 0, socket.AI_ADDRCONFIG | socket.AI_V4MAPPED)
    # AI_CANONNAME reverse search: get host name according, but the return result may be anything
    addr_info4 = socket.getaddrinfo('baidu.com', 'www', 0, socket.SOCK_STREAM, 0,
                                    socket.AI_ADDRCONFIG | socket.AI_V4MAPPED | socket.AI_CANONNAME)
    # my_sock = server_sock.accept()
    # addr, port = my_sock.getpeername()
    # get host name through the connect info of client, cannot get info if client no define the reverse host name
    # addr_info5 = socket.getaddrinfo(addr, port, my_sock.family, my_sock.type, my_sock.proto, socket.AI_CANONNAME)

    # get host name
    hn = socket.gethostname()
    # get full host info
    hn2 = socket.getfqdn()
    # get ip by host name
    ip = socket.gethostbyname('tbq-pc')
    # get host info by ip
    host_info = socket.gethostbyaddr('127.0.0.1')
    # get pro no
    pro_no = socket.getprotobyname('UDP')
    # get serv
    port = socket.getservbyname('www')
    # get serv
    serv = socket.getservbyport(80)


def connect_www_through_host_info(hostname_or_ip):
    try:
        addr_info = socket.getaddrinfo(hostname_or_ip, 'www', 0, socket.SOCK_STREAM, 0,
                                       socket.AI_ADDRCONFIG | socket.AI_V4MAPPED | socket.AI_CANONNAME)
    except socket.gaierror as e:
        print("Name service failure:", e.args[1])
        sys.exit(1)
    try_first_addr = addr_info[0]

    addr_family = try_first_addr[0].value
    sock_type = try_first_addr[1].value
    proto_type = try_first_addr[2]
    ip = try_first_addr[4][0]
    port = try_first_addr[4][1]
    host_name = try_first_addr[3]

    sock = socket.socket(addr_family, sock_type, proto_type)
    try:
        sock.connect((ip, port))
    except socket.error as e:
        print('Network failure: ', e.args[1])
    else:
        print("Success host ", host_name, 'is listening on port ', port)


def lookup_dns(host_name):
    # ipv4, ipv6, other name, mail server, name server
    for qtype in ('A', 'AAAA', 'CNAME', 'MX', 'NS'):
        answer = dns.resolver.query(host_name, qtype, raise_on_no_answer=False)
        if answer.rrset is not None:
            # result format: name valid_cache_time class addr_type
            print(answer.rrset)


def resolve_email_domain(domain):
    # try: A->AAAA->CNAME
    def resolve_hostname(hostname, indent=''):
        indent = indent + ' '
        answer = dns.resolver.query(hostname, 'A')

        if answer.rrset is not None:
            for record in answer:
                print(indent, hostname, 'has A address', record.address)
            return
        answer = dns.resolver.query(hostname, 'AAAA')
        if answer.rrset is not None:
            for record in answer:
                print(indent, hostname, 'has AAAA address', record.address)
            return
        answer = dns.resolver.query(hostname, 'CNAME')
        if answer.rrset is not None:
            record = answer[0]
            cname = record.address
            print(indent, hostname, 'is a CNAME alias for', cname)
            resolve_hostname(cname, indent)
            return

        print(indent, 'ERROR: no A, AAAA, CNAME record for', hostname)

    try:
        answer = dns.resolver.query(domain, 'MX', raise_on_no_answer=False)
    except dns.resolver.NXDOMAIN:
        print('No such domain', domain)
        return
    if answer.rrset is not None:
        records = sorted(answer, key=lambda record: record.preference)
        for idx, record in enumerate(records, start=1):
            name = record.exchange.to_text(omit_final_dot=True)
            print("This domain has ", idx, 'th MX record')
            print('Priority', record.preference)
            resolve_hostname(name)
    else:
        print("This domain has no explicit MX record")
        print("Attempting resolve it as an A, AAAA, or CNAME")
        resolve_hostname(domain)


def memcache1():
    def compute(mc, n):
        # key is str that is a genera key
        # get value from the memcache first
        # so it will cost a shorter time
        # memcache will lost data that no use for long time
        value = mc.get('sq:%d' % n)
        if value is None:
            time.sleep(0.001)
            value = n * n
            mc.set('sq:%d' % n, value)
        return value

    # should run the memcache process before connect
    mc = memcache.Client(['127.0.0.1:11211'])

    def make_request():
        compute(mc, random.randint(0, 5000))

    print('Ten successive runs:')
    for i in range(1, 11):
        print(' %.2fs' % timeit.timeit(make_request, number=2000), end='')
    print()


def hash1():
    """divide work with difference way, that hash is best way"""

    def alpha_shard(word):
        if word[0] < 'g':
            return 'server0'
        elif word[0] < 'n':
            return 'server1'
        elif word[0] < 't':
            return 'server2'
        else:
            return 'server3'

    def hash_shard(word):
        return 'server%d' % (hash(word) % 4)

    def md5_shard(word):
        data = word.encode('utf-8')
        return 'server%d' % (hashlib.md5(data).digest()[-1] % 4)

    words = 'in this lift time you do not have to prove nothing to nobody except yourself'.split()
    word_len = len(words)
    for function in alpha_shard, hash_shard, md5_shard:
        d = {'server0': 0, 'server1': 0, 'server2': 0, 'server3': 0}
        for word in words:
            d[function(word)] += 1
        print(function.__name__[:-6])
        for key, value in sorted(d.items()):
            print(' {} {} {:.2}'.format(key, value, value / word_len))
        print()


class MsgQueue:
    B = 32

    @staticmethod
    def ones_and_zeros(digits):
        return bin(random.getrandbits(digits)).lstrip('0b').zfill(digits)

    def bitsources(self, zcontext, url):
        zsock = zcontext.socket(zmq.PUB)
        zsock.bind(url)
        while True:
            zsock.send_string(self.ones_and_zeros(self.B * 2))
            time.sleep(0.01)

    @staticmethod
    def aways_yes(zcontext, in_url, out_url):
        isock = zcontext.socket(zmq.SUB)
        isock.connect(in_url)
        isock.setsockopt(zmq.SUBCIREBE, b'00')
        osock = zcontext.socket(zmq.PUSH)
        osock.connect(out_url)
        while True:
            isock.recv_string()
            osock.send_string('Y')

    def judge(self, zcontext, in_url, pythagoras_url, out_url):
        isock = zcontext.socket(zmq.SUB)
        isock.connect(in_url)
        for prefix in b'01', b'10', b'11':
            isock.setsockopt(zmq.SUBCRIBE, prefix)
        psock = zcontext.socket(zmq.REQ)
        psock.connect(pythagoras_url)
        osock = zcontext.socket(zmq.PUSH)
        osock.connect(out_url)
        unit = 2 ** (self.B * 2)
        while True:
            bits = isock.recv_string()
            n, m = int(bits[::2], 2), int(bits[1::2], 2)
            psock.send_json((n, m))
            sumsquares = psock.recv_json()
            osock.send_string('Y' if sumsquares < unit else 'N')

    @staticmethod
    def pythagoras(zcontext, url):
        zsock = zcontext.socket(zmq.REP)
        zsock.bind(url)
        while True:
            numbers = zsock.recv_json()
            zsock.send_json(sum(n * n for n in numbers))

    @staticmethod
    def tally(zcontext, url):
        zsock = zcontext.socket(zmq.PULL)
        zsock.bind(url)
        p = q = 0
        while True:
            decision = zsock.recv_string()
            q += 1
            if decision == 'Y':
                p += 4
            print(decision, p / q)


def msg_queue():
    def start_thread(function, *args):
        thread = Thread(target=function, args=args)
        thread.daemon = True
        thread.start()

    pubsub = 'tcp://127.0.0.1:6700'
    reqrep = 'tcp://127.0.0.1:6701'
    pushpull = 'tcp://127.0.0.1:6702'

    mq_obj = MsgQueue()
    zcontext = zmq.Context()

    # it is not safe that multiple thread share one socket
    start_thread(mq_obj.bitsources, zcontext, pubsub)
    start_thread(mq_obj.aways_yes, zcontext, pubsub, pushpull)
    start_thread(mq_obj.judge, zcontext, pubsub, reqrep, pushpull)
    start_thread(mq_obj.pythagoras, zcontext, reqrep)
    start_thread(mq_obj.tally, zcontext, pushpull)
    time.sleep(30)


def bootudp():
    choices = {'client': udpclient3, 'server': udpserver3}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listen at;'
                        'host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    # function(args.p)
    function(args.host, args.p)


def boottcp():
    choices = {'client': tcpclient1, 'server': tcpserver1}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        'host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)


def boottcp2():
    choices = {'client': tcpclient2, 'server': tcpserver2}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        'host the client sends to')
    parser.add_argument('bytecount', type=int, nargs='?', default=16, help='number of bytes for client to send (default 16)')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p, args.bytecount)


def boottcp3():
    parser = argparse.ArgumentParser(description='Transmit & receive a data stream')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1',
                        help='IP address or hostname(default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='run as the client')
    parser.add_argument('-p', type=int, metavar='port', default=1060,
                        help='TCP port number(default: %(default)s)')
    args = parser.parse_args()

    function = tcpclient3 if args.c else tcpserver3
    function((args.hostname, args.p))


def boottcp4():
    parser = argparse.ArgumentParser(description='Transmit & receive a data stream')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1',
                        help='IP address or hostname(default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='run as the client')
    parser.add_argument('-p', type=int, metavar='port', default=1060,
                        help='TCP port number(default: %(default)s)')
    args = parser.parse_args()

    function = tcpclient4 if args.c else tcpserver4
    function((args.hostname, args.p))


def boottcp5():
    parser = argparse.ArgumentParser(description='Transmit & receive a data stream')
    parser.add_argument('host', nargs='?', default='127.0.0.1',
                        help='IP address or hostname(default: %(default)s)')
    parser.add_argument('port', type=int, default=1060, help='TCP port number(default: %(default)s)')
    # signature file
    parser.add_argument('-a', metavar='cafile', default=None,
                        help='authority: path to CA certificate PEM file')
    parser.add_argument('-s', metavar='certfile', default=None,
                        help='run as server: path to server PEM file')
    args = parser.parse_args()

    if args.s:
        tcpserver5(args.host, args.port, args.s, args.a)
    else:
        tcpclient5(args.host, args.port, args.a)


def boottcp6():
    from pprint import pprint

    parser = argparse.ArgumentParser(description='Transmit & receive a data stream')
    parser.add_argument('host', nargs='?', default='127.0.0.1',
                        help='IP address or hostname(default: %(default)s)')
    parser.add_argument('port', type=int, default=1060, help='TCP port number(default: %(default)s)')
    # signature file
    parser.add_argument('-a', metavar='cafile', default=None,
                        help='authority: path to CA certificate PEM file')
    parser.add_argument('-c', metavar='certfile', default=None,
                        help='authority: path to PEM file with client certificate')
    parser.add_argument('-C', metavar='ciphers', default='ALL',
                        help='list of ciphers, formatted for per OpenSSL')
    parser.add_argument('-p', metavar='PROCOTOL', default='SSLv23',
                        help='protocol version(default: "SSLv23")')
    parser.add_argument('-s', metavar='certfile', default=None,
                        help='run as server: path to server PEM file')
    parser.add_argument('-d', action='store_true', default=False,
                        help='debug mode: do not hide "ctypes" exceptions')
    parser.add_argument('-v', action='store_true', default=False,
                        help='verbose: print out remote certificate')

    args = parser.parse_args()

    address = (args.host, args.port)

    tcp_obj = TCPServerClient6()
    # if the protocol of client not match server demand, will connect fail
    protocol = tcp_obj.look_up('PROTOCOL_', args.p)

    context = ssl.SSLContext(protocol)
    context.set_ciphers(args.C)
    context.check_hostname = False

    if args.s is not None and args.c is not None:
        parser.error("you cannot specify both -c and -s")
    elif args.s is not None:
        context.verify_mode = ssl.CERT_OPTIONAL
        purpose = ssl.Purpose.CLIENT_AUTH
        context.load_cert_chain(args.s)
    else:
        context.verify_mode = ssl.CERT_REQUIRED
        purpose = ssl.Purpose.SERVER_AUTH
        if args.c is not None:
            context.load_cert_chain(args.c)
    if args.a is None:
        context.load_default_certs(purpose)
    else:
        context.load_verify_locations(args.a)

    print()
    ssl_sock = tcp_obj.open_tls(context, address, args.s)
    cert = tcp_obj.describe(ssl_sock, context, args.host, server=args.s, debug=args.d)
    print()
    if args.v:
        pprint(cert)


def boottcp7():
    role = sys.argv[1]

    tcp_util = TCPUtils()

    if role == 'server7':
        address = tcp_util.parse_command_line('simple single-threaded server')
        listener = tcp_util.create_srv_socket(address)
        tcp_util.accept_connections_forever(listener)
    elif role == 'server8':
        address = tcp_util.parse_command_line('multiple single-threaded server')
        listener = tcp_util.create_srv_socket(address)
        # create specify amount of thread for server,
        # so can accept multiple connection at the same time
        worker = 4
        for i in range(worker):
            Thread(target=tcp_util.accept_connections_forever, args=(listener,)).start()
    elif role == 'server9':
        class ReqHandler(BaseRequestHandler):
            def handle(self) -> None:
                tcp_util.hand_conversation(self.request, self.client_address)

        # ForkingMixIn: use apart process to accept client, not threading
        class Server(ThreadingMixIn, TCPServer):
            allow_reuse_address = 1
            request_queue_size = 4

        address = tcp_util.parse_command_line('legacy "SocketServer" server')
        # two mode: server, handler, but it not limit thread amount, therefore this isn't safe
        server = Server(address, ReqHandler)
        server.serve_forever()
    elif role == 'server10':
        address = tcp_util.parse_command_line('low-level async server')
        listener = tcp_util.create_srv_socket(address)
        # only one thread, buy can accept multiple connection through poll
        # tips: poll only available in linux
        tcpserver10(listener)
    elif role == 'server11':
        address = tcp_util.parse_command_line('asyncio server using callbacks')
        loop = asyncio.get_event_loop()
        # only one thread, but can deal multiple connection at the same time
        coro = loop.create_server(TcpServer11, *address)
        server = loop.run_until_complete(coro)
        print("Listening at {}".format(address))
        try:
            loop.run_forever()
        finally:
            server.close()
            loop.close()
    elif role == 'server12':
        address = tcp_util.parse_command_line('asyncio server using coroutine')
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(tcp_util.hand_conversation_coroutine, *address)
        server = loop.run_until_complete(coro)
        print("Listening at {}".format(address))
        try:
            loop.run_forever()
        finally:
            server.close()
            loop.close()
    elif role == 'server13':
        address = tcp_util.parse_command_line('legacy "asyncore" server')
        listener = tcp_util.create_srv_socket(address)
        server = TcpServer13(listener)
        # already call listen()
        server.accepting = True
        asyncore.loop()
    elif role == 'server14':
        # use inted daemon to run socket, not available in window
        # inetd will manage its process, such as reboot server
        # /etc/inetd.conf:
        # 1060 stream tcp nowait tbq /usr/bin/python3 /usr/bin/python3 server.py
        # distribute every client connection to a new process
        # nowait: accept control by process
        # run: inetd -d inet.conf
        sock = socket.fromfd(0, socket.AF_INET, socket.SOCK_STREAM)
        # not real operate the fd, only file instance, thus unnecessary call close
        sys.stdin = open('/dev/null', 'r')
        sys.stdout = sys.stderr = open('log.txt', 'a', buffering=1)
        address = sock.getpeername()
        print("Accepted connection from {}".format(address))
        tcp_util.hand_conversation(sock, address)
    elif role == 'server15':
        sock = socket.fromfd(0, socket.AF_INET, socket.SOCK_STREAM)
        sys.stdin = open('/dev/null', 'r')
        sys.stdout = sys.stderr = open('log.txt', 'a', buffering=1)
        sock.settimeout(9)
        try:
            # if conf to 'wait', accept method deliver to script,
            # so one process can accept multiple connection
            tcp_util.accept_connections_forever(sock)
        except socket.timeout:
            print('Waited 9 seconds with no further connection; shutting down')
    elif role == 'client7':
        tcpclient7()


def main():
    hash1()


if __name__ == '__main__':
    main()
