import socket

bind_ip = "0.0.0.0"
bind_port = 3110

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(11)

print ("[*] Listening on %s:%d ",   (bind_ip,bind_port))

while True:
    client,addr = server.accept()
    print ('Connected by ', addr)

    while True:
        data = client.recv(1024)
        print ("Client recv data : %s ",  (data))

        client.send("ACK!")
