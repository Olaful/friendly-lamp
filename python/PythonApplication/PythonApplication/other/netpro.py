#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import socket
import argparse
from datetime import datetime
import time, timeit
import random
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
import requests
from urllib.request import urlopen
import urllib.error
from wsgiref.simple_server import make_server
import os, pprint, sqlite3
from collections import namedtuple
from flask import Flask, redirect, request, url_for, flash, get_flashed_messages, \
    render_template, session, abort
from jinja2 import Environment, PackageLoader
import uuid
import bs4, lxml.html, requests
from selenium import webdriver
from urllib.parse import urljoin, urlsplit
from lxml import etree


def getlltitude():
    """
    协议层次api<-url<-http<-tcp/ip
    :return:
    """
    from pygeocoder import Geocoder

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
    import http.client
    from urllib.parse import quote_plus

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
    udp相比于tcp,为不可靠传输,即不保证数据的准确送达,没有保存
    连接会话
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
    """
    mode: 1.pub-sub; 2.req-rep 3.push-pull
    """
    B = 32

    @staticmethod
    def ones_and_zeros(digits):
        return bin(random.getrandbits(digits)).lstrip('0b').zfill(digits)

    def bitsources(self, zcontext, url):
        # PUB: producer - to more consumer
        zsock = zcontext.socket(zmq.PUB)
        zsock.bind(url)
        while True:
            zsock.send_string(self.ones_and_zeros(self.B * 2))
            time.sleep(0.01)

    @staticmethod
    def aways_yes(zcontext, in_url, out_url):
        # SUB: consumer
        isock = zcontext.socket(zmq.SUB)
        # if connect before server bind the url, zmq will timed poll
        # to try connect
        isock.connect(in_url)
        # filter: b'00' only recv the msg which start with b'00'
        isock.setsockopt(zmq.SUBSCRIBE, b'00')
        osock = zcontext.socket(zmq.PUSH)
        osock.connect(out_url)
        while True:
            isock.recv_string()
            osock.send_string('Y')

    def judge(self, zcontext, in_url, pythagoras_url, out_url):
        isock = zcontext.socket(zmq.SUB)
        isock.connect(in_url)
        for prefix in b'01', b'10', b'11':
            isock.setsockopt(zmq.SUBSCRIBE, prefix)
        # req-rep will consider the tcp protocol common problem
        psock = zcontext.socket(zmq.REQ)
        psock.connect(pythagoras_url)
        # PUSH: producer - to one consumer
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
            # actually send to the client who send msg to the server, like common tcp
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
    # in order to avoid main process quit fast, let the thread run longer to
    # produce more example data
    time.sleep(30)


def http_client1():
    url = 'http://httpbin.org/headers'

    r = requests.get(url)
    # support gzip and deflate formation response
    # also can specify Accept-Encoding: gzip in the headers
    # requests will unzip data in backstage
    # requests not support cache
    # Accept: text/html;q=0.9, text/plain, image/jpg, */*;q=0.8
    # accept content will distribute diff weight, first weight equal 1
    # Content-Type: text/html; charset=utf-8 => specify charset of server data
    print(r.text)

    s = requests.Session()
    # customize header
    s.headers.update({'Accept-Language': 'en-US, en;q=0.8'})
    # auth, later get and post can use this auth msg
    s.auth = 'tbq', '123'
    # use cookies
    s.cookies.set('user', 'tbq')

    # urllib not support reuse tcp connection
    import http.client
    h = http.client.HTTPConnection('localhost:8000')
    h.request('GET', '/ip')
    r = h.getresponse()
    print(r.status)

    # will recreate a new tcp connection
    h.request('GET', '/user-agent')
    r = h.getresponse()
    print(r.status)

    # urllib not support cache
    r = urlopen(url)
    # not support gzip and deflate formation response
    # default use get method
    print(r.read().decode('ascii'))


def http_client2():
    url = 'http://httpbin.org/status/301'

    r = requests.get(url)
    print(r.status_code, r.url)
    # show the redirect his
    print(r.history)

    # not allow redirect
    r = requests.get(url, allow_redirects=False)
    r.raise_for_status()
    print(r.status_code, r.url, r.headers['Location'])

    # will redirect to https://www.baidu.com
    r = requests.get('https://baidu.com')
    print(r.url)

    # get error msg from Error obj
    try:
        urlopen('http://httpbin.org/status/500')
    except urllib.error.HTTPError as e:
        print(e.status, repr(e.headers['Content-Type']))

    requests.get('http://httpbin.org/status/500')
    # if http error, will raise error, if not call this method
    # then will not raise error
    r.raise_for_status()
    print(r.status_code)


def http_block_frame():
    # req rep
    # first end with CR-LF(回车换行)
    # whole end with CR-LF-CR-LF(空行)

    req = """
        GET /ip HTTP/1.1
        ...
    """

    # block frame according to Content-Length
    # Transfer-Encoding: chunked =>
    # hex_len : CR-LF : data : CR-LF
    # end => 0 : CR-LF : empty data : CR-LF
    # Connection: close =>
    # server once send msg over then close the socket
    # status code: 200
    # 200-300: success, 300-400: redirect, 400-500: not know or illicit
    # 500-600: server error
    # 3xx not contain msg body, but 4xx and 5xx contain
    rep = """
        HTTP/1.1 200 OK
        ...
        Content-Length: 27
    """


def http_method():
    """
    get: only get data not modify server data
    post: can modify server data, can't retry without rep of server
    options: only req the path that pair the http header
    head: only sent the head msg
    put: like post, can modift server data, put a document to server
    can retry without rep of server
    delete: req to delete specify path and that data under the path
    can retry without rep of server
    trace: debug
    connect: convert protocol from http to other protocol
    :return:
    """


def wsgi_app1():
    # wsgi: make the middleware between http server and web server
    # but not support async, other framework like Twisted, Tornado
    # support async

    from pprint import pformat

    # this app should be callable
    # environ contains the req info
    def app(environ, start_response):
        headers = {'Content-Type': 'text/plain; charset=utf-8'}
        start_response('200 ok', list(headers.items()))
        yield 'Here is the WSGI environment:\r\n\r\n'.encode('utf-8')
        yield pformat(environ).encode('utf-8')

    # other framework can call app like this
    httpd = make_server('', 800, app)
    host, port = httpd.socket.getsockname()
    print('Serving on ', host, 'port ', port)
    httpd.serve_forever()


def wsgi_app2():
    """
    write callable obj without framework, so
    you must parse url req, but framework will
    do this task
    :return:
    """
    def app(environ, start_response):
        host = environ.get('HTTP_HOST', '127.0.0.1')
        path = environ.get('PATH_INFO', '/')

        if ':' in host:
            host, port = host.split(':', 1)
        if '?' in path:
            path, query = path.split('?', 1)
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        if environ['REQUEST-METHOD'] != 'GET':
            start_response('501 Not Implemented', headers)
            yield b'501 Not Implemented'
        elif host != '127.0.0.1' or path != '/':
            start_response('404 Not Found', headers)
            yield b'404 Not Found'
        else:
            start_response('200 OK', headers)
            yield time.ctime().encode('ascii')


def wsgi_app3():
    """
    use webob deal with req and rep
    :return:
    """

    import webob

    def app(environ, start_response):
        request = webob.Request(environ)
        if environ['REQUEST_METHOD'] != 'GET':
            response = webob.Response('501 Not Implemented', status=501)
        elif request.domain != '127.0.0.1' or request.path != '/':
            response = webob.Response('404 Not Found', status=404)
        else:
            response = webob.Response(time.ctime())
        return response(environ, start_response)


def wsgi_app4():
    """
    use werkzeug deal with req and rep
    :return:
    """

    from werkzeug.wrappers import Request, Response

    @Request.application
    def app(request):
        host = request.host
        if ':' in host:
            host, port = host.split(':', 1)
        if request.method != 'GET':
            return Response('501 Not Implemented', status=501)
        elif host != '127.0.0.1' or request.path != '/':
            return Response('404 Not Found', status=404)
        else:
            return Response(time.ctime())


def server_framework():
    """
    httpserver -> wsgi
    apache -> mod_wsgi:
    if use mod_python, every apache thread reserve a python interpreter,
    but only one thread can run python at the same time
    reverse proxy(like apache, nginx) -> httpserver(like gunicorn):
    static source will delivery to reverse proxy to deal, dynamic source can delivery to server,
    reverse proxy will save the uncompleted req to the cache, if req over, then actually send to
    server, some error req will directly deny
    reverse proxy(like varnish) -> (apache, nginx) -> httpserver
    other: varnish -> httpserver: if you don't need reverse proxy to deal static source
    :return:
    """


def http_standard():
    """
    rest =>
    1. url: explict locate src
    2. src format: such as html, json, so can accepted by common customer
    3. msg self describe: such as can cache data through msg info
    4. hateoas
    protocol://hostname/path/querystring
    hyperlink: word and link
    http://www.baidu.com/otherpath?q=hello&page=10
    :return:
    """


