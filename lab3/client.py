import socket





def Error_handling(Error_msg):
    Err_msg = Error_msg.replace("ERROR ", "", 1)
    print (EErr_msg)
    cmd = input("% ")
    s.send(cmd.encode('utf-8'))
    get = s.recv(1024).decode('utf-8')
    return get

def Success_handling(Success_msg):
    Suc_msg = Success_msg.replace("SUC ", "", 1)
    print (Suc_msg)
    cmd = input("% ")
    s.send(cmd.encode('utf-8'))
    get = s.recv(1024).decode('utf-8')
    return get


#HOST = '54.198.148.205'
PORT = 1031

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
cmd = input("% ")
s.send(cmd.encode('utf-8'))
get = s.recv(1024).decode('utf-8')
while True:
    print ("server send :  ", get) ## .decode('utf-8'))
    if get.startswith("ERROR "):
        cmd = Error_handling(get)
    elif get.startswith("SUC "):
    	cmd = Success_handling(get)
    # elif cmd.startswith("register "):





    cmd = get


