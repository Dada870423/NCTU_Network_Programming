import socket
import _thread
import sys
import sqlite3
from sqlite3 import Error

def Client_Work(ClientSocket, addr):
    msg = "Welcome to my BBS server\r\n"
    ClientSocket.send(msg.encode('utf-8'))
    ClientSocket.recv(1024)
    msg_input = ""  # get out the trash
    
    login = -1 ## check login or not and whoami


    conn = sqlite3.connect('BBS.db')
    print("opened databases successfully")
    c = conn.cursor()
    while True:
        
        msg = "% "
        ClientSocket.send(msg.encode('utf-8'))
        msg_input = ClientSocket.recv(1024).decode('utf-8')
        msg_input = msg_input.replace('\n', '').replace('\r', '')
        msg_split = msg_input.split()

        print("msg : ", msg_input, "  len: ", len(msg_split))
        if len(msg_split) == 4 and msg_split[0] == "register":
            try:
                cursor = c.execute('INSERT INTO USERS ("Username", "Email", "Password") VALUES (?, ?, ?)', (msg_split[1], msg_split[2], msg_split[3]))
                conn.commit()
                print("Insertion is success")
                msg_suc = "Register successfully\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
            except Error:
                print("Username is already used")
                msg_err = "Username is already used\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
        elif len(msg_split) == 1:
            if msg_input == "register":
                msg_err = "Usage: register <username> <email> <password>\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
        elif len(msg_split) > 1:
            if msg_split[0] == "register":
                msg_err = "Usage: register <username> <email> <password>\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))

        
        if len(msg_split) == 3 and msg_split[0] == "login":
            if login > -1:
                msg_err = "Please logout first\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            cursor = c.execute('SELECT * FROM USERS WHERE Username = ?', (msg_split[1],))
            cursor = cursor.fetchone()
            if cursor != None and cursor[3] == msg_split[2]: #person is exist
                print("She is ", cursor[0], cursor[1])
                login = cursor[0]
                msg_suc = "Welcome, " + cursor[1] + "\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
            else: # no such person or password is incorrect
                msg_err = "Login failed" + "\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
        elif len(msg_split) == 1:
            if msg_input == "login":
                msg_err = "Usage: login <username> <password>\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
        elif len(msg_split) > 1:
            if msg_split[0] == "login":
                msg_err = "Usage: login <username> <password>\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))

        if msg_input == "whoami":
            if login > -1:
                cursor = c.execute('SELECT * FROM USERS WHERE UID = ?', (login,))
                cursor = cursor.fetchone()
                print("I am ", cursor[0], "\r\n")
                msg_suc = cursor[1] + "\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
            else:
                msg_err = "Please login first\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))

        if msg_input == "logout":
            if login > -1:
                cursor = c.execute('SELECT * FROM USERS WHERE UID = ?', (login,))
                cursor = cursor.fetchone()
                print("I am ", cursor[0], "\r\n")
                msg_suc = "Bye, " + cursor[1] + "\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
            else:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))


        if msg_input == "exit":
            print("the client ", login," want to bye")
            server.shutdown(0)
            #server.close()







bind_ip = "0.0.0.0"
bind_port = 3110

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(17)
print ("[*] Listening on  ", bind_ip,  bind_port)

while True:
    client,addr = server.accept()
    print ("New connection :", addr)
    _thread.start_new_thread(Client_Work, (client, addr))
