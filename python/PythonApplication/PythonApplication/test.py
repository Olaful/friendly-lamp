import socket
client = socket.socket()
host  = socket.gethostname()
port = 1025
client.connect((host, port))
print(client.recv(1024))