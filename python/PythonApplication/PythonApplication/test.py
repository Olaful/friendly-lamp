"""
import socket
client = socket.socket()
host  = socket.gethostname()
port = 1025
client.connect((host, port))
print(client.recv(1024))
    """
#---------------------------------------------------------------
def square(x):
    """
    >>> square(2)
    4
    >>> square(5)
    25
    """
    return x*x

def func2():
    """
    >>> from urllib.request import urlopen
    >>> urlopen('http://127.0.0.1:8080/kamm').read().decode('utf-8')
    >>> 1
    """

def func3(x, y):
    if x == 7 and y == 9:
        return 'unexpected numer'
    # pylint检查会提示，return后面不必要的else
    # 所以为了规范，后面的return不放在else中了
    #else:
    #    return x*y
    return x*y

if __name__ == '__main__':
    import doctest, test
    doctest.testmod(test)