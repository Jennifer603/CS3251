import socket
import threading
import sys 
import argparse


#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents




def server_program():
	parser = argparse.ArgumentParser()
	parser.add_argument('port',type=int)
	parser.add_argument('passcode',type=int)
	
	args = parser.parse_args()

    # get the hostname
	host = socket.gethostname()
	port = args.port  # take input to initiate port
	passcode = args.passcode
	server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
	server_socket.bind((host, port))  # bind host address and port together



    # configure how many client the server can listen simultaneously
	server_socket.listen(2)
	conn, address = server_socket.accept()  # accept new connection
	
	
	print("Server started on " + str(port) + ". Accepting Connections")
	while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
		data = conn.recv(1024).decode()
		if not data:
            # if data is not received break
			
			break
		
		print("from " + "connected user: " + str(data))
		data = input(' -> ')
		conn.send(data.encode())  # send data to the client
		conn.close()  # close the connection

if __name__ == "__main__":
	server_program()
