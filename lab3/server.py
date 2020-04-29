import socket
import _thread
import sys
import time
import sqlite3
import os
from sqlite3 import Error

def Client_Work(ClientSocket, addr):
    def RECEIVE():
        while True:
            try:
                msg_in = ClientSocket.recv(1024).decode('utf-8')
                return msg_in
            except:
                pass    

    def SEND(CMD):
        while True:
            try:
                ClientSocket.send(CMD.encode('utf-8'))
                return "Send_suc"
            except:
                pass


    ClientSocket.setblocking(0)
    


    ## print welcome msg
    msg = ""
    msg =  "*************************************************************************************************************************************\r\n" + \
           "__        __   _                            _          _   _             ____  ____ ____                                             \r\n" + \
           "\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |_| |__   ___   | __ )| __ ) ___|                                            \r\n" + \
           " \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | __| '_ \ / _ \  |  _ \|  _ \___ \   / __|/ _ \ '__\ \ / / _ \ '__|           \r\n" + \
           "  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |_| | | |  __/  | |_) | |_) |__) |  \__ \  __/ |   \ V /  __/ |              \r\n" + \
           "   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \__|_| |_|\___|  |____/|____/____/   |___/\___|_|    \_/ \___|_|          \r\n\r\n" + \
           "*************************************************************************************************************************************\r\n"
    SEND(CMD = msg)

    # ClientSocket.recv(1024) # there is no trash in cmd 
    
    # Initialize
    login = -1 ## check login or not and whoami
    msg_suc = ""
    msg_err = ""
    msg_Usage = ""
    msg_output = ""
    hashtag = "##"
    TITLE = " --title "
    SUBJECT = " --subject "
    CONTENT = " --content "
    POS = "POS"
    NEG = "NEG"
    board_Col_name = "{:^7} {:^20} {:^20} \r\n\r\n".format("Index", "Name", "Moderator")
    post_Col_name = "{:^7} {:^20} {:^20} {:^9}\r\n\r\n".format("ID", "Title", "Author", "Date")
    conn = sqlite3.connect('BBS.db')
    print("opened databases successfully")
    c = conn.cursor()
    while True:
        # msg = "% "
        # ClientSocket.send(msg.encode('utf-8'))
        msg_input = RECEIVE()
        msg_input = msg_input.replace('\n', '').replace('\r', '')
        msg_split = msg_input.split()
        print("msg : ", msg_input, "  len: ", len(msg_split))
        
        ## register
        if msg_input.startswith("register "):
            if len(msg_split) == 4:
                cursor = c.execute('SELECT * FROM USERS WHERE Username = ?', (msg_split[1],)).fetchone()
                if cursor == None:
                    SEND(CMD = POS)
                    BucketName = RECEIVE()

                    cursor = c.execute('INSERT INTO USERS ("Username", "Email", "Password", "BucketName", "Mnum") VALUES (?, ?, ?, ?, 0)', (msg_split[1], msg_split[2], msg_split[3], BucketName))
                    conn.commit()
                    print("USER insertion is success")
                    msg_output = "SUC " + "Register successfully."
                    
                else:
                    print("Username is already used")
                    msg_output = "ERR " + "Username is already used."
                SEND(CMD = msg_output)
        ## login
        if msg_input.startswith("login "):
            if len(msg_split) == 3:
                if login > -1:
                    msg_output = "ERR " + "Please logout first."
                    SEND(CMD = msg_output)
                else:
                    cursor = c.execute('SELECT * FROM USERS WHERE Username = ?', (msg_split[1],)).fetchone()
                    if cursor != None and cursor[3] == msg_split[2]: #person is exist
                        print("She is ", cursor[0], cursor[1])
                        login = cursor[0]
                        msg_output = "TROBLE " + cursor[4] + "# #" + "Welcome, " + cursor[1] 
                        SEND(CMD = msg_output)
                    else:   # no such person or password is incorrect
                        msg_output = "ERR " + "Login failed."
                        SEND(CMD = msg_output)
        ## whoami
        if msg_input == "whoami":
            if login > -1:
                cursor = c.execute('SELECT * FROM USERS WHERE UID = ?', (login,)).fetchone()
                print("I am ", cursor[0])
                msg_output = "SUC " + cursor[1]
            else:
                msg_output = "ERR " + "Please login first."
                print("He didn't login")
            SEND(CMD = msg_output)
        ## logout
        if msg_input == "logout":
            if login > -1:
                cursor = c.execute('SELECT * FROM USERS WHERE UID = ?', (login,)).fetchone()
                login = -1
                print("Bye from ", cursor[0], "\r\n")
                msg_output = "SUC " + "Bye, " + cursor[1]
            else:
                msg_output = "ERR " + "Please login first."
            SEND(CMD = msg_output)
        ## exit
        if msg_input == "exit":
            print("the client ", login," want to bye")
            ClientSocket.close()
            break

        ## create-board
        if msg_input.startswith("create-board "):
            if len(msg_split) > 1:
                BName = msg_input.replace("create-board ", "", 1)
                cursor = c.execute('SELECT * FROM BOARDS WHERE BName = ?', (BName,)).fetchone()
                if login == -1:
                    msg_output = "ERR " + "Please login first."
                else:
                    BName = msg_input.replace("create-board ", "", 1)
                    cursor = c.execute('SELECT * FROM BOARDS WHERE BName = ?', (BName,)).fetchone()
                    if cursor == None:
                        cursor = c.execute('INSERT INTO BOARDS ("BName", "Uid") VALUES (?, ?) ', (BName, login))
                        conn.commit()
                        print("Board insertion is success")
                        msg_output = "SUC " + "Create board successfully."
                    else:
                        print("Board is already exist")
                        msg_output = "ERR " + "Board is already exist."
                SEND(CMD = msg_output)




        ## To list the board
        if msg_input.startswith("list-board"): 
            
            HBName = msg_input.replace("list-board", "", 1)
            if msg_input == "list-board": ## without keyword
                cursor = c.execute("SELECT * FROM BOARDS").fetchone()
                if cursor == None:
                    print(cursor)
                    SEND(CMD = NEG)
                else:
                    msg_output = "DATA "
                    for row in c.execute("SELECT BOARDS.BID, BOARDS.BName, USERS.Username FROM BOARDS INNER JOIN USERS ON BOARDS.UID=USERS.UID"):
                        print("{:>5} {:^20} {:^20}".format(row[0], row[1], row[2]))
                        msg_output = msg_output + "{:>7} {:^20} {:^20}\r\n\r\n".format(row[0], row[1], row[2])
                    SEND(CMD = msg_output)

            elif hashtag in HBName: ## with keyword
                BName = HBName.replace(" ##", "", 1)
                BName = "%" + BName + "%"
                cursor = c.execute("SELECT BOARDS.BID, BOARDS.BName, USERS.Username FROM BOARDS INNER JOIN USERS ON BOARDS.UID=USERS.UID WHERE BOARDS.BName LIKE ?", (BName, )).fetchone()
                if cursor == None:
                    print(cursor)
                    SEND(CMD = NEG)
                else:
                    msg_output = "DATA "
                    for row in c.execute("SELECT BOARDS.BID, BOARDS.BName, USERS.Username FROM BOARDS INNER JOIN USERS ON BOARDS.UID=USERS.UID WHERE BOARDS.BName LIKE ?", (BName, )):
                        print("{:>5} {:^20} {:^20}".format(row[0], row[1], row[2]))
                        msg_output = msg_output + "{:>7} {:^20} {:^20}\r\n\r\n".format(row[0], row[1], row[2])
                    SEND(CMD = msg_output)



        ## create the post & file of comment
        if msg_input.startswith("create-post "):         
            if len(msg_split) > 5 and TITLE in msg_input and CONTENT in msg_input:                                        
                no_create = msg_input.replace("create-post ", "", 1)           ## Bname = BoardTitle[0]
                if login == -1:
                    msg_output = "ERR " + "Please login first."
                    SEND(CMD = msg_output)
                elif msg_split[1] == "--title":                                ## Title = TitleContent[0]
                    print("He did not choose the board")                       ## Content = TitleContent[1]
                elif msg_split[3] == "--content":
                    print("He did not name the title")
                else:
                    BoardTitle = no_create.split(" --title ")                   
                    TitleContent = BoardTitle[1].split(" --content ")           
                    print("Board name is : ", BoardTitle[0], "Title is : ", TitleContent[0], "Content is : ", TitleContent[1])
                    cursor = c.execute('SELECT * FROM BOARDS WHERE BName = ?', (BoardTitle[0],)).fetchone()
                    if cursor == None: #Board is not exist
                        print("Board is not exist")
                        msg_output = "ERR " + "Board is not exist."
                        SEND(CMD = msg_output)
                    else:
                        print("Board exist")

                        NowTime = time.strftime("%m/%d", time.localtime()) ## is a string
                        cursor = c.execute('INSERT INTO POSTS ("TITLE", "BName", "UID", "DT") VALUES (?, ?, ?, ?)', (TitleContent[0], BoardTitle[0], login, NowTime))
                        conn.commit()
                        Last_post = c.execute('SELECT * FROM POSTS WHERE TITLE = ?', (TitleContent[0],)).fetchall()
                        PID = str(Last_post[-1][0])
                        print(NowTime, type(NowTime), "POST insertion is success")
                        msg_output = "TROBLE " + PID + "# #" + "Create post successfully."
                        SEND(CMD = msg_output)



        ## list the post with ## or not
        if msg_input.startswith("list-post "): 
            BName = msg_input.replace("list-post ", "", 1)
            
            ## with keyword
            if hashtag in BName: 
                if msg_split[1].startswith("##"):
                    print("He did not choose the board")
                else:
                    BNameKey = BName.split(" ##")
                    BName = BNameKey[0]
                    keyword = "%" + BNameKey[1] + "%"
                    print("Bname is :", BName, "keyword is :", keyword)
                    cursor = c.execute('SELECT * FROM BOARDS WHERE BName = ?', (BName,)).fetchone()
                    if cursor == None:                        ## Board is not exist
                        print("Board is not exist")
                        msg_output = "ERR " + "Board is not exist."
                        SEND(CMD = msg_output)
                    else:
                        print("Board is exist")
                        cursor = c.execute("SELECT POSTS.PID, POSTS.TITLE, USERS.Username, POSTS.DT FROM POSTS INNER JOIN USERS ON POSTS.UID=USERS.UID WHERE POSTS.BName=? and POSTS.TITLE LIKE ?", (BName, keyword)).fetchone()
                        if cursor == None:  ## there is not any post in this board 
                            print(cursor)
                            SEND(CMD = NEG)
                        else:
                            msg_output = "DATA "
                            for row in c.execute("SELECT POSTS.PID, POSTS.TITLE, USERS.Username, POSTS.DT FROM POSTS INNER JOIN USERS ON POSTS.UID=USERS.UID WHERE POSTS.BName=? and POSTS.TITLE LIKE ?", (BName, keyword)):
                                print("{:>5} {:^20} {:^20} {:^9}".format(row[0], row[1], row[2], row[3]))
                                msg_output = msg_output + "{:>7} {:^20} {:^20} {:^9}\r\n".format(row[0], row[1], row[2], row[3])
                            SEND(CMD = msg_output)
            ## without keyword
            else:  
                print("Want to search in ", BName, " Board")
                cursor = c.execute('SELECT * FROM BOARDS WHERE BName = ?', (BName,)).fetchone()
                if cursor == None:                        ## Board is not exist
                    print("Board is not exist")
                    msg_output = "ERR " + "Board is not exist."
                    SEND(CMD = msg_output)
                else:
                    print("Board is exist")
                    cursor = c.execute("SELECT POSTS.PID, POSTS.TITLE, USERS.Username, POSTS.DT FROM POSTS INNER JOIN USERS ON POSTS.UID=USERS.UID WHERE POSTS.BName=?", (BName, )).fetchone()
                    if cursor == None:  ## there is not any post in this board 
                        print(cursor)
                        SEND(CMD = NEG)
                    else:
                        msg_output = "DATA "
                        for row in c.execute("SELECT POSTS.PID, POSTS.TITLE, USERS.Username, POSTS.DT FROM POSTS INNER JOIN USERS ON POSTS.UID=USERS.UID WHERE POSTS.BName=?", (BName, )):
                            print("{:>5} {:^20} {:^20} {:^9}".format(row[0], row[1], row[2], row[3]))
                            msg_output = msg_output + "{:>7} {:^20} {:^20} {:^9}\r\n\r\n".format(row[0], row[1], row[2], row[3])
                        SEND(CMD = msg_output)

