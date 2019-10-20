import math
import pygame
import tkinter as tk
from tkinter import messagebox
import socket
import json
 
class cube(object):

	def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color
		global width, height, rows, columns
		self.w = width
		self.h = height
		self.rows = rows
		self.columns = columns
		
	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
	def draw(self, surface, eyes=False):
		disy = self.h // self.rows
		disx = self.w // self.columns
		i = self.pos[0]
		j = self.pos[1]
 
		pygame.draw.rect(surface, self.color, (i*disx+1,j*disy+1, disx-2, disy-2))
		# todo: calcular a posição dos olhos
		# if eyes:
			# centre = dis//2
			# radius = 3
			# circleMiddle = (i*dis+centre-radius,j*dis+8)
			# circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
			# pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
			# pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
 
class snake(object):
	def __init__(self):
		self.next_move = "up"
 
	def move(self, socket, playerid):
		send = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				socket.close()
				dictmove["eventname"] = "exit"
				socket.sendall(json.dumps(dictmove).encode())
				exit(0)
 
			keys = pygame.key.get_pressed()

			for key in keys:
				if keys[pygame.K_LEFT]:
					if(self.next_move == "left"):
						continue
					else: 
						send = True
						self.next_move = "left"
				elif keys[pygame.K_RIGHT]:
					if(self.next_move == "right"):
						continue
					else: 
						send = True
						self.next_move = "right"
 
				elif keys[pygame.K_UP]:
					if(self.next_move == "up"):
						continue
					else:
						send = True
						self.next_move = "up"
 
				elif keys[pygame.K_DOWN]:
					if(self.next_move == "down"):
						continue
					else:
						send = True
						self.next_move = "down"

		if(send):
			dictmove = {"eventname": "move", "playerid": playerid, "dir": self.next_move}
			socket.sendall(json.dumps(dictmove).encode())
			print(json.dumps(dictmove).encode())
 
def drawGrid(w, h, rows, columns, surface):
	sizeBtwny = w // rows
	sizeBtwnx = h // columns
	x = 0
	y = 0
	for l in range(rows):
		y = y + sizeBtwny
		pygame.draw.line(surface, (255,255,255), (0,y),(w,y))

	for c in range(columns):
		x = x + sizeBtwnx
		pygame.draw.line(surface, (255,255,255), (x,0),(x,h))
 
def redrawWindow(surface):
	global rows, columns, width, height, s, snack
	surface.fill((0,0,0))
	drawGrid(width, height, rows, columns, surface)
	pygame.display.update()
 
 
def message_box(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass
 
 
def main():
	global width, height, rows, columns
	player = snake()
	hostname = input("Digite o dóminio ou ip so servidor: ")
	playername = input("Digite o nome do jogador: ")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: 
		sock.connect((hostname, 65333))
		data = sock.recv(1024)
		playerid =int(data.decode())
		#Envia o nome, o id e o evento ao servidor.
		dictplayer = {'playername':playername, 'playerid': playerid, 'eventname': 'setup'}
		sock.sendall(json.dumps(dictplayer).encode())
		
		#Recebe evento, id, height e width.
		data = sock.recv(1024)
		dictserver = json.loads(data.decode())
		rows = dictserver["height"]
		columns = dictserver["width"]
		width = 600
		height = 600

		win = pygame.display.set_mode((width, height))
		flag = True
		print(width, height, rows, columns)
	 
		clock = pygame.time.Clock()
		sock.setblocking(0)
		redrawWindow(win)
		while flag:
			try:
				data = sock.recv(1024)
				game_state = json.loads(data.decode())

				#Quando o evento for update, adicionar todas as snakes pra lista e desenha-las.
				if(game_state["eventname"] == "update"):
					win.fill((0,0,0))
					drawGrid(width, height, rows, columns, win)
					for index, s in enumerate(game_state["snakes"]):
						if(index == playerid and s != []):
							for c in s:
								cube(tuple(c), color=(255,0,0)).draw(win)
						elif(s != []):
							for c in s:
								cube(tuple(c), color=(0,0,255)).draw(win)

					snack = cube(game_state["appleposition"], color=(0,255,0)).draw(win)
					pygame.display.update()
				# pygame.time.delay(50)
				# clock.tick(10)
				
				'''
				for x in range(len(s.body)):
					if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
						print('Score: ', len(s.body))
						message_box('You Lost!', 'Play again...')
						s.reset((10,10))
						break
						'''
		 		
				# redrawWindow(win)
			except BlockingIOError:
				
				continue
			finally:
				player.move(sock, playerid)
 

main()