# -*- coding: utf-8 -*-

import argparse, random, socket, sys

def server(interface, port):
    MAX_BYTES = 65535

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

def client(hostname, port):
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

def main():
    choice = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP')
    parser.add_argument('role', choices=choice, help='which role to take')
    parser.add_argument('host', help='interface the server listen at;'
                        'host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choice[args.role]
    function(args.host, args.p)

if __name__ == '__main__':
    main()
