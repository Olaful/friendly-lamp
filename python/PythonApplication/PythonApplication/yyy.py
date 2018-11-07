import socket
client = socket.socket()
client.connect((socket.gethostname(), 1025))
print(client.recv(1024))
client.send('de')