def parse_build_url():
    from urllib.parse import urlsplit, parse_qs, parse_qsl, unquote, \
        quote, urlunsplit, urlencode, urljoin
    # split url
    u = urlsplit('https://www.google.com/search?q=apod&btnI=yes')
    scheme = u.scheme
    netloc = u.netloc

    # \s encode to %20 or +
    u = urlsplit('http://example/com/Q%26A/TCP%2FIP?q=packet+loss')
    path = [unquote(s) for s in u.path.split('/')]
    query = parse_qsl(u.query)
    # query word can be same, parse_qs: key: [v1, v2]
    query2 = parse_qs(u.query)

    # build url, safe: if is '/', will directly regard as normal char
    u = urlunsplit(('http', 'example.com', '/'.join(quote(p, safe='') for p in path), urlencode(query), ''))
    print(u)

    # if '/' append to the end, then current dir is rfc3986, otherwise html
    base = 'http://tools.ietf.org/html/rfc3986'
    print(urljoin(base, 'rfc7320'))
    print(urljoin(base, '.'))
    print(urljoin(base, '..'))
    print(urljoin(base, '/dailydose'))
    print(urljoin(base, '?version=1.0'))
    print(urljoin(base, '#section-5.4'))
    # directly return the absolute address
    print(urljoin(base, 'https://www.baidu.com'))
    # http will join to the head
    print(urljoin(base, '//www.baidu.com'))


class DB1:
    def open_database(self, path=r'E:\file\bank.db'):
        new = not os.path.exists(path)
        db = sqlite3.connect(path)
        if new:
            c = db.cursor()
            c.execute('CREATE TABLE payment(id INTERGER PRIMARY KEY, '
                      ' debit TEXT, credit TEXT, dollars INTERGER, memo TEXT)')
            self.add_payment(db, 'debit1', 'credit1', 125, 'Registration for PyCon')
            self.add_payment(db, 'debit1', 'credit2', 200, 'Payment for writing that code')
            self.add_payment(db, 'debit2', 'debit1', 25, 'Gas money-thanks for the ride')

            db.commit()

        return db

    @staticmethod
    def add_payment(db, debit, credit, dollars, memo):
        db.cursor().execute('INSERT INTO payment(debit, credit, dollars, memo) '
                            ' VALUES(?, ?, ?, ?)', (debit, credit, dollars, memo))

    @staticmethod
    def get_payments_of(db, account):
        c = db.cursor()
        c.execute('SELECT * FROM payment WHERE credit = ? or debit = ?'
                  ' ORDER BY id', (account, account))
        # can get value like Row.attr, it is readable
        Row = namedtuple('Row', [tup[0] for tup in c.description])
        return [Row(*row) for row in c.fetchall()]


class InsecureWebApp:
    app = Flask(__name__)
    sys.path.append(r'E:\\')
    get = Environment(loader=PackageLoader('myhtml', 'templates')).get_template
    db_obj = DB1()

    # attacker can via XSS(cross-site scripting)
    # to attack if webserver run this script
    """
    <script>
    var x = new XMLHTTPRequest();
    x.open('POST', 'http://localhost:5000/pay');
    x.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    x.send('account=hacker&dollars=100&memo=Theft);
    </script>
    """

    @staticmethod
    # post method will not display query world in url
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if request.method == 'POST':
            if (username, password) in [('user1', 'pwd1'), ('user2', 'pwd2')]:
                response = redirect(url_for('index'))
                # if cookies have set, so can through requests.post('url', cookies={'username': 'user1'})
                # to entry another url, so this cookie is not safe, can encode cookie or certify to ensure
                # safety
                response.set_cookie('username', username)
                return response
        return InsecureWebApp.get('login.html').render(username=username)

    @staticmethod
    @app.route('/logout')
    def logout():
        response = redirect(url_for('login'))
        response.set_cookie('username', '')
        return response

    @staticmethod
    @app.route('/')
    def index():
        username = request.cookies.get('username')
        if not username:
            return redirect(url_for('login'))
        payments = InsecureWebApp.db_obj.get_payments_of(InsecureWebApp.db_obj.open_database(), username)
        return InsecureWebApp.get('index.html').render(payments=payments, username=username,
                                                       flash_messages=request.args.getlist('flash'))

    @staticmethod
    @app.route('/pay', methods=['GET', 'POST'])
    def pay():
        username = request.cookies.get('username')
        if not username:
            return redirect(url_for('login'))
        account = request.form.get('account', '').strip()
        dollars = request.form.get('dollars', '').strip()
        memo = request.form.get('memo', '').strip()
        complaint = None
        if request.method == 'POST':
            if account and dollars and dollars.isdigit() and memo:
                db = InsecureWebApp.db_obj.open_database()
                InsecureWebApp.db_obj.add_payment(db, username, account, dollars, memo)
                db.commit()
                return redirect(url_for('index', flash='Payment successful'))
            complaint = ('Dollars must be an interger' if not dollars.isdigit()
                         else 'Please fill in all three fields')
        return InsecureWebApp.get('pay.html').render(complaint=complaint, account=account,
                                                     dollars=dollars, memo=memo)


class ImproveWebApp:
    app = Flask(__name__)
    # use secret key to sign cookies
    app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'
    app.template_folder = r'E:\python\myhtml\templates'
    db_obj = DB1()

    @staticmethod
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if request.method == 'POST':
            if (username, password) in [('user1', 'pwd1'), ('user2', 'pwd2')]:
                session['username'] = username
                # post will contain this token, if illegal user
                # forgery form data, but not pair the real session token
                # that will be forbidden by the server
                session['csrf_token'] = uuid.uuid4().hex
                return redirect(url_for('index'))
        # will escape such as '<', so str that include js will not run
        return render_template('login.html', username=username)

    @staticmethod
    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('login'))

    @staticmethod
    @app.route('/')
    def index():
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))
        payments = InsecureWebApp.db_obj.get_payments_of(InsecureWebApp.db_obj.open_database(), username)
        return render_template('index.html', payments=payments, username=username,
                                                       # get_flashed_messages will consider the attack of xss
                                                       flash_messages=get_flashed_messages())

    @staticmethod
    @app.route('/pay', methods=['GET', 'POST'])
    def pay():
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))
        account = request.form.get('account', '').strip()
        dollars = request.form.get('dollars', '').strip()
        memo = request.form.get('memo', '').strip()
        complaint = None
        if request.method == 'POST':
            if request.form.get('csrf_token') != session['csrf_token']:
                abort(403)
            if account and dollars and dollars.isdigit() and memo:
                db = InsecureWebApp.db_obj.open_database()
                InsecureWebApp.db_obj.add_payment(db, username, account, dollars, memo)
                db.commit()
                # flash msg will send to index
                flash('Payment successful')
                return redirect(url_for('index'))
            complaint = ('Dollars must be an interger' if not dollars.isdigit()
                         else 'Please fill in all three fields')
        return render_template('pay2.html', complaint=complaint, account=account,
                                                     dollars=dollars, memo=memo,
                                                        csrf_token=session['csrf_token'])

    @staticmethod
    @app.route('/robots.txt', methods=['GET'])
    def test():
        return 'hello world'


def web_app_with_django():
    """
    使用django重新实现
    login与logout可以直接使用框架内置的功能
    csrf也提供支持
    支持orm对象映射
    :return:
    """


def insecure_web_app():
    iwa = InsecureWebApp()
    iwa.app.debug = True
    iwa.app.run()


def improve_web_app():
    iwa = ImproveWebApp()
    iwa.app.debug = False
    iwa.app.run()


def attack_url1():
    """
    nonpersistent xss
    some explorer will prevent xss
    :return:
    """
    from urllib.parse import urlencode
    attack_js = """
    <script>
    var x = new XMLHTTPRequest();
    x.open('POST', 'http://localhost:5000/pay');
    x.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    x.send('account=hacker&dollars=100&memo=Theft);
    </script>
    """
    attack_js = attack_js.strip().replace('\n', ' ')
    query = {'flash': attack_js}
    url = 'http://localhost:5000/?' + urlencode(query)
    print(url)


def attack_url2():
    """
    persistent xss
    if js run in such as for or while program
    then it namely persistent
    :return:
    """
    from urllib.parse import urlencode
    attack_js = """
    <script>
    var x = new XMLHTTPRequest();
    x.open('POST', 'http://localhost:5000/pay');
    x.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    x.send('account=hacker&dollars=100&memo=Theft);
    </script>
    """
    attack_js = attack_js.strip().replace('\n', ' ')
    query = {'memo': attack_js}
    url = 'http://localhost:5000/?' + urlencode(query)
    print(url)


def attack_url3():
    """
    CSRF: Cross-Site Request Forgery
    embed attack js to form
    :return:
    """


def web_socket():
    """
    can send msg on two direction at the same time
    :return:
    """


