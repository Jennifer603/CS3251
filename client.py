import socket
import threading
import sys 
import argparse
import random

#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents
def parseCLA():
	parser = argparse.ArgumentParser()
	parser.add_argument('host')
	parser.add_argument('port',type=int)
	parser.add_argument('username')
	parser.add_argument('passcode')
	args = parser.parse_args()
	return args.host, args.port, args.username, args.passcode


def client_program(host, port, username, passcode):
	
	client_socket = socket.socket()  # instantiate
	print(socket.gethostname())
	client_socket.connect((host, port))  # connect to the server
	login = username + " " + passcode #construct username and passcode
	client_socket.send(login.encode())
	response = client_socket.recv(1024).decode()
	print (response)
	if (response == "Incorrect passcode"):
		client_socket.close()
		return

	text = input(" -> ")

	while True:
		client_socket.send(text.encode())  # send message
		response = client_socket.recv(1024).decode()  # receive response

		print('Received from server: ' + response)  # show in terminal
		sys.stdout.flush()
		text = input(" -> ")  # take input
		if (text.lower().strip() == 'exit'):
			client_socket.send(text.encode())
			break

	client_socket.close()  # close the connection


if __name__ == '__main__':
	host, port, username, passcode = parseCLA()
	client_program(host, port, username, passcode)