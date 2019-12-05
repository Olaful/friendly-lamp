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
import sys, random

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

def main():
    boottcp2()

if __name__ == '__main__':
    main()