class Scraper1:
    ROW = '{:>12} {}'

    @staticmethod
    def download_page_with_requests(base):
        session = requests.session()
        # if privacy key contains in form
        # then we must need it to post
        response = session.post(urljoin(base, '/login'),
                                {'username': 'user1', 'password': 'pwd1'})
        assert response.url == urljoin(base, '/')
        return response.text

    @staticmethod
    def download_page_with_selenium(base):
        br = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        br.get(base)
        assert br.current_url == urljoin(base, '/login')
        css = br.find_element_by_css_selector
        # just like common explorer, thus if form contain privacy key,
        # it also post success
        css('input[name="username"]').send_keys('user1')
        css('input[name="password"]').send_keys('pwd1')
        css('input[name="password"]').submit()
        assert br.current_url == urljoin(base, '/')
        return br.page_source

    @staticmethod
    def scrape_with_soup(text):
        soup = bs4.BeautifulSoup(text, features='lxml')
        total = 0
        for li in soup.find_all('li', 'to'):
            dollars = int(li.get_text().split()[0].lstrip('$'))
            memo = li.find('i').get_text()
            total += dollars
            print(Scraper1.ROW.format(dollars, memo))
        print(Scraper1.ROW.format('-' * 8, '-' * 30))
        print(Scraper1.ROW.format(total, 'Total payment made'))

    @staticmethod
    def scrap_with_lxml(text):
        root = lxml.html.document_fromstring(text)
        total = 0
        for li in root.cssselect('li.to'):
            dollars = int(li.text_content().split()[0].lstrip('$'))
            memo = li.cssselect('i')[0].text_content()
            total += dollars
            print(Scraper1.ROW.format(dollars, memo))
        print(Scraper1.ROW.format('-' * 8, '-' * 30))
        print(Scraper1.ROW.format(total, 'Total payment made'))


class Scraper2:
    """
    recursive scraper
    """

    def GET(self, url):
        response = requests.get(url)
        if response.headers.get('Content-Type', '').split(';')[0] != 'text/html':
            return
        text = response.text
        try:
            html = etree.HTML(text)
        except Exception as e:
            print(' {}: {}'.format(e.__class__.__name__, e))
            return
        links = html.findall('.//a[@href]')
        for link in links:
            yield self.GET, urljoin(url, link.attrib['href'])

    @staticmethod
    def scrape(start, url_filter):
        further_work = {start}
        already_seen = {start}
        while further_work:
            call_tuple = further_work.pop()
            function, url, *etc = call_tuple
            print(function.__name__, url, *etc)
            for call_tuple in function(url, *etc):
                if call_tuple in already_seen:
                    continue
                already_seen.add(call_tuple)
                function, url, *etc = call_tuple
                if not url_filter(url):
                    continue
                further_work.add(call_tuple)


class Scraper3:
    """
    render page by explorer
    """
    def __init__(self):
        self.br = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

    def GET(self, url):
        self.br.get(url)
        time.sleep(2)
        yield from self.parse()
        if self.br.find_elements_by_xpath('.//form'):
            yield self.submit_form, url

    def parse(self):
        url = self.br.current_url
        links = self.br.find_elements_by_xpath('.//a[@href]')
        for link in links:
            yield self.GET, urljoin(url, link.get_attribute('href'))

    def submit_form(self, url):
        self.br.get(url)
        self.br.find_element_by_xpath('.//form').submit()
        yield from self.parse


def scraper1():
    parser = argparse.ArgumentParser(description='Scrape our payment site')
    parser.add_argument('url', help='the URL at which to begin')
    parser.add_argument('-l', action='store_true', help='scrape using lxml')
    parser.add_argument('-s', action='store_true', help='get with selenium')
    args = parser.parse_args()
    scraper_obj = Scraper1()
    if args.s:
        text = scraper_obj.download_page_with_selenium(args.url)
    else:
        text = scraper_obj.download_page_with_requests(args.url)
    if args.l:
        scraper_obj.scrap_with_lxml(text)
    else:
        scraper_obj.scrape_with_soup(text)


def scraper2():
    parser = argparse.ArgumentParser(description='Scrape a simple site')
    parser.add_argument('url', help='the URL at which to begin')
    args = parser.parse_args()

    start_url = args.url
    start_netloc = urlsplit(start_url).netloc
    url_filter = (lambda url: urlsplit(url).netloc == start_netloc)

    scraper_obj = Scraper2()
    scraper_obj.scrape((scraper_obj.GET, start_url), url_filter)


def scraper3():
    parser = argparse.ArgumentParser(description='Scrape a simple site')
    parser.add_argument('--url', default='https://www.baidu.com/', help='the URL at which to begin')
    args = parser.parse_args()

    scraper_obj = Scraper3()
    for function, url in scraper_obj.GET(args.url):
        print(url)


def email1():
    """
    email may added other head while sending
    through diff server
    email format:
    From:
    Reply-to:
    To:
    Cc:
    Bcc:
    Subject:
    Date: must support
    Message-Id: must support
    In-Reply-To:
    Received:
    :return:
    """

    import email.message, email.policy, email.utils

    text = """Hello, 
    This is a MIME message from this chapter.
     - Anonymous"""

    # header not case sensitive
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'recipient@example.com'
    message['From'] = 'Test Sender <sender@example.com>'
    message['Subject'] = 'Test Message, Chapter this'
    message['Date'] = email.utils.formatdate(localtime=True)
    # RFC 2392: must be globally unique
    message['Message-ID'] = email.utils.make_msgid()

    # context should end with CRLF
    message.set_content(text)
    sys.stdout.buffer.write(message.as_bytes())


def email2():
    """
    MIME(Multipurpose Internet Mail Extension) email
    :return:
    """
    parser = argparse.ArgumentParser(description='Build, print a MIME email')
    parser.add_argument('-i', action='store_true', help='Include GIF image')
    parser.add_argument('filename', nargs='*', help='Attachment filename')
    args = parser.parse_args()

    import email.message, email.policy, email.utils, mimetypes

    plain = """Hello, 
    This is a MIME message from this chapter.
     - Anonymous"""

    html = """<p>Hello,</p>
    <p>This is a <b>test message</b> from Chapter this.</p>
    <p>- <i>Anonymous</i></p>"""

    img = """<p>This is the smallest possible blue GIF:</p>
    <img src="cid:{}" height="80" width="80">"""

    blue_dot = (b'GIF89a1010\x900000\xff000,000010100\x02\x02\x0410;'
                .replace(b'0', b'\x00').replace(b'1', b'\x01'))

    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'recipient@example.com'
    message['From'] = 'Test Sender <sender@example.com>'
    message['Subject'] = 'Test Message, Chapter this'
    message['Date'] = email.utils.formatdate(localtime=True)
    message['Message-ID'] = email.utils.make_msgid()

    # every email body contain "head, CRLF, body"
    # and depart with boundary

    if not args.i:
        # email head: multipart/*: support diff version to cilent
        message.set_content(html, subtype='html')
        # make sure some client which has weak function can generate msg
        message.add_alternative(plain)
    else:
        cid = email.utils.make_msgid()
        # cid must contained in '<>'
        message.set_content(html + img.format(cid.strip('<>')), subtype='html')
        # add other src, such as msg, css, js,
        # link to html
        # msg will be a attachment
        message.add_related(blue_dot, 'image', 'gif', cid=cid, filename='blue-dot.gif')
        message.add_alternative(plain)
    for filename in args.filename:
        mime_type, encoding = mimetypes.guess_type(filename)
        if encoding or (mime_type is None):
            mime_type = 'application/octet-stream'
        main, sub = mime_type.split('/')
        if main == 'text':
            with open(filename, encoding='utf-8') as f:
                text = f.read()
            # add attachment, such as msg, pdf, excel
            # if content contain unicode, it will whole encode to base64
            # if specify cte, ASCII char still keep in email
            message.add_attachment(text, sub, filename=filename, cte='quoted-printable')
        else:
            with open(filename, 'rb') as f:
                data = f.read()
            message.add_attachment(data, main, sub, filename=filename)

    sys.stdout.buffer.write(message.as_bytes())


def display_email1():
    """
    display email from file
    :return:
    """
    parser = argparse.ArgumentParser(description='Parse and print an email')
    parser.add_argument('filename', nargs='?', help='File Containing an email')
    args = parser.parse_args()

    import email.policy

    if args.filename is None:
        binary_file = sys.stdin.buffer
    else:
        binary_file = open(args.filename, 'rb')

    policy = email.policy.SMTP
    message = email.message_from_binary_file(binary_file, policy=policy)
    for header in ['From', 'To', 'Date', 'Subject']:
        print(header + ':' + message.get(header, '(none)'))
    print()

    try:
        # if preferencelist default, some client can parse complex
        # content
        body = message.get_body(preferencelist=('html', 'plain'))
    except KeyError:
        print('<This message lack a printable text of HTML body>')
    else:
        print(body.get_content())

    for part in message.walk():
        cd = part['Content-Disposition']
        is_attachment = cd and cd.split(';')[0].lower() == 'attachment'
        if not is_attachment:
            continue
        content = part.get_content()
        # get_content_maintype: get main type, get_content_subtype: get sub type,
        print('* {} attachment named {!r}: {} object of length {}'.format(
            part.get_content_type(), part.get_filename(),
            type(content).__name__, len(content)
        ))

    if binary_file.name != '<stdin>':
        binary_file.close()


def email3():
    """
    head that contain international char
    :return:
    """
    import email.message, email.policy

    text = """
    Bạn là gì?Trương Bạn bận thế nào?
    Cai gi lam bạn bận rôn?
    Bạn làm nghề gì?
    Bạn đã có một giấc mơ?
    """

    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'Νικόλαος<recipient@example.com>'
    message['From'] = 'Eardstapa <sender@example.com>'
    message['Subject'] = 'Four line from The Wanderer'
    message['Date'] = email.utils.formatdate(localtime=True)
    message.set_content(text, cte='quoted-printable')
    sys.stdout.buffer.write(message.as_bytes())


