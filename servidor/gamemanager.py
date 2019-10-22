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
		self.apples = []
		self.load_socket()
		self.play()

	def get_random_valid_position(self):
		x = randint(1, self.board_width-1)
		y = randint(1, self.board_height-1)
		invalid = False
		for _ in range(0, (self.board_width-1)*(self.board_height-1)-1):
			for player in self.players:
				if(player == None):
					continue
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
		player.spawn(pos, self.min_player_size)

	def send_event_to_all(self, dictjson):
		for player in self.players:
			if(player):
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
		timer = time.time()
		update_timer = time.time()
		time_timer = time.time()
		now = 0
		iostart = 0
		iototal = 0
		pstotal = 0
		try:
			read_list.append(self.socket)
			while True :
				now = time.time() 
				if(now - timer > self.apple_spawn_rate):
					timer = now 
					if(len(self.apples) < self.max_apples):
						self.apples.append(self.get_random_valid_position())
					pstime = time.time() - now 
					pstotal += pstime
				if(now - update_timer > 0.1):
					iotime = now - iostart
					iototal += iotime
					update_timer = now 
					self.update_game()
					pstime = time.time() - now 
					pstotal += pstime
					iostart = time.time()
					self.send_game_state()
					iotime = time.time() - iostart 
					iototal += iotime
				elif(iostart != 0):
					iotime = now - iostart
					iototal += iotime
				if(time.time() - time_timer > 5):
					print(iototal, pstotal)
					iototal = 0 
					pstotal = 0
					time_timer = time.time()
				iostart = time.time()
				readable, writeable, error = select.select(read_list,[],[], 0)
				for sock in readable:
					if sock is self.socket:
						conn, info = sock.accept()
						read_list.append(conn)
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
			self.socket.close()
			exit()

	def process_event(self, eventstr):
		try:
			event = json.loads(eventstr)
		except Exception:
			print(f"json invalido recebido:\n{eventstr}")
			return
		player = self.players[event["playerid"]]
		if(event["eventname"] == "setup"):
			player.name = event["playername"]
			self.spawn_player(event["playerid"])
			# player.body = self.get_random_body()
			jsondict = dict()
			jsondict["eventname"] = "setup"
			jsondict["height"] = self.board_height
			jsondict["width"] = self.board_width
			self.send_event_to_player(event["playerid"], jsondict)
		elif(event["eventname"] == "move"):
			mdir = event["dir"]
			if(	(mdir == "up" and player.last_move == "down")) or \
				(mdir == "down" and player.last_move == "up") or \
				(mdir == "left" and player.last_move == "right") or \
				(mdir == "right" and player.last_move == "left"):
				pass
			else:
				player.next_move = mdir
		elif(event["eventname"] == "exit"):
			self.player.conn.close()
			self.players[playerid] = None
		else:
			print("evento não definido.")
			jsondict = dict()
			jsondict["eventname"] = "setup"
			jsondict["errordesc"] = "invalid json sent."
			self.send_event_to_player(event["playerid"], jsondict)
        #lembrete
		'''para verificar se ela está morta, é necessário 
		verificar se a proxima parte do corpo também colide'''
	def update_game(self):
		for player in self.players:
			if(player):
				player.move(self.board_width, self.board_height)
		# checar se comeu a maça
		for player in self.players:
			if(player == None):
				continue
			for apple in self.apples:
				if(player.try_eat(apple)):
					self.apples.remove(apple)
		# checar se o player colidiu com alguém
		deads = []
		for playeroneid, playerone in enumerate(self.players):
			if(playerone == None or len(playerone.snake) == 0):
				continue
			for playertwoid, playertwo in enumerate(self.players):
				if(playertwo == None or len(playerone.snake) == 0):
					continue
				elif(playeroneid == playertwoid):
					if(len(playerone.snake) > 4 and playerone.snake[0] in list(playerone.snake)[4:]):
						deads.append(playeroneid)
				else:
					if(playerone.snake[0] in playertwo.snake):
						deads.append(playeroneid)
		for dead in deads:
			for body_part in self.players[dead].snake:
				self.apples.append(body_part)
			event = {'eventname': 'die'}
			self.players[dead].send_message(json.dumps(event))
			self.players[dead].spawn(0, 0)


	def send_game_state(self):
		game_state = dict()
		game_state["eventname"] = "update"
		game_state["snakes"] = [list(player.snake) if player else [] for player in self.players]
		game_state["apples"] = self.apples
		game_state["scoreboard"] = [[player.name,player.score] for player in self.players if player]
		for player in self.players:
			if(player and player.name):
				player.send_message(json.dumps(game_state))

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