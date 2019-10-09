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
	players = []
	while True :
		readable, writeable, error = select.select(read_list,[],[])
		for sock in readable:
			if sock is s:
				conn, info = sock.accept()
				read_list.append(conn)
				print("connection received from ", info)
				strplayerid = str(len(players))
				players.append(Player(info))
				conn.sendall(strplayerid.encode("utf-8"))
			else:
				data = sock.recv(1024)
				if data:
					# conn.id.pablo
					# move.id.up
					# die
					# maca.10,10
					cmd, playerid, arg = data.decode("utf-8").split(".")
					playerid = int(playerid)
					if(cmd == "conn"):
						players[playerid].name = arg
						msg = f"Jogador {arg} conectado."
						send_message_to_all(read_list, msg.encode("utf-8"))
					elif(cmd == "move"):
						print(f"Jogador {players[playerid].name} se moveu para {arg}.")
				else:
					sock.close()
					read_list.remove(sock)
#
		
def send_message_to_all(conns, message):
	for conn in conns:
		conn.send(message)