def display_email2():
    """
    walk every part of an email
    :return:
    """
    parser = argparse.ArgumentParser(description='Parse and print an email')
    parser.add_argument('filename', nargs='?', help='File Containing an email')
    args = parser.parse_args()

    import email.policy

    if args.filename is None:
        binary_file = sys.stdin.buffer
    else:
        binary_file = open(args.filename, 'rb')

    def walk(part, prefix=''):
        yield prefix, part
        # iter_parts: get sub part
        for i, subpart in enumerate(part.iter_parts()):
            yield from walk(subpart, prefix + '.{}'.format(i))

    policy = email.policy.SMTP
    message = email.message_from_binary_file(binary_file, policy=policy)
    # if you have known the part info, can through get_payload to get part
    specify_part = message.get_payload(0).get_payload(0).get_payload(1)
    print('specify-----\n', specify_part)
    for prefix, part in walk(message):
        line = '{} type={}'.format(prefix, part.get_content_type())
        # if not multipart, so can get its content
        if not part.is_multipart():
            content = part.get_content()
            line += ' {} len={}'.format(type(content).__name__, len(content))
            cd = part['Content-Disposition']
            is_attachment = cd and cd.split(';')[0].lower() == 'attachment'
            if is_attachment:
                line += ' attachment'
            filename = part.get_filename()
            if filename is not None:
                line += ' filename = {!r}'.format(filename)
            print(line)


def email_parse_date():
    """
    parse_date
    :return:
    """
    import email.utils
    # if date formation not correct, it return None
    d1 = email.utils.parsedate('Tue, 25 Error 2014 17:14:01 -0400')
    print(d1)
    d2 = email.utils.parsedate_tz('Tue, 25 Mar 2014 17:14:01 -0400')
    print(d2)
    d3 = email.utils.parsedate_to_datetime('Tue, 25 Mar 2014 17:14:01 -0400')
    print(d3)


def smtp_mail1():
    """
    send mail use smtp
    smtp no use Cc and Bcc
    normally no need auth between servers
    a simple send process: client->MTA(mail transfer agent)->
    ->server1(DNS found)->server2->..->rubbish filter server(if exist)
    ->final sever(save mail)
    every server have a Received header that added self above
    once msg send to server, client think that it send successful
    :return:
    """

    import smtplib

    # To: this is unrelated to real recipient
    message_template = """
    To: {}
    From: {}
    Subject: Test Message from test
    Hello,
    This is a test message sent to you from test program
    """
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print('usage: {} server fromaddr toaddr [toaddr...]'.format(name))
        sys.exit(2)
    server, fromaddr, toaddr = sys.argv[1], sys.argv[2], sys.argv[3:]
    message = message_template.format(', '.join(toaddr), fromaddr)
    connection = smtplib.SMTP(server)
    # once one of recipient receive faild, it will raise exception
    connection.sendmail(fromaddr, toaddr,  message)
    connection.quit()

    s = '' if len(toaddr) == 1 else 's'
    print('Message sent to {} recipients{}'.format(len(toaddr), s))


def smtp_mail2():
    """
    deal exception
    :return:
    """

    import smtplib

    message_template = """
    To: {}
    From: {}
    Subject: Test Message from test
    Hello,
    This is a test message sent to you from test program
    """
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print('usage: {} server fromaddr toaddr [toaddr...]'.format(name))
        sys.exit(2)
    server, user, pwd, fromaddr, toaddr = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
    message = message_template.format(', '.join(toaddr), fromaddr)

    try:
        connection = smtplib.SMTP(server)
        # show the session detail msg
        connection.set_debuglevel(1)
        # some mail server need auth
        connection.login(user, pwd)
        connection.sendmail(fromaddr, toaddr,  message)
    except (socket.gaierror, socket.error, socket.herror,
            smtplib.SMTPException) as e:
        print("Your message may not have been sent")
        print(e)
        sys.exit(1)
    else:
        s = '' if len(toaddr) == 1 else 's'
        print('Message sent to {} recipients{}'.format(len(toaddr), s))
        connection.quit()


def smtp_mail3():
    """
    use esmtp(extend smtp) to get more info
    such max msg size
    diff server support diff esmtp function
    :return:
    """

    import smtplib

    def report_on_message_size(connection, fromaddr, toaddr, message):
        # ehlo support more feature than helo
        code = connection.ehlo()[0]
        # success retcode between 200 and 299
        use_esmtp = (200 <= code <= 299)
        if not use_esmtp:
            # some client and server only support helo
            code = connection.helo()[0]
            if not (200 <= code <= 299):
                print('Remote server refused HELO; code:', code)
                sys.exit(1)
        if use_esmtp and connection.has_extn('size'):
            max_msg_size = connection.esmtp_features['size']
            print('Maximum message size is ', max_msg_size)
            if len(message) > int(max_msg_size):
                print('Message to large; aborting.')
                sys.exit(1)
        connection.sendmail(fromaddr, toaddr, message)

    message_template = """
    To: {}
    From: {}
    Subject: Test Message from test
    Hello,
    This is a test message sent to you from test program
    """
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print('usage: {} server fromaddr toaddr [toaddr...]'.format(name))
        sys.exit(2)
    server, user, pwd, fromaddr, toaddr = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
    message = message_template.format(', '.join(toaddr), fromaddr)

    try:
        connection = smtplib.SMTP(server)
        connection.login(user, pwd)
        report_on_message_size(connection, fromaddr, toaddr, message)
    except (socket.gaierror, socket.error, socket.herror,
            smtplib.SMTPException) as e:
        print("Your message may not have been sent")
        print(e)
        sys.exit(1)
    else:
        s = '' if len(toaddr) == 1 else 's'
        print('Message sent to {} recipients{}'.format(len(toaddr), s))
        connection.quit()


def smtp_mail4():
    """
    use tls to connect
    :return:
    """

    import smtplib

    def send_message_securely(connection, user, pwd, fromaddr, toaddr, message):
        code = connection.ehlo()[0]
        use_esmtp = (200 <= code <= 299)
        if not use_esmtp:
            code = connection.helo()[0]
            if not (200 <= code <= 299):
                print('Remote server refused HELO; code:', code)
                sys.exit(1)
        # if sever not support esmtp, it will not support tls
        if use_esmtp and connection.has_extn('starttls'):
            print('Negotiating TLS...')
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.set_default_verify_paths()
            context.verify_mode = ssl.CERT_REQUIRED
            purpose = ssl.Purpose.SERVER_AUTH
            context.load_default_certs(purpose=purpose)
            connection.starttls(context=context)
            # if server has auth, should call ehlo again
            code = connection.ehlo()[0]
            if not (200 <= code <= 299):
                print("Couldn't EHLO after STARTTLS")
                sys.exit(5)
            print("Using TLS connection")
        else:
            print("Server does not support TLS; using normal connection.")

        # should first build tls, then use it to send auth info
        # most server not support auth, so should make sure that
        # it support auth
        if connection.has_extn('auth'):
            connection.login(user, pwd)
        connection.sendmail(fromaddr, toaddr, message)

    message_template = """
    To: {}
    From: {}
    Subject: Test Message from test
    Hello,
    This is a test message sent to you from test program
    """
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print('usage: {} server fromaddr toaddr [toaddr...]'.format(name))
        sys.exit(2)
    server, user, pwd, fromaddr, toaddr = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
    message = message_template.format(', '.join(toaddr), fromaddr)

    try:
        connection = smtplib.SMTP(server)
        # connection.login(user, pwd)
        send_message_securely(connection, user, pwd, fromaddr, toaddr, message)
    except (socket.gaierror, socket.error, socket.herror,
            smtplib.SMTPException) as e:
        print("Your message may not have been sent")
        print(e)
        sys.exit(1)
    else:
        s = '' if len(toaddr) == 1 else 's'
        print('Message sent to {} recipients{}'.format(len(toaddr), s))
        connection.quit()


def pop_mail1():
    """
    pop(post office protocol)
    use it to get email info from server, such as download
    some pop sever will modify mail flag, such as to unread
    once connect to server or download mail, or lock mailbox during
    connection, diff server have diff behavior
    only support access one dir
    :return:
    """
    import getpass, poplib

    if len(sys.argv) != 3:
        print("usage: %s hostname username" % sys.argv[0])
        sys.exit(2)
    hostname, username = sys.argv[1:]
    passwd = getpass.getpass()
    p = poplib.POP3_SSL(host=hostname)
    try:
        print("Attempting APOP authentication...")
        # apop will encrypt passwd
        p.apop(username, passwd)
    # some server not support apop
    except poplib.error_proto:
        print("Attempting standard authentication...")
        try:
            p.user(username)
            p.pass_(passwd)
        except poplib.error_proto as e:
            print('Login failed:', e)
            sys.exit(1)
        else:
            status = p.stat()
            print("You have %d message totalling %d bytes" % status)
        finally:
            # some server will lock mailbox during connection
            # so should close connection at last
            p.quit()


