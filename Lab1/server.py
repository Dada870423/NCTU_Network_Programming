import socket
import _thread
import sys

def Client_Work(ClientSocket, addr):
	msg = "Welcome to my BBS server\r\n"
	ClientSocket.send(msg.encode('utf-8'))
	ClientSocket.recv(1024)
	while True:
		msg_input = ""
		if msg_input != "":
			msg = "% "
			ClientSocket.send(msg.encode('utf-8'))
		msg_input = ClientSocket.recv(1024).decode('utf-8')
		msg_input = msg_input.replace('\n', '').replace('\r', '')
		print(msg_input)
		

bind_ip = "0.0.0.0"
bind_port = 3110

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(11)
print ("[*] Listening on  ", bind_ip,  bind_port)

while True:
    client,addr = server.accept()
    print ("New Client connection :", addr)
    _thread.start_new_thread(Client_Work(server, addr))
