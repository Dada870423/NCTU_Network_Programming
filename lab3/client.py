import socket


POS = "POS"
NEG = "NEG"


def INT_handling(int_msg):
    response = -1
    if int_msg.startswith("SUC"):
    	int_msg = int_msg.replace("SUC ", "", 1)
    	response = 0
    	print(int_msg)
    elif int_msg.startswith("ERR"):
    	int_msg = int_msg.replace("ERR ", "", 1)
    	response = 1
    	print(int_msg)
    elif int_msg.startswith("USAGE"):
    	int_msg = int_msg.replace("USAGE ", "", 1)
    	response = 2
    	print(int_msg)
    elif int_msg.startswith("POS"):
    	response = 3
    elif int_msg.startswith("NEG"):
    	response = 4
    return response

    


def CmdLine():
    cmd = input("% ")
    while cmd == "":
        cmd = input("% ")
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
        ### if s3 success then
    	###    s.send(POS.encode('utf-8'))
        get = s.recv(1024).decode('utf-8')
        response1 = INT_handling(int_msg = get)





HOST = '52.87.247.141'
PORT = 1031

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

welcome = s.recv(1024).decode('utf-8')
print (welcome)



Get_Input = 1

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
    else:
        get = s.recv(1024).decode('utf-8')
        INT_handling(int_msg = get)