def pop_mail2():
    """
    list every mail info
    :return:
    """
    import getpass, poplib

    if len(sys.argv) != 3:
        print("usage: %s hostname username" % sys.argv[0])
        sys.exit(2)
    hostname, username = sys.argv[1:]
    passwd = getpass.getpass()
    p = poplib.POP3_SSL(host=hostname)
    try:
        print("Attempting APOP authentication...")
        p.apop(username, passwd)
    except poplib.error_proto:
        print("Attempting standard authentication...")
        try:
            p.user(username)
            p.pass_(passwd)
        except poplib.error_proto as e:
            print('Login failed:', e)
            sys.exit(1)
        else:
            response, listings, octet_count = p.list()
            if not listings:
                print("No message")
            for listing in listings:
                # msg_id in diff connection may diff
                number, size = listing.decode('utf-8').split()
                print("Message %s has %s bytes" % (number, size))
        finally:
            p.quit()


def pop_mail3():
    """
    download and delete mail
    :return:
    """
    import getpass, poplib
    import email

    decode = 'ascii'

    def visit_all_listings(p):
        response, listings, octets = p.list()
        for listing in listings:
            visit_listing(p, listing)

    def visit_listing(p, listing):
        number, size = listing.decode(decode).split()
        print('Message', number, '(size is ', size, 'bytes):')
        print()
        # return specify line if mail, not set seen flag
        response, lines, octets = p.top(number, 0)
        # every msg's row will construct to a list to return
        document = '\n'.join(line.decode(decode) for line in lines)
        message = email.message_from_string(document)
        for header in 'From', 'To', 'Subject', 'Date':
            if header in message:
                print(header + ":" + message[header])
        print()
        print('Read this message [ny]?')
        answer = input()
        if answer.lower().startswith('y'):
            # most server will set seen flag
            response, lines, octets = p.retr(number)
            document = '\n'.join(line.decode(decode) for line in lines)
            message = email.message_from_string(document)
            print('-' * 72)
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    print(part.get_payload())
                    print('-' * 72)
        print()
        print("Delete this message [ny]?")
        answer = input()
        if answer.lower().startswith('y'):
            # delete mail from server
            p.dele(number)
            print('Deleted.')

    if len(sys.argv) != 3:
        print("usage: %s hostname username" % sys.argv[0])
        sys.exit(2)
    hostname, username = sys.argv[1:]
    passwd = getpass.getpass()
    p = poplib.POP3_SSL(host=hostname)
    try:
        print("Attempting APOP authentication...")
        p.apop(username, passwd)
    except poplib.error_proto:
        print("Attempting standard authentication...")
        try:
            p.user(username)
            p.pass_(passwd)
        except poplib.error_proto as e:
            print('Login failed:', e)
            sys.exit(1)
        else:
            visit_all_listings(p)
        finally:
            p.quit()


def imap_mail1():
    """
    imap(internet message access protocal)
    compare with pop:
    1. classify mail into diff dir
    2. flag msg such have read, have deleted
    3. search info in server
    4. upload local info to remote dir
    5. unique msg id to ensure sync between local and server
    6. share dir with other, flag dir to have read
    7. some server show none mail src in dir, such as Usenet news group
    8. download part of msg with choice, such as some attachment
    :return:
    """

    import getpass, imaplib

    if len(sys.argv) != 3:
        print("usage: %s hostname username" % sys.argv[0])
        sys.exit(2)

    hostname, username = sys.argv[1:]
    # IMAP4rev1: most popular version
    m = imaplib.IMAP4_SSL(host=hostname)
    m.login(username, getpass.getpass())
    try:
        # show supported imap feature
        print("Capabilities:", m.capabilities)
        print("Listing mailboxes")
        status, data = m.list()
        print("Status:", repr(status))
        print("Data:")
        for datum in data:
            print(datum.decode('GB2312'))
    finally:
        m.logout()


def imap_mail2():
    """
    user third part package(imapclient) to
    fetch mail info
    :return:
    """

    import getpass
    from imapclient import IMAPClient

    if len(sys.argv) != 3:
        print("usage: %s hostname username" % sys.argv[0])
        sys.exit(2)

    hostname, username = sys.argv[1:]
    # msg uid not the same, but tmp msg id may be same
    # between diff session
    c = IMAPClient(host=hostname, ssl=True, use_uid=True)
    try:
        c.login(username, getpass.getpass())
    except c.Error as e:
        print("Could not log in:", e)
    else:
        print("Capabilities:", c.capabilities())
        print("Listing mailboxes")
        # no need judge status code, if problem happen it
        # will raise exception
        data = c.list_folders()
        # folder name return on str formation
        # flag: NoSelect: no contain any msg
        # HasNoChildren: no sub folder
        # HasChildren: contain sub folder
        for flags, delimiter, folder_name in data:
            print("%-30s%s %s" % (' '.join(map(repr, flags)), delimiter, folder_name))
        # if folder has been selected, later operation such as download
        # only affect in this folder, surpport rw control
        # c.select_folder(readonly=True)
    finally:
        c.logout()


def imap_mail3():
    """
    display digest of folder
    :return:
    """

    import getpass
    from imapclient import IMAPClient

    if len(sys.argv) != 4:
        print("usage: %s hostname username" % sys.argv[0])
        sys.exit(2)

    hostname, username, foldername = sys.argv[1:]
    c = IMAPClient(host=hostname, ssl=True)
    try:
        c.login(username, getpass.getpass())
    except c.Error as e:
        print("Could not log in:", e)
    else:
        select_dict = c.select_folder(folder=foldername, readonly=True)
        # EXISTS(must rtn): total msg,
        # FLAGS(must rtn): flag of can set in msg
        # RECENTS(must rtn): msg appeal after select_folder last
        # PERMANENTFLAGS: self define flag of can set in msg
        # UIDNEXT: next msg uid that server guest
        # UIDVALIDITY: confirm uid of msg if change, if diff between
        # new and last, it prove that uid reallocate to the msg, last one
        # is invalid
        # UNSEEN: first unread msg in the folder
        for k, v in sorted(select_dict.items()):
            print('%s:  %r' % (k, v))
    finally:
        c.logout()


def imap_mail4():
    """
    retrieving the whole mailbox
    :return:
    """

    import getpass
    import email
    from imapclient import IMAPClient

    def print_summary(c, foldername):
        c.select_folder(foldername, readonly=True)
        # msg index: exemple: 2,4:6,20: msg 2, msg4 to msg6, msg20 to msg of
        # id gt 20
        # PEEK: only query msg, don't set seen flag to msg
        msgdict = c.fetch('1:*', ['BODY.PEEK[]'])
        for message_id, message in list(msgdict.items()):
            # also can save mail in file
            # with open(fr'E:\file\mailbox\{message_id}.txt', 'w', encoding='gbk') as f:
            #     f.write(message[b'BODY[]'].decode())
            # BODY[] mean whole msg
            e = email.message_from_string(message[b'BODY[]'].decode())
            print(message_id, e['From'])
            pay_load = e.get_payload()
            if isinstance(pay_load, list):
                part_content_types = [part.get_content_type() for part in pay_load]
                print(' Parts:', ' '.join(part_content_types))
            else:
                print(' ', ' '.join(pay_load[:60].split()), '...')

    if len(sys.argv) != 4:
        print("usage: %s hostname username" % sys.argv[0])
        sys.exit(2)

    hostname, username, foldername = sys.argv[1:]
    c = IMAPClient(host=hostname, ssl=True)
    try:
        c.login(username, getpass.getpass())
    except c.Error as e:
        print("Could not log in:", e)
    else:
        print_summary(c, foldername)
    finally:
        c.logout()


