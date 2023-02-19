import socket
import threading
import sys 
import argparse


#TODO: Implement all code for your server here


# Use sys.stdout.flush() after print statemtents

#Global Client list
clientList = []
lock = threading.Lock()

def receivingMes(socket):
	while True:
		text = socket.recv(100).decode()
		if len(text) >= 100:
			break
	return text.strip()

#Parse Command Line Arguments
def parseCLA():
	parser = argparse.ArgumentParser()
	parser.add_argument('port',type=int)
	parser.add_argument('passcode') #if no type specified, it is a string
	args = parser.parse_args()
	return args.port, args.passcode

#Check if passcode is valid
def check_passcode(passcode):
	if (len(passcode) > 5):
		return False
	return passcode.isalnum()

def start_server(portNum):
	#Get local host name
	host = socket.gethostname()
	server_socket = socket.socket()
	server_socket.bind((host, portNum))
	print("Server started on " + str(portNum) + ". Accepting Connections")
	sys.stdout.flush()
	return server_socket, host

def each_client(passcode, hostName, port, conn):
	login = receivingMes(conn)
	#print (str(conn) + " and "+ str(address))
	userInfo = login.split(" ")
	print(userInfo[0] + " and " + userInfo[1])
	sys.stdout.flush()
	if (passcode != userInfo[1]):
		print ("hello?")
		sys.stdout.flush()
		loginResponse = "Incorrect passcode"
		loginResponse = loginResponse.ljust(100, " ")
		conn.sendall(loginResponse.encode())
		conn.close()
		return
	else:
		print ("hiii")
		sys.stdout.flush()
		loginResponse = "Connected to " + hostName + " on port " + str(port)
		loginResponse = loginResponse.ljust(100, " ")
		conn.sendall(loginResponse.encode())

	lock.acquire()
	clientList.append(conn)
	lock.release()
	userName = userInfo[0]
	while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
		while True:
			data = conn.recv(100).decode()
			if (len(data) >= 100):
				break
		if not data:
            # if data is not received break
			
			break
		data = data.strip()
		if data == 'Exit':
			conn.close()
			endMessage = userName + " has left the chat"
			endMessage = endMessage.ljust(100, " ")
			lock.acquire()
			for client in clientList:
				if (client != conn):
					client.sendall(endMessage.encode())
			clientList.remove(conn)
			lock.release()
			break

		constText = "from " + userName + "(user): " + data
		constText = constText.ljust(100, " ")
		sys.stdout.flush()
		lock.acquire()
		for client in clientList:
			if (client != conn):
				client.sendall(constText.encode())
		lock.release()
		


def server_program(server_socket, passcode, hostName, port):
    # configure how many clients the server can listen simultaneously
	while True:
		server_socket.listen()
		conn, address = server_socket.accept()  # accept new connection
		t = threading.Thread(target=each_client, args=(passcode, hostName, port, conn))
		t.start()
	

if __name__ == "__main__":
	port, passcode = parseCLA()
	if (not check_passcode(passcode)):
		print ("Invalid Argument")
		exit()
	socket, hostName = start_server(port)
	server_program(socket, passcode,hostName, port)
