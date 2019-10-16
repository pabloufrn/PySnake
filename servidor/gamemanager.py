import json
import socket
import select
import time
from random import randint
from entities import *

WAITING = 0
STARTED = 1
ENDED = 2

class GameManager:
	#initializing
	def __init__(self):
		self.players = []
		self.game_state = WAITING
		self.load_config()
		self.apple_pos = self.get_random_valid_position()
		self.load_socket()
		self.play()

	def get_random_valid_position(self):
		x = randint(1, self.board_width-1)
		y = randint(1, self.board_height-1)
		invalid = False
		for _ in range(0, (self.board_width-1)*(self.board_height-1)-1):
			for player in self.players:
				invalid = False
				if((x, y) in player.snake):
					if(x == self.board_width-2):
						x = 0
						if(y == self.board_height-2):
							y = 0
						else:
							y += 1
					else:
						x += 1
					invalid = True
					break
				if(invalid == False):
					break
		if(invalid):
			pass # todo: não conseguiu achar uma posição aleatória válida
		return (x, y)

	def spawn_player(self, playerid):
		player = self.players[playerid]
		pos = self.get_random_valid_position()
		player.snake = []
		for _ in range(self.min_player_size):
			player.snake.append(pos)

	def log_event(self, eventbytes):
		print(eventbytes.decode())

	def send_event_to_all(self, dictjson):
		for player in self.players:
			player.send_message(json.dumps(dictjson))

	def send_event_to_player(self, playerid, dictjson):
		self.players[playerid].send_message(json.dumps(dictjson))

	def load_config(self):
		with open('config.json', 'r') as f:
			config = json.load(f)
			self.hostname = config["hostname"]
			self.port = config["port"]
			self.board_width = config["board_width"]
			self.board_height = config["board_height"]
			self.max_players = config["max_players"]
			self.max_apples = config["max_apples"]
			self.min_player_size = config["min_player_size"]
			self.max_player_size = config["max_player_size"]
			self.apple_spawn_rate = config["apple_spawn_rate"]

	def load_socket(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.hostname, self.port))
		self.socket.listen(self.max_players)
		self.socket.setblocking(0)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def play(self):
		read_list = []
		try:
			read_list.append(self.socket)
			while True :
				readable, writeable, error = select.select(read_list,[],[])
				for sock in readable:
					if sock is self.socket:
						conn, info = sock.accept()
						read_list.append(conn)
						print("connection received from ", info)
						strplayerid = str(len(self.players))
						self.players.append(Player(conn, info))
						conn.send(strplayerid.encode())
					else:
						data = sock.recv(1024)
						if data:
							self.process_event(data.decode())
						else:
							sock.close()
							read_list.remove(sock)
		except Exception as e:
			raise e
			# print(e)
			# self.socket.close()
			# exit()

	def process_event(self, eventstr):
		try:
			event = json.loads(eventstr)
		except Exception:
			print(f"json invalido recebido:\n{eventstr}")
			return
		if(event["eventname"] == "setup"):
			player = self.players[event["playerid"]]
			player.name = event["playername"]
			self.spawn_player(event["playerid"])
			# player.body = self.get_random_body()
			jsondict = dict()
			jsondict["eventname"] = "setup"
			# jsondict["player"] = self.players
			jsondict["height"] = self.board_height
			jsondict["width"] = self.board_width
			jsondict["appleposition"] = self.apple_pos
			jsondict["snakes"] = [player.snake for player in self.players]
			print(json.dumps(jsondict))
			self.send_event_to_player(event["playerid"], jsondict)
		else:
			print("evento não definido.")
			jsondict = dict()
			jsondict["eventname"] = "setup"
			jsondict["errordesc"] = "invalid json sent."
			self.send_event_to_player(event["playerid"], jsondict)
			#lembrete
			'''para verificar se ela está morta, é necessário 
			verificar se a proxima parte do corpo também colide'''


''' Lista de coisas para fazer
- Carregar configuração do servidor e enviar para o cliente.
- Receber a configuração no cliente e exibir o jogo.
- Processar um evento de movimento no servidor
- Enviar evento de movimento
	- receber o estado do jogo e atualizar
'''

''' exemplos de json
Setup (enviador pelo cliente):
{
	"eventname": "setup"
	"playername": "teste"
}
Setup (enviador pelo server):
{
	"eventname": "setup"
	"playerid": 0,
	"height": 20,
	"width": 30 
}

'''