import socket
import threading
import sys 
import argparse


#TODO: Implement all code for your server here


# Use sys.stdout.flush() after print statemtents

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
	return server_socket, host



def server_program(server_socket, passcode, hostName, port):
    # configure how many clients the server can listen simultaneously
	server_socket.listen()
	conn, address = server_socket.accept()  # accept new connection
	login = conn.recv(1024).decode()
	#print (str(conn) + " and "+ str(address))
	userInfo = login.split(" ")
	if (passcode != userInfo[1]):
		loginResponse = "Incorrect passcode"
		conn.send(loginResponse.encode())
	else:
		loginResponse = "Connected to " + hostName + " on port " + str(port)
		conn.send(loginResponse.encode())

	userName = userInfo[0]
	
	
	while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
		data = conn.recv(1024).decode()
		if not data:
            # if data is not received break
			
			break
		
		print("from " + userName + "(user): " + data)
		sys.stdout.flush()
		data = input(' -> ')
		conn.send(data.encode())  # send data to the client

if __name__ == "__main__":
	port, passcode = parseCLA()
	if (not check_passcode(passcode)):
		print ("Invalid Argument")
		exit()
	socket, hostName = start_server(port)
	server_program(socket, passcode,hostName, port)
