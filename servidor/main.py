import socket
import select
import time
import sys
from entities import Player

port = 65432
# todo: arquivo json de configuração

read_list = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

	s.setblocking(0)
	s.bind(('', port))
	s.listen(5)
	read_list.append(s)
	players = {}
	while True :
		readable, writeable, error = select.select(read_list,[],[])
		for sock in readable:
			if sock is s:
				conn, info = sock.accept()
				read_list.append(conn)
				print("connection received from ", info)
				players[info[0]] = None
			else:
				data = sock.recv(1024)
				if data:
					# conn.pablo
					# move.up

					# die
					# maca.10,10
					cmd, arg = data.decode("utf-8").split(".")
					if(cmd == "conn"):
						playername = data.decode("utf-8")
						players[info] = None
						print(f"Jogador {playername} conectado.")
						sock.send(data)
					elif(cmd == "move"):
						direction = data.decode("utf-8")
						print(f"Jogador se moveu para {direction}.")

				else:
					sock.close()
					read_list.remove(sock)

		
