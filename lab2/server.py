import socket
import _thread
import sys
import sqlite3
from sqlite3 import Error

def Client_Work(ClientSocket, addr):
    msg = "*************************************************************************************************************************************\r\n"
    ClientSocket.send(msg.encode('utf-8'))
    #print welcome msg
    msg = "__        __   _                            _          _   _             ____  ____ ____ \r\n"
    ClientSocket.send(msg.encode('utf-8'))
    msg = "\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |_| |__   ___   | __ )| __ ) ___| \r\n"
    ClientSocket.send(msg.encode('utf-8'))
    msg = " \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | __| '_ \ / _ \  |  _ \|  _ \___ \   / __|/ _ \ '__\ \ / / _ \ '__| \r\n"
    ClientSocket.send(msg.encode('utf-8'))
    msg = "  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |_| | | |  __/  | |_) | |_) |__) |  \__ \  __/ |   \ V /  __/ | \r\n"
    ClientSocket.send(msg.encode('utf-8'))
    msg = "   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \__|_| |_|\___|  |____/|____/____/   |___/\___|_|    \_/ \___|_|  \r\n\r\n"
    ClientSocket.send(msg.encode('utf-8'))
    msg = "*************************************************************************************************************************************\r\n"
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
################################################################################################## Lab1
        print("msg : ", msg_input, "  len: ", len(msg_split))
        if len(msg_split) == 4 and msg_split[0] == "register":
            try:
                cursor = c.execute('INSERT INTO USERS ("Username", "Email", "Password") VALUES (?, ?, ?)', (msg_split[1], msg_split[2], msg_split[3]))
                conn.commit()
                print("Insertion is success")
                msg_suc = "Register successfully.\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
            except Error:
                print("Username is already used")
                msg_err = "Username is already used.\r\n"
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
                msg_err = "Please logout first.\r\n"
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
                msg_err = "Login failed." + "\r\n"
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
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))

        if msg_input == "logout":
            if login > -1:
                cursor = c.execute('SELECT * FROM USERS WHERE UID = ?', (login,))
                cursor = cursor.fetchone()
                login = -1
                print("I am ", cursor[0], "\r\n")
                msg_suc = "Bye, " + cursor[1] + "\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
            else:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))


        if msg_input == "exit":
            print("the client ", login," want to bye")
            ClientSocket.close()
            break

################################################################################################### Lab1 done
        if len(msg_split) == 2 and msg_split[0] == "create-board":
            if login == 0:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            try:
                cursor = c.execute('INSERT INTO BOARDS ("BName") VALUES (?) ', msg_split[1])
                conn.commit()
                print("Board insertion is success")
                os.system("mkdir data/{}".format(msg_split[1]))
                os.system("mkdir data/{}/post".format(msg_split[1]))
                os.system("mkdir data/{}/comment".format(msg_split[1]))
                msg_suc = "Create board srccessfully.\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
            except Error:
                print("Board is already exist")
                msg_err = "Board is already exist\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
        elif (len(msg_split) == 1 and msg_input == "create-board") or (len(msg_split) > 1 and msg_split[0] == "create-board"):
            msg_err = "Usage: create-board <Board Name>\r\n"
            ClientSocket.send(msg_err.encode('utf-8'))










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
