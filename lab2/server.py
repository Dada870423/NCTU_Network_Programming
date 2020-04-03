import socket
import _thread
import sys
import time
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
    hashtag = "##"
    TITLE = " --title "
    CONTENT = " --content "
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

        if msg_input.startswith("register "):
            if len(msg_split) == 4:
                try:
                    cursor = c.execute('INSERT INTO USERS ("Username", "Email", "Password") VALUES (?, ?, ?)', (msg_split[1], msg_split[2], msg_split[3]))
                    conn.commit()
                    print("USER insertion is success")
                    msg_suc = "Register successfully.\r\n"
                    ClientSocket.send(msg_suc.encode('utf-8'))
                except Error:
                    print("Username is already used")
                    msg_err = "Username is already used.\r\n"
                    ClientSocket.send(msg_err.encode('utf-8'))
                continue
       

        if msg_input.startswith("login "):
            if login > -1:
                    msg_err = "Please logout first.\r\n"
                    ClientSocket.send(msg_err.encode('utf-8'))
                    continue
            elif len(msg_split) == 3:
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
                print("Bye from ", cursor[0], "\r\n")
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
        if msg_input.startswith("create-board "):
            if login == -1:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            BName = msg_input.replace("create-board ", "")
            try:
                cursor = c.execute('INSERT INTO BOARDS ("BName", "Uid") VALUES (?, ?) ', (BName, login))
                conn.commit()
                print("Board insertion is success")
                msg_suc = "Create board srccessfully.\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
                continue
            except Error:
                print("Board is already exist")
                msg_err = "Board is already exist\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue

            
## Create board done
## To list the board
        if msg_input.startswith("list-board"): 
            HBName = msg_input.replace("list-board", "")
            if login == -1:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            elif msg_input == "list-board": ## without keyword
                cursor = c.execute("SELECT * FROM BOARDS")
                cursor = cursor.fetchone()
                if cursor == None:
                    print(cursor)
                    msg_err = "There is not any board yet.\r\n"
                    ClientSocket.send(msg_err.encode('utf-8'))
                else:
                    msg_suc = "{:^7} {:^20} {:^20} \r\n\r\n".format("Index", "Name", "Moderator")
                    ClientSocket.send(msg_suc.encode('utf-8'))
                    for row in c.execute("SELECT BOARDS.BID, BOARDS.BName, USERS.Username FROM BOARDS INNER JOIN USERS ON BOARDS.UID=USERS.UID"):
                        print("{:>5} {:^20} {:^20}".format(row[0], row[1], row[2]))
                        msg_suc = "{:>7} {:^20} {:^20}\r\n\r\n".format(row[0], row[1], row[2])
                        ClientSocket.send(msg_suc.encode('utf-8'))
                continue    
            elif hashtag in HBName: ## with keyword
                BName = HBName.replace(" ##", "")
                BName = "%" + BName + "%"
                cursor = c.execute("SELECT BOARDS.BID, BOARDS.BName, USERS.Username FROM BOARDS INNER JOIN USERS ON BOARDS.UID=USERS.UID WHERE BOARDS.BName LIKE ?", (BName, ))
                cursor = cursor.fetchone()
	            
                if cursor == None:
                    print(cursor)	
                    msg_err = "No keyword board yet.\r\n"
                    ClientSocket.send(msg_err.encode('utf-8'))
                    continue
                msg_suc = "{:^7} {:^20} {:^20} \r\n\r\n".format("Index", "Name", "Moderator")
                ClientSocket.send(msg_suc.encode('utf-8'))
                ## for row in c.execute("SELECT * FROM BOARDS WHERE BName LIKE ?", (srch_board, )):
                for row in c.execute("SELECT BOARDS.BID, BOARDS.BName, USERS.Username FROM BOARDS INNER JOIN USERS ON BOARDS.UID=USERS.UID WHERE BOARDS.BName LIKE ?", (BName, )):
                    print("{:>5} {:^20} {:^20}".format(row[0], row[1], row[2]))
                    msg_suc = "{:>7} {:^20} {:^20}\r\n\r\n".format(row[0], row[1], row[2])
                    ClientSocket.send(msg_suc.encode('utf-8'))
                continue

