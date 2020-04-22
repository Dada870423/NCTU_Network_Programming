import socket


def CmdLine():
    cmd = input("% ")
    s.send(cmd.encode('utf-8'))
    return cmd


def INT_handling(int_msg):
    int_msg = int_msg.replace("int80 ", "", 1)
    print (Err_msg)
    




HOST = '34.201.243.85'
PORT = 1031

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

get = s.recv(1024).decode('utf-8')
print ("server send :  ", get)
cmd = CmdLine()
get = s.recv(1024).decode('utf-8')
print ("server send :  ", get)
for i in range(10):
    print ("server send :  ", get) ## .decode('utf-8'))
    if get.startswith("int80 "): ## print suc/err msg
        INT_handling(get)


    # elif cmd.startswith("register "):
    cmd = CmdLine()

    if cmd.upper() == "EXIT":
    	break
    get = s.recv(1024).decode('utf-8')
    get = cmd


