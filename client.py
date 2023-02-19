import socket
import threading
import sys 
import argparse

#TODO: Implement a client that connects to your server to chat with other clients here

lock = threading.Lock()
# Use sys.stdout.flush() after print statemtents
def parseCLA():
	parser = argparse.ArgumentParser()
	parser.add_argument('host')
	parser.add_argument('port',type=int)
	parser.add_argument('username')
	parser.add_argument('passcode')
	args = parser.parse_args()
	return args.host, args.port, args.username, args.passcode

def paddingString(text):
	return text.ljust(100, " ").encode()

def sendMessage(socket, text):
	socket.sendall(paddingString(text))


def receivingMes(socket):
	while True:
		text = socket.recv(100).decode()
		if len(text) >= 100:
			break
	return text.strip()

def printToClient(socket):
	try:
		while True:
			while True:
				text = socket.recv(100).decode()
				if len(text) >= 100:
					break
			print (text.strip())
			sys.stdout.flush()
	except:
		return


def client_program(host, port, username, passcode):
	
	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server
	login = username + " " + passcode #construct username and passcode
	response = sendMessage(client_socket, login)
	print (response)
	if (response == "Incorrect passcode"):
		client_socket.close()
		return

	t = threading.Thread(target=printToClient, args=[client_socket])
	t.start()
	while True:
		text = input()  # take input
		sendMessage(client_socket, text)
		if (text == 'Exit'):
			client_socket.close()
			break

	#client_socket.close()   close the connection


if __name__ == '__main__':
	host, port, username, passcode = parseCLA()
	client_program(host, port, username, passcode)