## create the post & file of comment
        if msg_input.startswith("create-post"):                             
            if login == -1:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            elif len(msg_split) > 5 and TITLE in msg_input and CONTENT in msg_input:                                        
                no_create = msg_input.replace("create-post ", "")           ## Bname = BoardTitle[0]
                if no_create.startswith("--title"):
                    print("He did not choose the board")
                    msg_err = "Please choose a board.\r\n"
                    ClientSocket.send(msg_err.encode('utf-8'))
                    continue
                BoardTitle = no_create.split(" --title ")                   ## Title = TitleContent[0]
                TitleContent = BoardTitle[1].split(" --content ")           ## Content = TitleContent[1]
                print("Board name is : ", BoardTitle[0], "Title is : ", TitleContent[0], "Content is : ", TitleContent[1])
                cursor = c.execute('SELECT * FROM BOARDS WHERE BName = ?', (BoardTitle[0],))
                cursor = cursor.fetchone()
                if cursor != None: #Board is exist
                    print("Board exist")
                else:
                    print("Board is not exist")
                    msg_err = "Board is not exist.\r\n"
                    ClientSocket.send(msg_err.encode('utf-8'))
                    continue
                
                NowTime = time.strftime("%Y/%m/%d", time.localtime()) ## is a string
                print(NowTime, type(NowTime))
                cursor = c.execute('INSERT INTO POSTS ("TITLE", "BName", "UID", "DT") VALUES (?, ?, ?, ?)', (TitleContent[0], BoardTitle[0], login, NowTime))
                conn.commit()
                print("POST insertion is success")
                msg_suc = "CREATE POST successfully.\r\n"
                ClientSocket.send(msg_suc.encode('utf-8'))
                DIR = 'data/post'
                P_num = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) 
                
                cnt = TitleContent[1].split("<br>")
                os.system("echo "" >> data/comment/{}".format(P_num+1))
                for iter_cnt in cnt:
                    print(iter_cnt)
                    os.system("echo {} >> data/post/{}".format(iter_cnt, P_num+1))
                continue



        if msg_input.startswith("list-post"): 
            BName = msg_input.replace("list-post ", "")
            if login == -1:
                msg_err = "Please login first.\r\n"
                ClientSocket.send(msg_err.encode('utf-8'))
                continue
            elif len(msg_split) > 1 and hashtag in BName: ## with keyword
                continue
            elif len(msg_split) > 1:                      ## without keyword
                print("Want to search in ", BName, " Board")
                cursor = c.execute('SELECT * FROM BOARDS WHERE BName = ?', (BName,))
                cursor = cursor.fetchone()
                if cursor == None:                        ## Board is not exist
                    print("Board is not exist")
                    msg_err = "Board is not exist.\r\n"
                    ClientSocket.send(msg_err.encode('utf-8'))
                    continue
                else:
                    print("Board is exist")
                    msg_suc = "{:^7} {:^20} {:^20} {:^9}\r\n\r\n".format("ID", "Title", "Author", "Date")
                    ClientSocket.send(msg_suc.encode('utf-8'))
                    for row in c.execute("SELECT POSTS.PID, POSTS.TITLE, USERS.Username, POSTS.DT FROM POSTS INNER JOIN USERS ON POSTS.UID=USERS.UID WHERE POSTS.BName=?", (BName, )):
                        print("{:>5} {:^20} {:^20} {:^9}".format(row[0], row[1], row[2], row[3]))
                        msg_suc = "{:>7} {:^20} {:^20} {:^9}\r\n\r\n".format(row[0], row[1], row[2], row[3])
                        ClientSocket.send(msg_suc.encode('utf-8'))


                continue















## Command not found
        if msg_input.startswith("register"):
            msg_err = "Usage: register <username> <email> <password>\r\n"
        elif msg_input.startswith("login"):
            msg_err = "Usage: login <username> <password>\r\n"
        elif msg_input.startswith("whoami"):
            msg_err = "Usage: whoami\r\n"
        elif msg_input.startswith("logout"):
            msg_err = "Usage: logout\r\n"
        elif msg_input.startswith("exit"):
            msg_err = "Usage: exit\r\n"
        elif msg_input.startswith("create-board"):
            msg_err = "Usage: create-board <Board Name>\r\n"
        elif msg_input.startswith("list-board"):
            if hashtag in msg_input:
                msg_err = "Usage: list-board ##<keyword>\r\n"
            else:
                msg_err = "Usage: list-board\r\n"
        elif msg_input.startswith("create-post"):
            msg_err = "Usage: create-post <Board Name> --title <title> --content <content>\r\n"
        elif msg_input.startswith("list-post"):
            if hashtag in msg_input:
                msg_err = "Usage: list-post <Board Name> ##<keyword>\r\n"
            else:
                msg_err = "Usage: list-post <Board Name>\r\n"
        elif msg_input != "":
            msg_err = "Command not found\r\n"
        
        if msg_input != "":
            ClientSocket.send(msg_err.encode('utf-8'))



#CREATE TABLE BOARDS(
#BID INTEGER PRIMARY KEY AUTOINCREMENT,
#BName TEXT NOT NULL UNIQUE,
#UID INTEGER);

#CREATE TABLE POSTS(
#PID INTEGER PRIMARY KEY AUTOINCREMENT,
#TITLE TEXT NOT NULL,
#BName TEXT,
#UID INTEGER,
#DT TEXT);








P_num = 1

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
