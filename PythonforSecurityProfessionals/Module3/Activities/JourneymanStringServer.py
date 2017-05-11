import socket



def main():
    HOST  = '127.0.0.1'
    PORT  = 50001
    message_list = ['alpha' , 'bravo' , 'charlie' , 'delta']
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    s.bind((HOST , PORT))
    print "HOST: %s" % (HOST)
    print "socket is binded to %s" %(PORT)
    for i in message_list:

        s.listen(1)
        conn, addr = s.accept()
        conn.send(i)
    	conn.close()
        
main()
