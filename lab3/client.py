import socket


def CmdLine():
    cmd = input("% ")
    while cmd == "":
        cmd = input("% ")
    s.send(cmd.encode('utf-8'))
    return cmd


def INT_handling(int_msg):
    int_msg = int_msg.replace("int80 ", "", 1)
    print (int_msg)
    




HOST = '34.201.243.85'
PORT = 1031

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

welcome = s.recv(1024).decode('utf-8')
print (welcome)



Get_Input = 1

get = "" ## get is return msg from server
for i in range(10):
     ## .decode('utf-8'))
    if get.startswith("int80 "): ## print suc/err msg
        INT_handling(get)
        Get_Input = 1


    # elif cmd.startswith("register "):
    if Get_Input == 1:
        cmd = CmdLine()
        Get_Input = 0

    if cmd == "exit":
    	break
    get = s.recv(1024).decode('utf-8')
    print ("server send :  ", get)


