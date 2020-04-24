import socket
import os



POS = "POS"
NEG = "NEG"
board_Col_name = "{:^7} {:^20} {:^20} \r\n\r\n".format("Index", "Name", "Moderator")
post_Col_name = "{:^7} {:^20} {:^20} {:^9}\r\n\r\n".format("ID", "Title", "Author", "Date")



def MKDIR():
    Fdata = "./.data"
    Fpost = "./.data/post"
    Cpost = "./.data/comment"

    try:
      os.makedirs(Fdata)
      os.makedirs(Fpost)
      os.makedirs(Cpost)
    except FileExistsError:
      return







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
    	return 3
    elif int_msg.startswith("NEG"):
    	return 4
    elif int_msg.startswith("DATA"):
        int_msg = int_msg.replace("DATA ", "", 1)
        response  = 5
    print(int_msg)
    return response

    


def CmdLine():
    cmd = input("% ")
    test = cmd.replace(' ', '')
    while test == "":
        cmd = input("% ")
        test = cmd.replace(' ', '')
    s.send(cmd.encode('utf-8'))
    return cmd


def REG(CMD):
    get = s.recv(1024).decode('utf-8')
    response = INT_handling(int_msg = get)
    if response == 1:
    	gogo_S3 = 1
    	## S3


        ## S3 done
    else:
    	gogo_S3 = 0



def LOGIN(CMD):
    get = s.recv(1024).decode('utf-8')	
    response = INT_handling(int_msg = get)
    if response == 1:
    	gogo_S3 = 1
    	## S3


        ## S3 done
    else:
    	gogo_S3 = 0


def WHOAMI(CMD):
    get = s.recv(1024).decode('utf-8')
    response = INT_handling(int_msg = get)


def LOGOUT(CMD):
    get = s.recv(1024).decode('utf-8')
    response = INT_handling(int_msg = get)

def CBOARD(CMD):
    get = s.recv(1024).decode('utf-8')
    response = INT_handling(int_msg = get)
    if response == 3:
        gogo_S3 = 1
    	## S3


        ## S3 done
        if True:
    	    s.send(POS.encode('utf-8'))
        get1 = s.recv(1024).decode('utf-8')
        response1 = INT_handling(int_msg = get1)



def LBOARD(CMD):
    print(board_Col_name)
    FLAG = 5
    while FLAG == 5:
        get = s.recv(1024).decode('utf-8')
        FLAG = INT_handling(int_msg = get)





HOST = '52.87.247.141'
PORT = 1031

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

MKDIR()


welcome = s.recv(1024).decode('utf-8')
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
    else:
        get = s.recv(1024).decode('utf-8')
        INT_handling(int_msg = get)

