# -------------^ client done

        ## read post and read comment
        if len(msg_split) == 2 and msg_split[0] == "read":
            cursor = c.execute('SELECT * FROM POSTS WHERE PID = ?', (msg_split[1],)).fetchone()
            if cursor == None:
                print(cursor, "Post is not exist.")
                msg_output = "ERR " + "Post is not exist."
                SEND(CMD = msg_output)
            else:
                cursor = c.execute("SELECT USERS.Username, POSTS.TITLE, POSTS.DT, USERS.BucketName FROM POSTS INNER JOIN USERS ON POSTS.UID=USERS.UID WHERE POSTS.PID = ?", (msg_split[1], )).fetchone()
                print(cursor[0], cursor[1], cursor[2], cursor[3]) ##cursor[3] is BucketName
                msg_output = "TROBLE " + cursor[3] + "# #" + "Author : {:>20} \r\nTitle  : {:>20} \r\nDate   : {:>20}\r\n--\r\n".format(cursor[0], cursor[1], cursor[2])
                SEND(CMD = msg_output)


        ## delete the post
        if len(msg_split) == 2 and msg_split[0] == "delete-post":
            if login == -1:
                msg_output = "ERR " + "Please login first."
            else:
                cursor = c.execute('SELECT * FROM POSTS WHERE PID = ?', (msg_split[1],)).fetchone()
                if cursor == None:
                    print(cursor, "Post is not exist.")
                    msg_output = "ERR " + "Post is not exist."
                elif cursor[3] != login:
                    print("Owner is:",  cursor[3])
                    msg_output = "ERR " + "Not the post owner."
                else:
                    cursor = c.execute('DELETE FROM POSTS WHERE PID = ?', (msg_split[1],))
                    conn.commit()
                    print("POST delete is success")
                    msg_output = "SUC " + "Delete successfully."
            SEND(CMD = msg_output)
        ## update the post
        if msg_input.startswith("update-post ") and len(msg_split) > 2:
            if login == -1:
                msg_output = "ERR " + "Please login first."
                SEND(CMD = msg_output)
            else:
                cursor = c.execute('SELECT * FROM POSTS WHERE PID = ?', (msg_split[1],)).fetchone()
                if cursor == None:
                    print(cursor, "Post is not exist.")
                    msg_output = "ERR " + "Post is not exist."
                    SEND(CMD = msg_output)
                elif cursor[3] != login:
                    print("Owner is:",  cursor[3])
                    msg_output = "ERR " + "Not the post owner."
                    SEND(CMD = msg_output)
                elif msg_split[2] == "--title":
                    UTitle = msg_input.split(" --title ") 
                    print("I want to update the title, and the new title is:", UTitle[1])	
                    cursor = c.execute('UPDATE POSTS SET TITLE = ? WHERE PID = ?', (UTitle[1], msg_split[1]))
                    conn.commit()
                    msg_output = "SUC " + "Update successfully.\r\n"
                    SEND(CMD = msg_output)
                elif msg_split[2] == "--content":
                    UContent = msg_input.split(" --content ") 
                    print("I want to update the content, and the new content is:", UContent[1])

                    msg_output = "SUC " + "Update successfully.\r\n"
                    SEND(CMD = msg_output)
        ## comment
        if msg_input.startswith("comment ") and len(msg_split) > 2:
            if login == -1:
                msg_output = "ERR " + "Please login first.\r\n"
                SEND(CMD = msg_output)
            else:
                cursor = c.execute('SELECT * FROM POSTS WHERE PID = ?', (msg_split[1],)).fetchone()
                if cursor == None:
                    print(cursor, "Post is not exist.")
                    msg_output = "ERR " + "Post is not exist."
                    SEND(CMD = msg_output)
                else:
                    starts = "comment " + msg_split[1] + " "
                    Ccomment = msg_input.replace(starts, "", 1)

                    cursor = c.execute('SELECT * FROM USERS WHERE UID = ?', (login,)).fetchone()
                    Cname = cursor[1]
                    print("I am ", Cname, "and i want to comment", Ccomment, "in", msg_split[1])
                    cursor = c.execute("SELECT USERS.Username, USERS.BucketName FROM POSTS INNER JOIN USERS ON POSTS.UID=USERS.UID WHERE POSTS.PID = ?", (msg_split[1], )).fetchone()          
                    print(cursor[1])
                    msg_output = "TROBLE " + cursor[1] + "# #" + Cname + "# #" + "Comment successfully.\r\n"
                    SEND(CMD = msg_output)



        ## mail to
        if msg_input.startswith("mail-to "):         
            if len(msg_split) > 5 and SUBJECT in msg_input and CONTENT in msg_input:                                        
                no_mt = msg_input.replace("mail-to ", "", 1)
                if login == -1:
                    msg_output = "ERR " + "Please login first."
                    SEND(CMD = msg_output)
                elif msg_split[1] == "subject":
                    print("He did not choose the receiver")
                elif msg_split[3] == "--content":
                    print("He did not name the title")
                else:
                    UNameSub = no_mt.split(" --subject ")
                    Receiver = UNameSub[0] ## receiver 
                    SubContent = UNameSub[1].split(" --content ")
                    Subject = SubContent[0]

                    print("Receiver is : ", Receiver, " Subject is : ", Subject, "Content is : ", SubContent[1])
                    cursor = c.execute('SELECT * FROM USERS WHERE Username = ?', (Receiver,)).fetchone()
                    if cursor == None: #Receiver is not exist
                        print("Receiver is not exist")
                        msg_output = "ERR " + Receiver + "  does not exist."
                        SEND(CMD = msg_output)
                    else:
                        print("Receiver exist")
                        Rid = cursor[0]
                        RBucket = cursor[4]
                        Mnum = cursor[5] + 1
                        ## get receiver info
                        NowTime = time.strftime("%m/%d", time.localtime()) ## is a string
                        
                        cursor = c.execute('INSERT INTO MAILS ("Subject", "DT", "Sender", "Receiver", "Mnum") VALUES (?, ?, ?, ?, ?)', (Subject, NowTime, login, Rid, Mnum))
                        cursor = c.execute('UPDATE USERS SET Mnum = ? WHERE UID = ?', (Mnum, Rid))
                        conn.commit()
                        ## get MID to create M{}
                        Last_mail = c.execute('SELECT * FROM MAILS WHERE Sender = ?', (login,)).fetchall()
                        MID = str(Last_mail[-1][0])
                        print(NowTime, "Sent successfully.")
                        msg_output = "TROBLE " + MID + "# #" + RBucket + "# #" + "Sent successfully."
                        SEND(CMD = msg_output)



        ## list the mail
        if msg_input == "list-mail": 
            print("Want to list ", login, " s mail")
            if login == -1:
                msg_output = "ERR " + "Please login first."
                SEND(CMD = msg_output)
            else:
                print("list")
                msg_output = "DATA "
                iter_mail = 0
                for row in c.execute("SELECT MAILS.Subject, USERS.Username, MAILS.DT FROM MAILS INNER JOIN USERS ON MAILS.Receiver=USERS.UID WHERE MAILS.Receiver = ? and MAILS.Mnum = ?", (login, )).fetchone():
                    iter_mail = iter_mail + 1
                    print("{:>5} {:^20} {:^20} {:^9}".format(iter_mail, row[0], row[1], row[2]))
                    msg_output = msg_output + "{:>7} {:^20} {:^20} {:^9}\r\n\r\n".format(iter_mail, row[0], row[1], row[2])
                SEND(CMD = msg_output)



        ## delete the mail
        if len(msg_split) == 2 and msg_split[0] == "delete-mail":
            if login == -1:
                msg_output = "ERR " + "Please login first."
            else:
                cursor = c.execute("SELECT * FROM MAILS WHERE Receiver = ?", (login, )).fetchall()
                if cursor == None:
                    print(cursor, "No such mail.")
                    msg_output = "ERR " + "No such mail."
                else:
                    MID = cursor[int(msg_split[1]) - 1][0]
                    cursor = c.execute('DELETE FROM MAILS WHERE MID = ?', (MID,))
                    conn.commit()
                    print("POST delete is success")
                    msg_output = "SUC " + "Delete successfully."
            SEND(CMD = msg_output)

        ## retr mail
        if len(msg_split) == 2 and msg_split[0] == "retr-mail":
            if login == -1:
                msg_output = "ERR " + "Please login first."
            else:
                cursor = c.execute("SELECT MAILS.MID, MAILS.Subject, USERS.Username, MAILS.DT FROM MAILS INNER JOIN USERS ON MAILS.Sender=USERS.UID WHERE MAILS.Receiver = ? and MAILS.Mnum = ?", (login, msg_split[1])).fetchone() 

                if cursor == None:
                    print(cursor, "No such mail.")
                    msg_output = "ERR " + "No such mail."
                else:
                    print(cursor[0], cursor[1], cursor[2], cursor[3]) ##cursor[0] is MID
                    msg_output = "TROBLE " + str(cursor[0]) + "# #" + "Subject   : {:>20} \r\nFROM      : {:>20} \r\nDate      : {:>20}\r\n--\r\n".format(cursor[1], cursor[2], cursor[3])
            SEND(CMD = msg_output)



        ## Command not found
        if msg_input.startswith("register"):
            msg_Usage = "Usage: register <username> <email> <password>"
        elif msg_input.startswith("login"):
            msg_Usage = "Usage: login <username> <password>"
        elif msg_input.startswith("whoami"):
            msg_Usage = "Usage: whoami"
        elif msg_input.startswith("logout"):
            msg_Usage = "Usage: logout"
        elif msg_input.startswith("exit"):
            msg_Usage = "Usage: exit"
        elif msg_input.startswith("create-board"):
            msg_Usage = "Usage: create-board <borad-name>"
        elif msg_input.startswith("list-board"):
            if hashtag in msg_input:
                msg_Usage = "Usage: list-board ##<key>"
            else:
                msg_Usage = "Usage: list-board"
        elif msg_input.startswith("create-post"):
            msg_Usage = "Usage: create-post <board-name> --title <title> --content <content>"
        elif msg_input.startswith("list-post"):
            if hashtag in msg_input:
                msg_Usage = "Usage: list-post <board-name> ##<key>"
            else:
                msg_Usage = "Usage: list-post <board-name>"
        elif msg_input.startswith("read"):
            msg_Usage = "Usage: read <post-id>"
        elif msg_input.startswith("delete-post"):
            msg_Usage = "Usage: delete-post <post-id>"
        elif msg_input.startswith("update-post"):
            msg_Usage = "Usage: update-post <post-id> --title/content <new>\r\n"        
        elif msg_input.startswith("comment"):
            msg_Usage = "Usage: comment <post-id> <comment>" 
        else:
            msg_Usage = "Command not found"


        if msg_output == "":
            msg_Usage = "USAGE " + msg_Usage
            ClientSocket.send(msg_Usage.encode('utf-8'))
            msg_Usage = ""
        msg_output = ""


bind_ip = "0.0.0.0"
bind_port = 1031

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(17)
print ("[*] Listening on  ", bind_ip,  bind_port)

while True:
    client,addr = server.accept()
    print ("New connection :", addr)
    _thread.start_new_thread(Client_Work, (client, addr))
