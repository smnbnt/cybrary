'''
The final activity for the Advanced Python section is a drive-wide FTP-like
tool. You should be able to receive multiple connections, each on their 
own thread. You should take several commands:
DRIVESEARCH <filename>
    DRIVESEARCH looks for the given filename across the entire drive. If
    it finds the file, it sends back the drive location.
DIRSEARCH <directory> <filename>
    DIRSEARCH looks for the file in the given directory or its 
    subdirectories. If it finds the file, it sends back the location.
DOWNLOAD <filename>
    DOWNLOAD requires the full file path, or at least the relative path,
    of the file. It sends the contents of the file across the network.
UPLOAD <filename>
    UPLOAD requires the full file path, or at least the relative path,
    where the user wants to locate the file. It reads the file contents
    from across the network connection.
CLOSE
    CLOSE ends the connection
    
This activity will require you to use multithreading, ctypes, regular
expressions, and some libraries with which you're unfamiliar. ENJOY!
'''

import os, re, threading, struct, sys, socket
from ctypes import *

def read_file(filename): #ctypes
	kernel32 = windll.LoadLibrary("kernel32")
	file_handle = kernel32.CreateFileA(filename, 0x10000000, 0, 0, 3, 0x80, 0)
	if (file_handle == -1):
		return -1
	data = create_string_buffer(4096)
	read_data = c_int(0)
	bool_success = kernel32.ReadFile(file_handle, byref(data), 4096, byref(read_data), 0)
	kernel32.CloseHandle(file_handle)
	if bool_success == 0:
		return -1
	return data.value

def create_file(filename, data): #ctypes
	kernel32 = windll.LoadLibrary("kernel32")
	file_handle = kernel32.CreateFileA(filename, 0x10000000, 0, 0, 2, 0x80, 0)
	if (file_handle == -1):
		return -1
	written_data = c_int(0)
	bool_success = kernel32.WriteFile(file_handle, data, len(data), byref(written_data), 0)
	kernel32.CloseHandle(file_handle)
	if bool_success == 0:
		return -1
	return

def recv_data(user_sock): #Implement a networking protocol
	data_len = struct.unpack("!I", user_sock.recv(4))
	return user_sock.recv(data_len)

def send_data(user_sock,data): #Implement a networking protocol
	data_len = len(data)
	user_sock.send(struct.pack("!I", data_len))
	user_sock.send(data)
	return

def search_drive(file_name): #DRIVESEARCH
	re_obj = re.compile(file_name)
	for root, dirs, files in os.walk("C:\\"):
		for file in files:
			if (re.search(re_obj, file))
				return os.path.join(root, file)
	return -1

def search_directory(file_name): #DIRSEARCH
    root, dirs, files = os.walk(os.getcwd())
    re_obj = re.compile(file_name)
    for file in files:
		if (re.search(re_obj, file)):
			return os.path.join(root, file)
    return -1

def send_file_contents(file_name,user_sock,userinfo): #DOWNLOAD
	if send_data(user_sock, read_file(file_name)) == -1:
		send_data(user_sock, "File sending failed")
	return

def receive_file_contents(file_name,user_sock):#UPLOAD
	if create_file(file_name, recv_data(user_sock)) == -1:
		send_data(user_sock, "File creation failed.")
	return

def handle_connection(user_sock,userinfo):
	command_list = ["DRIVESEARCH",
					"DIRSEARCH",
					"DOWNLOAD",
					"UPLOAD",
					"CLOSE"]
	continue_bool = True
	while(continue_bool):
		command = recv_data(user_sock).upper()

		if (command == "DRIVESEARCH"):
			send_data(user_sock, "Filename: ")
			search_result = search_drive(recv_data(user_sock))
			if search_result == -1:
				send_data(user_sock, "File not found.")
			else:
				send_data(user_sock, search_result)

		if (command == "DIRSEARCH"):
			send_data(user_sock, "Filename: ")
			search_result = search_drive(recv_data(user_sock))
			if search_result == -1:
				send_data(user_sock, "File not found.")
			else:
				send_data(user_sock, search_result)

		if (command == "DOWNLOAD"):
			send_data(user_sock, "Filename: ")
			search_drive(recv_data(user_sock), user_sock, userinfo)

		if (command == "UPLOAD"):
			send_data(user_sock, "Filename: ")
			search_drive(recv_data(user_sock), user_sock)

		if (command == "CLOSE"):
			continue_bool = False
			return
		else:
			send_data(user_sock, "INVALID COMMAND")
def main():

	try:
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind(('',55555))
	except socket.error, msg:
		sys.stderr.write("[ERROR] %s\n" % msg[1])
		sys.exit(1)

	while(True):
		server_socket.listen(8)
		user_sock, userinfo = server_socket.accept()
		conn_thread = threading.Thread(None, handle_connection, None, (user_sock, userinfo))
		conn_thread.start()
	return

main()
