#reference: https://realpython.com/python-sockets/

import socket
import time
import json

HOST = '10.7.109.10'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

player_name = input("Digite seu nome: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.connect((HOST, PORT))
    data = s.recv(1024)
    playerid = data.decode()
    #Envia o nome, o id e o evento ao servidor.
    dictplayer = {'playername':'nome1', 'playerid': playerid, 'eventname': 'setup'}
    s.sendall(json.dumps(dictplayer).encode())
    
    #Recebe evento, id, height e width.
    data = s.recv(1024)
    dictserver = json.loads(data.decode())

    #while(True):

    	

print('Received', repr(data))