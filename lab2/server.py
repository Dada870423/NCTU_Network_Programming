import socket
import _thread
import sys
import sqlite3
import os
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
            continue
        elif (msg_input == "register") or (len(msg_split) > 1 and msg_split[0] == "register"):
            msg_err = "Usage: register <username> <email> <password>\r\n"
            ClientSocket.send(msg_err.encode('utf-8'))
            continue
       

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
            continue
        elif (len(msg_split) > 1 and msg_split[0] == "login") or (msg_input == "login"):
            msg_err = "Usage: login <username> <password>\r\n"
            ClientSocket.send(msg_err.encode('utf-8'))
            continue

        if msg_input == "whoami":
            if login > -1:
                cursor = c.execute('SELECT * FROM USERS WHERE UID = ?', (login,))
                cursor = cursor.fetchone()
                print("I am ", cursor[0])
                msg_suc = cursor[1] + "\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
            else:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                print("He didn't login")
            continue

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
            continue

        if msg_input == "exit":
            print("the client ", login," want to bye")
            ClientSocket.close()
            break

################################################################################################### Lab1 done
        if len(msg_split) == 2 and msg_split[0] == "create-board":
            if login == -1:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            try:
                cursor = c.execute('INSERT INTO BOARDS ("BName", "Moderator_id") VALUES (?, ?) ', (msg_split[1], login))
                conn.commit()
                print("Board insertion is success")
                msg_suc = "Create board srccessfully.\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
            except Error:
                print("Board is already exist")
                msg_err = "Board is already exist\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
            continue
        elif (len(msg_split) == 1 and msg_input == "create-board") or (len(msg_split) > 1 and msg_split[0] == "create-board"):
            msg_err = "Usage: create-board <Board Name>\r\n"
            ClientSocket.send(msg_err.encode('utf-8'))
            continue
## Create board done
## To list the board
        if len(msg_split) == 2 and msg_split[0] == "list-board": ## with keyword
            if login == -1:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            hashtag = "##"
            if hashtag in msg_split[1]:
            	msg_split[1] = msg_split[1].replace("##", "")
            else:
            	msg_err = "Use ## to search keyword.\r\n"
            	ClientSocket.send(msg_err.encode('utf-8'))
            	continue
            srch_board = "%" + msg_split[1] + "%"
            cursor = c.execute("SELECT * FROM BOARDS WHERE BName LIKE ?", (srch_board, ))
            cursor = cursor.fetchone()
            print(cursor)
            if cursor == None:
                msg_err = "No keyword board yet.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            msg_suc = "{:^7} {:^20} {:^20} \r\n\r\n".format("Index", "Name", "Moderator")
            ClientSocket.send(msg_suc.encode('utf-8'))
            for row in c.execute("SELECT * FROM BOARDS WHERE BName LIKE ?", (srch_board, )):
                print("{:>5} {:^20} {:^20}".format(row[0], row[1], row[2]))
                msg_suc = "{:>7} {:^20} {:^20}\r\n\r\n".format(row[0], row[1], row[2])
                ClientSocket.send(msg_suc.encode('utf-8'))
            continue

        elif msg_input == "list-board": ## without keyword
            if login == -1:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            cursor = c.execute("SELECT * FROM BOARDS")
            cursor = cursor.fetchone()
            print(cursor)
            if cursor == None:
                msg_err = "There is not any board yet.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            msg_suc = "{:^7} {:^20} {:^20} \r\n\r\n".format("Index", "Name", "Moderator")
            ClientSocket.send(msg_suc.encode('utf-8'))
            for row in c.execute("SELECT * FROM BOARDS"):
                print("{:>5} {:^20} {:^20}".format(row[0], row[1], row[2]))
                msg_suc = "{:>7} {:^20} {:^20}\r\n\r\n".format(row[0], row[1], row[2])
                ClientSocket.send(msg_suc.encode('utf-8'))
            continue

## Command not found
        if msg_input != "":
            msg_err = "Command not found\r\n"
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