def imap_mail5(*args):
    """
    browse folder, messages, message parts
    :return:
    """

    import getpass
    from imapclient import IMAPClient
    import email.header

    banner = '-' * 72

    def operate_folder(c):
        c.create_folder('MyFolder')
        c.delete_folder('MyFolder2')

        c.select_folder('MyFolder3')
        c.copy([1, 2], 'MyFolder4')
        
        msg = '\r\n'.join('one\rtwo\r\three'.splitlines())
        c.append('MyFolder5', msg)

    def decode_header(header):
        decoded_header = email.header.decode_header(header)
        decoded_header = ''.join([part.decode(encoding) if encoding else
                                  (part.decode('utf-8', 'replace') if not isinstance(part, str) else part)
                                  for part, encoding in decoded_header])
        return decoded_header

    # other api: asynchronous api

    def explore_account(c):
        while True:
            print()
            folder_flags = {}
            data = c.list_folders()
            for flags, delimiter, name in data:
                folder_flags[name] = flags
            for name in sorted(folder_flags.keys()):
                flags = list(map(bytes.decode, folder_flags[name]))
                print('%-30s %s' % (name, ' '.join(flags)))
            print()

            reply = input('Type a folder name, or "q" to quit:').strip()
            if reply.lower() == 'q':
                break
            if reply in folder_flags:
                explore_folder(c, reply)
            else:
                print('Error: no folder named', repr(reply))

    def explore_folder(c, name):
        while True:
            c.select_folder(name, readonly=True)

            reply = input('Folder %s - type a search text:'
                          % name).strip()
            if reply:
                # search text example:
                # 1. SINCE 13-Jan-2020 TEXT Apple
                # 2. OR (SINCE 13-Jan-2020) (TEXT Apple)
                # 3. UID
                # 4. SMALLER m: msg less than 100 octets in length
                # 5. DRAFT: have the flag \Draft
                # 6. CC string FROM string BODY string
                # 7. BEFORE 01-Jan-2020: actual date that receive
                # 8. SENTBEFORE 01-Jan-2020: actual date that sent
                # ...
                try:
                    print(c.search(reply.encode()))
                except Exception as e:
                    print('Search error: ', str(e))

            msgdict = c.fetch('1:*', ['BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)]',
                                      'FLAGS', 'INTERNALDATE', 'RFC822.SIZE'])
            print()
            for uid in sorted(msgdict):
                items = msgdict[uid]
                flags = list(map(bytes.decode, items[b'FLAGS']))
                print('%6d %20s %6d bytes %s' % (
                    uid, items[b'INTERNALDATE'], items[b'RFC822.SIZE'],
                    ' '.join(flags)))
                for i in items[b'BODY[HEADER.FIELDS (FROM SUBJECT)]'].splitlines():
                    decoded_header = decode_header(i.strip().decode())
                    print(' ' * 6, decoded_header)
            reply = input('Folder %s - type a message uid, or "q" to quit:'
                          % name).strip()
            if reply.lower() == 'q':
                break
            try:
                reply = int(reply)
            except ValueError:
                print('Please  type a integer or "q" to quit:')
            else:
                if reply in msgdict:
                    explore_message(c, reply)

    def explore_message(c, uid):
        # fetch specify part
        msgdict = c.fetch(uid, ['BODYSTRUCTURE', 'FLAGS'])

        # set flag on msg
        # c.get_flags(uid)
        # c.remove_flags(uid, ['\\Seen'])
        # c.add_flags(uid, ['\\Answered'])
        # c.set_flags(uid, ['\\Seen', '\\Answered'])

        # first: mark flag to \Delete; second: delete actually
        # c.delete_messages([uid])
        # c.expunge()

        while True:
            print()
            print('Flags:', end=' ')
            # common flags: Answered, Draft, Flagged, Recent, Seen
            flag_list = msgdict[uid][b'FLAGS']
            if flag_list:
                flags = list(map(bytes.decode, flag_list))
                print(' '.join(flags))
            else:
                print('none')

            print('Structure:')
            display_structure(msgdict[uid][b'BODYSTRUCTURE'])
            print()
            reply = input('Message %s - type a part name, or "q" to quit:'
                          % uid).strip()
            if reply.lower() == 'q':
                break
            key = 'BODY[%s]' % reply
            # truncate msg
            # key2 = 'BODY[%s]<100>' % reply
            try:
                msgdict2 = c.fetch(uid, key)
            except c._imap.error:
                print('Error - cannot fetch section' % reply)
            else:
                content = msgdict2[uid][key.encode()]
                if content:
                    print(banner)
                    print(content.strip())
                    print(banner)
                else:
                    print('No such section')

    def display_structure(structure, parentparts=[]):
        if parentparts:
            name = '.'.join(parentparts)
        else:
            print(" HEADER")
            name = 'TEXT'

        is_multipart = isinstance(structure[0], (list, tuple))

        if not is_multipart:
            stru = tuple(map(bytes.decode, structure[:2]))
            parttype = ('%s/%s' % stru).lower()
            print(' %-9s' % name, parttype, end=' ')
            if structure[6]:
                print('size = %s' % structure[6], end=' ')
            if structure[9]:
                print('disposition = %s' % structure[9][0],
                      ' '.join('{}={}'.format(k, v) for k, v in structure[9][1:]),
                      end=' ')
            print()
            return

        parttype = 'multipart/%s' % structure[1].lower().decode()
        print(' %-9s' % name, parttype, end=' ')
        print()
        subparts = structure[0]
        for i in range(len(subparts)):
            display_structure(subparts[i], parentparts + [str(i+1)])

    if len(sys.argv) != 3:
        print("usage: %s hostname username" % sys.argv[0])
        if not args:
            sys.exit(2)
        hostname, username, passwd = args[:3]
    else:
        hostname, username = sys.argv[1:]
        passwd = getpass.getpass()

    c = IMAPClient(host=hostname, ssl=True)
    try:
        c.login(username, passwd)
    except c.Error as e:
        print("Could not log in:", e)
    else:
        explore_account(c)
    finally:
        c.logout()


def shell1():
    """
    subprocess can call os command
    """
    import subprocess

    # special character only affect in shell,
    # no associate with operate system
    args = ['echo', 'Sometimes', '*', 'is just an asterisk']
    # \0 regarded as special char by os, mean the end of args
    # will raise exception
    args2 = ['echo', 'Sentences can end\0 abruptly']
    subprocess.call(args2)


def shell2():
    import subprocess

    # not support special char
    while True:
        args = input('] ').strip().split()
        if not args:
            pass
        elif args == ['exit']:
            break
        elif args[0] == 'show':
            print('Arguments: ', args[1:])
        else:
            try:
                subprocess.call(args)
            except Exception as e:
                print(e)


def shell3():
    # not like subprocess, system will call shell like bash
    # so if this call in linux, it will echo all file in current
    # dir
    os.system('echo *')


def shell4():
    from subprocess import list2cmdline
    from pipes import quote

    # escape special char
    print(quote('file "single quoted" inside!'))

    # if ssh to window, args will be a text to new process
    # so use this method convert list to text
    args = ['rename', 'first "second".xls', 'first-second.xls']
    print(list2cmdline(args))


def shell5():
    """
    :return:
    """
    # interactive app only show prompt in tty input
    """
    cat | bash
    echo Here we are inside of bash, with no prompt
    # python read all script to buffer, then begin to run
    python
    # will not response info
    # only show response with the end of cat(ctrl+D)
    print('Python has no printed a prompt, either.')
    import sys
    print('Is this a terminal?', sys.stdin.isatty())
    """

    """
    # out formation adj to tty side
    ls 
    # but out to pipe, out formation will any width
    ls | cat
    """

    """
    # no show prompt
    ssh -T host port
    """

    """
    # close std input, every char will read by app
    # immediately
    stty -icanon
    # ctrl + s stop output, ctrl + q continute output
    # close the feature above
    stty -ixon -ixoff
    # disable or enable set feature above
    stty raw
    stty cooked
    """


def telnet1():
    """
    telnet only build a channel to show the
    transfer info like password, it don't know
    any auth, so it no safe
    :return:
    """
    import getpass, telnetlib

    parser = argparse.ArgumentParser(description='Use telnet to login')
    parser.add_argument('hostname', help='Remote host to telnet to')
    parser.add_argument('port', help='Remote port to telnet to')
    parser.add_argument('username', help='Remote username')
    args = parser.parse_args()
    password = getpass.getpass('Password: ')

    t = telnetlib.Telnet(host=args.hostname, port=args.port)
    t.set_debuglevel(1)
    t.read_until(b'login:')
    t.write(args.username.encode('utf-8'))
    t.write(b'\r')

    # first letter must be 'P' or 'p'
    t.read_until(b'password:')
    t.write(password.encode('utf-8'))
    t.write(b'\r')

    # index of match in the regex list, regex match obj, match text
    n, match, previous_text = t.expect([br'Login incorrect', br'\$'], 10)

    if n == 0:
        print('Username and password failed - giving up')
    else:
        t.write(b'exec uptime\r')
        # read util socket closes
        print(t.read_all().decode('utf-8'))

    
def telnet2():
    """
    :return:
    """
    import getpass
    from telnetlib import Telnet, IAC, DO, DONT, WILL, WONT, SB, SE, TTYPE

    def process_option(tsocket, command, option):
        # should suport response for every type
        # otherwise server's wait will interrupt session
        if command == DO or command == TTYPE:
            tsocket.sendall(IAC + WILL + TTYPE)
            print('Sendging terminal type "mypython"')
            tsocket.sendall(IAC + SB + TTYPE + b'\0' + b'mypython' + IAC + SE)
        elif command in (DO, DONT):
            print('will not', ord(option))
            tsocket.sendall(IAC + WONT + option)
        elif command in (WILL, WONT):
            print('Do not', ord(option))
            tsocket.sendall(IAC + DONT + option)

    parser = argparse.ArgumentParser(description='Use telnet to login')
    parser.add_argument('hostname', help='Remote host to telnet to')
    parser.add_argument('port', help='Remote port to telnet to')
    parser.add_argument('username', help='Remote username')
    args = parser.parse_args()
    password = getpass.getpass('Password: ')

    t = Telnet(host=args.hostname, port=args.port)
    t.set_debuglevel(1)
    t.set_option_negotiation_callback(process_option)
    t.read_until(b'login:')
    t.write(args.username.encode('utf-8'))
    t.write(b'\r')

    t.read_until(b'assword:')
    t.write(password.encode('utf-8'))
    t.write(b'\r')

    n, match, previous_text = t.expect([br'Login incorrect', br'\$'], 10)

    if n == 0:
        print('Username and password failed - giving up')
    else:
        t.write(b'exec uptime\r')
        # read util socket closes
        print(t.read_all().decode('utf-8'))


