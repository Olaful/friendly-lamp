""""
import socket
client = socket.socket()
client.connect((socket.gethostname(), 1025))
print(client.recv(1024))
client.send('de')

import sys
name = sys.argv[0]
print(name)
"""
#-------------------------------------
def squra(x):
    """
    test function
    >>> squra(2)
    5
    >>> squra(5)
    25
    """
    return x*x

def func2():
    """
    >>> from urllib.request import urlopen
    >>> urlopen('http://127.0.0.1:8080/kamm').read().decode('utf-8')
    >>> 1
    """

def func3(x,y):
    if x == 7 and y == 9:
        return 'unexpected numer'
    else:
        return x*y

def func4():
    from mylib import mydll
    isHw = mydll.is_huiwen('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhehhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    print(isHw)

def func5():
    test = 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhehhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
    nLen = len(test)
    for i in range(nLen//2):
        if test[i] != test[nLen-1-i]:
            return False
    return True

def func6(nNum):
    for i in range(nNum):
        a = i
    return a - 1

def func7(nNum):
    from mylib import mydll
    test = mydll.vistData(nNum)

if __name__ == '__main__':
    # import doctest, test
    # doctest.testmod(test)
    ''