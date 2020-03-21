import socket
import _thread
import sys
import sqlite3


def Client_Work(ClientSocket, addr):
    msg = "Welcome to my BBS server\r\n"
    ClientSocket.send(msg.encode('utf-8'))
    ClientSocket.recv(1024)
    msg_input = ""
    
    conn = sqlite3.connect('BBS.db')
    print("opened databases successfully")
    c = conn.cursor()
##########
    str_input = "register name123 email pass"
    str_split = str_input.split()
    cursor = c.execute('INSERT INTO USERS ("Username", "Email", "Password") VALUES (?, ?, ?)', (str_split[1], str_split[2], str_split[3]))
    conn.commit()
    conn.close()
##########
    while True:
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

server.listen(17)
print ("[*] Listening on  ", bind_ip,  bind_port)

while True:
    client,addr = server.accept()
    print ("New Client connection :", addr)
    _thread.start_new_thread(Client_Work, (client, addr))
