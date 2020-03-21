import socket
## no need the clinet
HOST = '54.198.148.205'
PORT = 3110

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    cmd = input("Please input msg:")
    s.send(cmd.encode('utf-8'))
    data = s.recv(1024)
    print ("server send :  ", data.decode('utf-8'))
