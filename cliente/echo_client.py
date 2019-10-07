#reference: https://realpython.com/python-sockets/

import socket
import time

HOST = '10.7.104.10'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

player_name = input("Digite seu nome: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.connect((HOST, PORT))
    s.sendall(("conn." + player_name).encode("utf-8"))
    data = s.recv(1024)

    while(True):
    	time.sleep(1)
    	s.sendall(b"move.left")

print('Received', repr(data))