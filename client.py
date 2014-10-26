import socket
import select
import sys

socklist = []
port = 8000
host=socket.gethostname()

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

cs.connect((host, 8000))

socklist.append(cs)
socklist.append(sys.stdin)

def prompt():
   sys.stdout.write('CLIENT > ')
   sys.stdout.flush()

print ('* * * CONNECTED TO SERVER * * *')
prompt()

while 1:

    
    r_sock, wr_sock, err_sock = select.select(socklist, [], [])

    for sock in r_sock:
        if sock == cs:
            data = sock.recv(4096)
            if not data:
                print ('\nDisconnected from chat server')
                sys.exit()
            else:
                sys.stdout.write('\r'+data)
                prompt()
        else:
            msg = sys.stdin.readline()
            cs.send('\rCLIENT > ' + msg)
            prompt()
