
class Player:
	def __init__(self, conn):
		self.snake_size = 3
		self.conn = conn
		# self.set_position((0,0)) # posição aleatoria
	def set_name(self, name):
		self.name = name

	def send_message(self, message):
		self.conn.send(message.encode("utf-8"))