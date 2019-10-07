import deque

class Player:
	def __init__(self, name, snake_size, position):
		self.name = name
		self.snake_size = snake_size
		self.set_position(position)

	def set_position(self, pos):
		for _ in range(snake_size):
			snake.push(pos)