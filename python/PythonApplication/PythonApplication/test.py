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