import socket
import threading
import sys 
import argparse


#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents


def client_program():
	

	host = socket.gethostname()  # as both code is running on same pc
	port = 5000  # take input to initiate port

	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server

	message = input(" -> ")  # take input

	while message.lower().strip() != 'Exit':
		client_socket.send(message.encode())  # send message
		data = client_socket.recv(1024).decode()  # receive response

		print('Received from server: ' + data)  # show in terminal

		message = input(" -> ")  # again take input

	client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()