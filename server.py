import socket
import select
import sys

connlist = []
port = 8000
host=socket.gethostname()

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ss.bind((host, port))
ss.listen(5)

connlist.append(ss)
connlist.append(sys.stdin)


print ( 'SERVER STARTED WAITING FOR CLIENT TO CONNECT')


def prompt() :
    sys.stdout.write('SERVER > ')
    sys.stdout.flush()

while True:

    r_sock, w_sock, err_sock = select.select(connlist, [], []) 

    for sock in r_sock:
        if sock == ss:
            
            sockts, addr = ss.accept()
            connlist.append(sockts)
            print ('Clinet (%s, %s) connected ' % addr)
	    prompt()
           
        elif sock == sys.stdin:
	
	    prompt() 
            msg = sys.stdin.readline()
            
	    for i in connlist:
	        if i == sockts:
                    sockts.send('SERVER > '+msg)            
        else:

            try:                
                data = sock.recv(1024)		
                if data:		    
                    print (data)
                    prompt()
            except:                
                print ("Client (%s, %s) is offline" % addr)
                sock.close()
                connlist.remove(sock)
                continue