def ssh1():
    """
    secure shell
    only one connection, laster session
    reuse this connection,
    ssh support port forward
    """
    import paramiko, getpass

    # if need some self strategy to deal with host key auth
    # can inherit this class to achive
    class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
        def missing_host_key(self, client, hostname, key):
            return
    
    parser = argparse.ArgumentParser(description='Connect over SSH')
    parser.add_argument('hostname', help='Remote host to telnet to')
    parser.add_argument('username', help='Remote username')
    parser.add_argument('port', help='Remote port to telnet to')
    args = parser.parse_args()

    password = getpass.getpass()

    client = paramiko.SSHClient()
    # if not support this method and connect to unknow host,
    # ssh will raise exception, some strategy will add remote host keys
    # to local, next connection will not raise auth exception
    client.set_missing_host_key_policy(AllowAnythingPolicy)
    client.connect(args.hostname, username=args.username, port=args.port, password=password)
    
    # start a session for shell
    channel = client.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')

    stdin.write(b'echo Hello, world\rexit\r')
    # output result like normal tty, include show of prompt
    output = stdout.read()
    client.close()

    sys.stdout.buffer.write(output)


def ssh2():
    import paramiko, getpass

    class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
        def missing_host_key(self, client, hostname, key):
            return
    
    parser = argparse.ArgumentParser(description='Connect over SSH')
    parser.add_argument('hostname', help='Remote host to telnet to')
    parser.add_argument('username', help='Remote username')
    parser.add_argument('port', help='Remote port to telnet to')
    args = parser.parse_args()

    password = getpass.getpass()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(AllowAnythingPolicy)
    client.connect(args.hostname, username=args.username, port=args.port, password=password)

    # seperate every command, and invoke_shell can't do this
    for command in 'echo "Hello, world!"', 'uname', 'uptime':
        # exec_command only accept whole text command, not like 
        # subprocess, other use like subprocess
        # build channel for every_command
        stdin, stdout, stderr = client.exec_command(command)
        stdin.close()
        print(repr(stdout.read()))
        stdout.close()
        stderr.close()
    
    client.close()


def ssh3():
    """
    run multiple commands simultaneously in diff channels
    """
    import paramiko, getpass
    import threading

    class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
        def missing_host_key(self, client, hostname, key):
            return
    
    parser = argparse.ArgumentParser(description='Connect over SSH')
    parser.add_argument('hostname', help='Remote host to telnet to')
    parser.add_argument('username', help='Remote username')
    parser.add_argument('port', help='Remote port to telnet to')
    args = parser.parse_args()

    password = getpass.getpass()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(AllowAnythingPolicy)
    client.connect(args.hostname, username=args.username, port=args.port, password=password)

    def read_until_EOF(fileobj):
        s = fileobj.readline()
        while s:
            print(s.strip())
            s = fileobj.readline()

    # two channel not effect each other
    ioe1 = client.exec_command('echo One;sleep 2;echo Two;sleep 1;echo Three')
    ioe2 = client.exec_command('echo A;sleep 1;echo B;sleep 2;echo C')
    thread1 = threading.Thread(target=read_until_EOF, args=(ioe1[1], ))
    thread2 = threading.Thread(target=read_until_EOF, args=(ioe2[1], ))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    client.close()


def ssh4():
    """
    sftp is a sub protocol of ssh
    every open file has its channel
    if filename contain specify char,
    sftp will regards it as a part of filename
    """
    import paramiko, getpass
    import functools

    class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
        def missing_host_key(self, client, hostname, key):
            return
    
    parser = argparse.ArgumentParser(description='Connect over SSH')
    parser.add_argument('hostname', help='Remote host to telnet to')
    parser.add_argument('username', help='Remote username')
    parser.add_argument('port', help='Remote port to telnet to')
    parser.add_argument('filenames', nargs='+', help='Remote port to telnet to')
    args = parser.parse_args()

    password = getpass.getpass()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(AllowAnythingPolicy)
    client.connect(args.hostname, username=args.username, port=args.port, password=password)

    def print_status(filename, bytes_so_far, bytes_total):
        percent = 100. * bytes_so_far / bytes_total
        print('Transfer of %r is at %d/%d bytes (%.1f%%)' % (
            filename, bytes_so_far, bytes_total, percent
        ))

    sftp = client.open_sftp()
    for filename in args.filenames:
        if filename.endswith('.copy'):
            continue
        callback = functools.partial(print_status, filename)
        sftp.get(filename, filename + '.copy', callback=callback)
    
    client.close()


def ftp1():
    """
    build two tcp
    1. control channel
    2. data channel
    process:
    1. client connect to server
    2. auth
    3. change dir of server
    4. client listen on port for data transfer
    and tell this to server to connect, but most
     situation, this process is reverse
    5. transfer file

    more secure replacement: sftp, http
    """

    from ftplib import FTP
    import getpass

    parser = argparse.ArgumentParser(description='FTP')
    parser.add_argument('host', help='host')
    parser.add_argument('user', help='user')
    args = parser.parse_args()

    passwd = getpass.getpass()

    ftp = FTP(args.host)
    print("Welcome:", ftp.getwelcome())
    ftp.login(user=args.user, passwd=passwd)
    print('Current working directory:', ftp.pwd())
    ftp.quit()


def ftp2():
    """
    download text file
    """

    from ftplib import FTP
    import getpass

    parser = argparse.ArgumentParser(description='FTP')
    parser.add_argument('host', help='host')
    parser.add_argument('user', help='user')
    args = parser.parse_args()

    passwd = getpass.getpass()

    if os.path.exists('README'):
        raise IOError('refusing to overwrite your README file')

    ftp = FTP(args.host)
    print("Welcome:", ftp.getwelcome())
    ftp.login(user=args.user, passwd=passwd)
    ftp.cwd(r'\file')

    with open('README', 'w') as f:
        def writeline(data):
            f.write(data)
            # transfer not contain line sep
            # so add it by self
            f.write(os.linesep)
        # param1: command filename
        # param2: callback
        # ascii mode: transfer one line per
        ftp.retrlines('RETR README', writeline)

    ftp.quit()


def ftp3():
    """
    download binary file
    """

    from ftplib import FTP
    import getpass

    parser = argparse.ArgumentParser(description='FTP')
    parser.add_argument('host', help='host')
    parser.add_argument('user', help='user')
    args = parser.parse_args()

    passwd = getpass.getpass()

    if os.path.exists('patch.zip'):
        raise IOError('refusing to overwrite your patch.zip file')

    ftp = FTP(args.host)
    print("Welcome:", ftp.getwelcome())
    ftp.login(user=args.user, passwd=passwd)
    ftp.cwd(r'\file')

    with open('patch.zip', 'wb') as f:
        ftp.retrbinary('RETR patch.zip', f.write)

    ftp.quit()


def ftp4():
    """
    download binary file
    more detail transfer info
    """

    from ftplib import FTP
    import getpass

    parser = argparse.ArgumentParser(description='FTP')
    parser.add_argument('host', help='host')
    parser.add_argument('user', help='user')
    args = parser.parse_args()

    passwd = getpass.getpass()

    if os.path.exists('patch.zip'):
        raise IOError('refusing to overwrite your patch.zip file')

    ftp = FTP(args.host)
    print("Welcome:", ftp.getwelcome())
    ftp.login(user=args.user, passwd=passwd)
    ftp.cwd(r'\file')
    # set image transfer mode
    # no return
    ftp.voidcmd('TYPE I')

    # retrbinary call voidcmd, but this method wont
    # size may be not correct
    socket, size = ftp.ntransfercmd('RETR patch.zip')
    nbytes = 0

    f = open('patch.zip', 'wb')

    while True:
        data = socket.recv(2048)
        if not data:
            break
        f.write(data)
        nbytes += len(data)
        # \r alway move cursor to left-right
        print('\rReceived ', nbytes, end=' ')
        if size:
            print('of %d total bytes (%.1f%%)' % (size, 
            100 * nbytes / float(size)), end=' ')
        else:
            print('bytes', end=' ')
        sys.stdout.flush()

    print()
    f.close()
    socket.close()
    # read resp from server, should call this method
    # otherwise server may wait too long
    ftp.voidresp()
    ftp.quit()


def ftp5():
    """
    upload binary file
    """

    from ftplib import FTP
    import getpass

    parser = argparse.ArgumentParser(description='FTP')
    parser.add_argument('host', help='host')
    parser.add_argument('user', help='user')
    parser.add_argument('localfile', help='localfile')
    parser.add_argument('remotedir', help='remotedir')
    args = parser.parse_args()

    prompt = 'Enter the password for {} on {}:'.format(args.user, args.host)
    passwd = getpass.getpass(prompt)

    ftp = FTP(args.host)
    print("Welcome:", ftp.getwelcome())
    ftp.login(user=args.user, passwd=passwd)
    ftp.cwd(args.remotedir)

    with open(args.localfile, 'rb') as f:
        ftp.storbinary('STOR % s' % os.path.basename(args.localfile), f)

    ftp.quit()


