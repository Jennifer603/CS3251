import socket
import threading
import sys 
import argparse
import datetime

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
	parser = argparse.ArgumentParser(description='Start the server')
	parser.add_argument('-start', action='store_true', help='Start the server')
	parser.add_argument('-port',type=int, required=True, help='Port number for the server')
	parser.add_argument('-passcode', required=True, help='Passcode for the server') #if no type specified, it is a string
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
	print("Server started on port " + str(portNum) + ". Accepting connections")
	sys.stdout.flush()
	return server_socket, host

def send_to_all(text, conn):
	text = text.ljust(100, " ")
	for client in clientList:
		if (client != conn):
			client.sendall(text.encode())

def constructText(username, text):
	header = username + ": "
	now = datetime.datetime.now()
	if (text == ":)"):
		header += "[feeling happy]"
	elif (text == ":("):
		header += "[feeling sad]"
	elif (text == ":mytime"):
		#%a - abbreviated weekday, %A - full weekday, %m - full month, %b - abbreviated month
		formatedTime = now.strftime("%a %b %d %H:%M:%S %Y")
		header += str(formatedTime)
	elif (text == ":+1hr"):
		newTime = now + datetime.timedelta(hours=1)
		#%a - abbreviated weekday, %A - full weekday, %m - full month, %b - abbreviated month
		formatedNewTime = newTime.strftime("%a %b %d %H:%M:%S %Y")
		header += formatedNewTime
	else:
		header += text
	return header.ljust(100, " ")
def each_client(passcode, hostName, port, conn):
	#checking login
	login = receivingMes(conn)
	userInfo = login.split(" ")
	if (passcode != userInfo[1]):
		loginResponse = "Incorrect passcode"
		loginResponse = loginResponse.ljust(100, " ")
		conn.sendall(loginResponse.encode())
		conn.close()
		return
	else:
		loginResponse = "Connected to " + hostName + " on port " + str(port)
		loginResponse = loginResponse.ljust(100, " ")
		conn.sendall(loginResponse.encode())

	#if login correct
	userName = userInfo[0]
	lock.acquire()
	clientList.append(conn)
	welcome = userName + " joined the chatroom"
	send_to_all(welcome, conn)
	lock.release()
	print(welcome)
	sys.stdout.flush()

	
	while True:
        # receive data stream. it won't accept data packet greater than 100 bytes (100 chars)
		data = receivingMes(conn)
		if data == 'Exit':
			conn.close()
			endMessage = userName + " has left the chatroom"
			endMessage = endMessage.ljust(100, " ")
			lock.acquire()
			send_to_all(endMessage, conn)
			clientList.remove(conn)
			lock.release()
			break

		constText = constructText(userName, data)
		lock.acquire()
		send_to_all(constText, conn)
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
