import socket
import sys
'''
1.5) Python Journeyman: Write a Python server which:
	receives a connection from the included client (JourneymanFinal.py)
	stores received data in a file, then adds the file to a list
	returns the data from the file when requested
	deals with errors and missing files
'''

class datasave:
	def __init__(self, name = '', data = ''):
		self.name = name
		self.data = data
		return



def loaddata(connection, fname):
	fobj = file(fname, 'r+')
	data = fobj.read()
	print "%s: \t %s" % (fname, data)
	connection.send(fobj.read())
	fobj.close()
	connection.close()
	return

def savedata(connection):
	fname = connection.recv(5)
	fobj = file(fname, 'w+')
	data = connection.recv(1024)
	print "%s: \t %s" % (fname, data)
	fobj.write(data)
	fobj.close()
	connection.close()
	return fname

def main():
	HOST = ''
	PORT = 50002
	sentinel = False
	opts_list = ["SAVE", "LOAD"]
	file_list = []
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		print "Connected to host: %s on port: %s" % (HOST, PORT)
	except socket.error, msg:
		sys.stderr.write("[ERROR] %s\n" % msg[1])
		sys.exit(1)
	while(sentinel != True):
		print "Listening on socket"
		s.listen(1)
		connection, address = s.accept()
		print "Connection: %s" % (connection)
		print "Addresse: %s" % str(address)
		data = connection.recv(4)
		print "data: %s" %(data)

		if data == opts_list[0]:
			file_list.append(savedata(connection))

		elif data == opts_list[1]:
			fname = data
			if fname not in file_list:
				connection.send("File not found")
				connection.close()
			loaddata(connection, fname)
		else:
			print data
			sentinel = True
	try:
		print "Debug #1"
		s.close()
	except socket.error, msg:
		sys.stderr.write("[ERROR] %s\n" % msg[1])
		sys.exit(1)


main()
