import socket
import os
import boto3
import time



POS = "POS"
NEG = "NEG"
target_bucket = None
board_Col_name = "{:^7} {:^20} {:^20} \r\n".format("Index", "Name", "Moderator")
post_Col_name = "{:^7} {:^20} {:^20} {:^9}\r\n".format("ID", "Title", "Author", "Date")

s3 = boto3.resource('s3')

def MKDIR():
    Pdata = "./.data"
    Ppost = "./.data/post"
    Pcomment = "./.data/comment"

    try:
      os.makedirs(Pdata)
      os.makedirs(Ppost)
      os.makedirs(Pcomment)
    except FileExistsError:
      return

def RECEIVE():
    while True:
        try:
            msg_in = s.recv(1024).decode('utf-8')
            return msg_in
        except:
            pass    

def SEND(CMD):
    while True:
        try:
            s.send(CMD.encode('utf-8'))
            break
        except:
            pass



def INT_handling(int_msg):
    response = -1
    if int_msg.startswith("SUC"):
    	int_msg = int_msg.replace("SUC ", "", 1)
    	response = 0
    elif int_msg.startswith("ERR"):
    	int_msg = int_msg.replace("ERR ", "", 1)
    	response = 1
    elif int_msg.startswith("USAGE"):
    	int_msg = int_msg.replace("USAGE ", "", 1)
    	response = 2
    elif int_msg.startswith("POS"):
    	return 3, int_msg
    elif int_msg.startswith("NEG"):
    	return 4, int_msg
    elif int_msg.startswith("DATA"):
        int_msg = int_msg.replace("DATA ", "", 1)
        response  = 5
    elif int_msg.startswith("TROBLE"):
        int_msg = int_msg.replace("TROBLE ", "", 1)
        return 6, int_msg

    print(int_msg)
    return response, int_msg

    


def CmdLine():
    cmd = input("% ")
    test = cmd.replace(' ', '')
    while test == "":
        cmd = input("% ")
        test = cmd.replace(' ', '')
    SEND(CMD = cmd)
    return cmd



def CBucketName():
    ti = str(time.time())
    BucketName = "netprolab3qsefthuk" + ti
    return BucketName


def REG(CMD):
    get = RECEIVE()
    response, trash = INT_handling(int_msg = get)
    if response == 3:
        BucketName = CBucketName()
        s3.create_bucket(Bucket = BucketName)
        SEND(CMD = BucketName)
        get = RECEIVE()
        INT_handling(int_msg = get)  
    else:
        pass
   



def LOGIN(CMD):
    get = RECEIVE()	
    response, BWN = INT_handling(int_msg = get)
    if response == 6:
        LoginHandling(BWN = BWN)

def LoginHandling(BWN):
    BN_WEL = BWN.split("# #") 
    BucketName = BN_WEL[0]
    WelcomeName = BN_WEL[1]
    print(WelcomeName)
    global target_bucket
    target_bucket = s3.Bucket(BucketName)
    return BucketName



def WHOAMI(CMD):
    get = RECEIVE()
    INT_handling(int_msg = get)


def LOGOUT(CMD):
    get = RECEIVE()
    INT_handling(int_msg = get)
    target_bucket = None


def CBOARD(CMD):
    get = RECEIVE()
    INT_handling(int_msg = get)


def LBOARD(CMD):
    print(board_Col_name)
    get = RECEIVE()
    INT_handling(int_msg = get)

def LPOST(CMD):
    print(post_Col_name)
    get = RECEIVE()
    INT_handling(int_msg = get)


def Get_BTC(CMD):
    CMD = CMD.replace("create-post ", "", 1) 
    BoardTitle = CMD.split(" --title ")                   
    TitleContent = BoardTitle[1].split(" --content ")
    Board = BoardTitle[0]
    Title = TitleContent[0]
    Content = TitleContent[1]
    return Board, Title, Content


def CPOST(CMD):
    get = RECEIVE()
    response, PidSMsg = INT_handling(int_msg = get)
    
    if response == 6:
        PidSMsg = PidSMsg.split("# #")
        PID = PidSMsg[0]
        print(PidSMsg[1])
        print("PID is : ", PID)
        Board, Title, Content = Get_BTC(CMD = CMD)
        cnt = Content.split("<br>")
        for iter_cnt in cnt:
            print(iter_cnt)
            os.system("echo {} >> ./.data/post/P{}".format(iter_cnt, PID))
        ## S3
        target_bucket.upload_file("./.data/post/P{}".format(PID), "P{}".format(PID))

        ## S3 done








HOST = '3.84.34.171'
PORT = 1031

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.setblocking(0)
MKDIR()


welcome = RECEIVE()
print (welcome)



get = "" ## get is return msg from server
while True:
    cmd = CmdLine()


    if cmd == "exit":
    	break
    elif cmd.startswith("register"):
        REG(CMD = cmd)
    elif cmd.startswith("login"):
        LOGIN(CMD = cmd)
    elif cmd.startswith("whoami"):
        WHOAMI(CMD = cmd)
    elif cmd.startswith("logout"):
        LOGOUT(CMD = cmd)
    elif cmd.startswith("create-board"):
        CBOARD(CMD = cmd)
    elif cmd.startswith("list-board"):
        LBOARD(CMD = cmd)
    elif cmd.startswith("create-post"):
        CPOST(CMD = cmd)
    elif cmd.startswith("list-post"):
        LPOST(CMD = cmd) 
    else:
        get = RECEIVE()
        INT_handling(int_msg = get)

