def ftp6():
    """
    upload binary file
    more detail transfer info
    """

    from ftplib import FTP
    import getpass

    BLOCKSIZE = 8192

    parser = argparse.ArgumentParser(description='FTP')
    parser.add_argument('host', help='host')
    parser.add_argument('user', help='user')
    parser.add_argument('localfile', help='localfile')
    parser.add_argument('remotedir', help='remotedir')
    args = parser.parse_args()

    passwd = getpass.getpass()

    ftp = FTP(args.host)
    print("Welcome:", ftp.getwelcome())
    ftp.login(user=args.user, passwd=passwd)
    ftp.cwd(args.remotedir)
    ftp.voidcmd('TYPE I')

    datasock, esize = ftp.ntransfercmd('STOR %s' % os.path.basename(args.localfile))
    size = os.stat(args.localfile)[6]
    nbytes = 0

    f = open(args.localfile, 'rb')

    while True:
        data = f.read(BLOCKSIZE)
        if not data:
            break
        datasock.sendall(data)
        nbytes += len(data)
        print('\r Sent', nbytes, 'of', size, 'bytes',
        '(%.1f%%)\r' % (100 * nbytes / float(size)), end=' ')
        sys.stdout.flush()

    print()
    f.close()
    datasock.close()
    ftp.voidresp()
    ftp.quit()


def ftp7():
    """
    show remote file and dir
    """

    from ftplib import FTP
    import getpass

    parser = argparse.ArgumentParser(description='FTP')
    parser.add_argument('host', help='host')
    parser.add_argument('user', help='user')
    parser.add_argument('remotedir', help='remotedir')
    args = parser.parse_args()

    passwd = getpass.getpass()

    ftp = FTP(args.host)
    print("Welcome:", ftp.getwelcome())
    ftp.login(user=args.user, passwd=passwd)
    ftp.cwd(args.remotedir)
    entries = ftp.nlst()
    ftp.quit()

    print(len(entries), 'entries:')

    for entry in sorted(entries):
        print(entry)


def ftp8():
    """
    show remote file and dir
    more detail info
    """

    from ftplib import FTP
    import getpass

    parser = argparse.ArgumentParser(description='FTP')
    parser.add_argument('host', help='host')
    parser.add_argument('user', help='user')
    parser.add_argument('remotedir', help='remotedir')
    args = parser.parse_args()

    passwd = getpass.getpass()

    ftp = FTP(args.host)
    print("Welcome:", ftp.getwelcome())
    ftp.login(user=args.user, passwd=passwd)
    ftp.cwd(args.remotedir)
    entries = []
    # out formation depend on os
    # every file or dir will callback
    ftp.dir(entries.append)
    ftp.quit()

    print(len(entries), 'entries:')

    for entry in sorted(entries):
        print(entry)


def ftp9():
    """
    recurse dir
    """

    from ftplib import FTP, error_perm
    import getpass

    parser = argparse.ArgumentParser(description='FTP')
    parser.add_argument('host', help='host')
    parser.add_argument('user', help='user')
    parser.add_argument('remotedir', help='remotedir')
    args = parser.parse_args()

    passwd = getpass.getpass()

    def walk_dir(ftp, dirpath):
        original_dir = ftp.pwd()
        try:
            # sniff dir
            ftp.cwd(dirpath)
        except error_perm:
            return 
        print(dirpath)
        names = sorted(ftp.nlst())
        for name in names:
            walk_dir(ftp, os.path.join(dirpath, name))
        ftp.cwd(original_dir)

    ftp = FTP(args.host)
    print("Welcome:", ftp.getwelcome())
    ftp.login(user=args.user, passwd=passwd)
    walk_dir(ftp, args.remotedir)
    ftp.quit()


def ftp10():
    """
    delete
    mkd
    rmd
    rename
    ftp_tls
    """


def rpc_server1():
    """
    xmlrpc: data convert to xml to deliver

    remote procedure call
    just like normal function call
    usage:
    1. distribute task to diff machine
    2. get remote info

    features:
    1. limited data type
    2. raise exception immediately
    3. show supported caller
    4. need supply addressing method
    5. some rpc support auth

    rpc can use in web, mq
    exception example:
    call over, but resp error as network error,
    so try again must consider the over task
    """

    import operator, math
    from xmlrpc.server import SimpleXMLRPCServer
    from functools import reduce

    
    def addtogether(*things):
        """Add together everthing in the list `things`."""
        return reduce(operator.add, things)

    def quadratic(a, b, c):
        """Determin `x` values satisfying: `a` * x * x + `b` * x * x == 0"""
        b24ac = math.sqrt(b*b - 4.0*a*c)
        return list(set([(-b-b24ac) / 2.0*a, (-b+b24ac) / 2.0*a]))

    def remote_repr(arg):
        """Return the `repr()` rendering of supplied `args`."""
        return arg

    server = SimpleXMLRPCServer(('127.0.0.1', 7001))
    server.register_introspection_functions()
    # this server allow simultaneously call multiple func
    # package in network
    server.register_multicall_functions()
    server.register_function(addtogether)
    server.register_function(quadratic)
    server.register_function(remote_repr)
    print('Server ready')
    server.serve_forever()


def rpc_server2():
    """
    json-rpc
    data formation: json
    one of features: support async call
    """
    from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

    def lengths(*args):
        """
        Measure the length of each input argument.
        """
        results = []
        for arg in args:
            try:
                arglen = len(arg)
            except TypeError:
                # json-rpc support return None value
                arglen = None
            results.append((arglen, arg))
        return results

    server = SimpleJSONRPCServer(('localhost', 7002))
    server.register_function(lengths)
    print('Starting server')
    server.serve_forever()


def rpc_server3():
    """
    RpyC
    support other obj, like file obj
    """
    import rpyc
    from rpyc.utils.server import ThreadedServer

    class MyServer(rpyc.Service):
        # method name should start with exposed
        def exposed_line_counter(self, fileobj, function):
            print('Client has invoked exposed_line_counter()')
            for linenum, line in enumerate(fileobj.readlines()):
                # this function define in client
                function(line)
            return linenum + 1 

    t = ThreadedServer(MyServer, port=18861)
    print('Starting server')
    t.start()


def rpc_client1():
    """
    show method supported by server with the use
    of introspect
    """
    import xmlrpc.client

    proxy = xmlrpc.client.ServerProxy('http://127.0.0.1:7001')

    print('Here are the functions supported by this server')
    # this method need server support introspect function
    for method_name in proxy.system.listMethods():
        if method_name.startswith('system.'):
            continue

        # because python have not type definition,
        # so there are nothing return
        signatures = proxy.system.methodSignature(method_name)
        if isinstance(signatures, list) and signatures:
            for signature in signatures:
                print('%s(%s)' % (method_name, signature))
        else:
            print('%s(...)' % (method_name, ))
        
        # get the doc the method
        method_help = proxy.system.methodHelp(method_name)
        if method_help:
            print(' ', method_help)


def rpc_client2():
    """
    call rpc
    """
    import xmlrpc.client

    proxy = xmlrpc.client.ServerProxy('http://127.0.0.1:7001')
    # no limit for param type
    # return value must only one
    print(proxy.addtogether('x', 'y', 'z'))
    print(proxy.addtogether(20, 30, 41, 1))
    print(proxy.quadratic(2, -4, 0))
    print(proxy.quadratic(1, 2, 1))
    # param will convert to list to pass
    # as most language support list param
    print(proxy.remote_repr((1, 2.0, 'thress')))
    print(proxy.remote_repr([1, 2.0, 'thress']))
    # if param is dict, key must be a string
    print(proxy.remote_repr({'name': 'Mike', 
                             'data': {'age': 41, 'sex': 'M'}}))
    # exception formation only one as ignore what language that
    # server use
    print(proxy.quadratic(1, 0, 1))

    # None type param can set option to support


def rpc_client3():
    """
    multi call at an network loop
    """
    import xmlrpc.client

    proxy = xmlrpc.client.ServerProxy('http://127.0.0.1:7001')
    multicall = xmlrpc.client.MultiCall(proxy)
    multicall.addtogether('a', 'b', 'c')
    multicall.quadratic(2, -4, 0)
    multicall.remote_repr([1, 2.0, 'three'])
    for answer in multicall():
        print(answer)


def rpc_client4():
    """
    json rpc
    """
    from jsonrpclib import Server

    proxy = Server('http://localhost:7002')
    # param will convert to list to pass, key of dict must be string
    # but can achive this through list that contain multiple dict
    print(proxy.lengths((1, 2, 3), 27, {'Sirius': -1.46, 'Rigel': 0.12}))


def rpc_client5():
    """
    rpyc client
    """
    import rpyc

    def noisy(string):
        print('Noisy:', repr(string))

    # this config allow remote call attrs of local obj
    config = {'allow_public_attrs': True}
    proxy = rpyc.connect('localhost', 18861, config=config)
    # open a local file
    fileobj = open('wordid.py')
    # this file obj will deliver to server
    # server can call obj's method
    linecount = proxy.root.line_counter(fileobj, noisy)
    print('The number of lines in the file was', linecount)


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


def bootrpc():
    if len(sys.argv) != 2:
        print('usage:', sys.argv[0], 'type')
        return

    if sys.argv[1] == 'rpcserver1':
        rpc_server1()
    elif sys.argv[1] == 'rpcserver2':
        rpc_server2()
    elif sys.argv[1] == 'rpcserver3':
        rpc_server3()
    elif sys.argv[1] == 'rpcclient1':
        rpc_client1()
    elif sys.argv[1] == 'rpcclient2':
        rpc_client2()
    elif sys.argv[1] == 'rpcclient3':
        rpc_client3()
    elif sys.argv[1] == 'rpcclient4':
        rpc_client4()
    elif sys.argv[1] == 'rpcclient5':
        rpc_client5()


def main():
    bootrpc()


if __name__ == '__main__':
    main()

