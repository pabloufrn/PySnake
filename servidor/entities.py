from collections import deque

class Player:
	def __init__(self, conn, address):
		self.snake_size = 3
		self.conn = conn
		self.address = address
		self.snake = deque()
		self.last_move = "up"
		self.next_move = "right"
		self.name = None
		self.score = 0

	def send_message(self, message):
		self.conn.send(message.encode())
	def spawn(self, pos, size):
		self.snake = deque()
		for _ in range(size):
			self.snake.append(pos)
	def try_eat(self, apple_pos):
		if(len(self.snake) > 0 and self.snake[0] == apple_pos):
			self.snake.append(self.snake[-1])
			self.score += 1
			return True
		else: 
			return False
	def move(self, width, height):
		if(not self.name or len(self.snake) == 0):
			return
		self.snake.pop()
		self.last_move = self.next_move
		next_pos = None
		if(self.next_move == "up"):
			if(self.snake[0][1] == 0):
				next_pos = (self.snake[0][0], height-1)
			else:
				next_pos = (self.snake[0][0], self.snake[0][1]-1)
		elif(self.next_move == "down"):
			if(self.snake[0][1] == height-1):
				next_pos = (self.snake[0][0], 0)
			else:
				next_pos = (self.snake[0][0], self.snake[0][1]+1)
		elif(self.next_move == "left"):
			if(self.snake[0][0] == 0):
				next_pos = (width-1, self.snake[0][1])
			else:
				next_pos = (self.snake[0][0]-1, self.snake[0][1])
		elif(self.next_move == "right"):
			if(self.snake[0][0] == width-1):
				next_pos = (0, self.snake[0][1])
			else:
				next_pos = (self.snake[0][0]+1, self.snake[0][1])
		else:
			print("direção invalida")
			exit(1)
		self.snake.appendleft(next_pos)

		