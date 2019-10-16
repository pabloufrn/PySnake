
class Player:
	def __init__(self, conn, address):
		self.snake_size = 3
		self.conn = conn
		self.address = address
		self.snake = []
		# self.set_position((0,0)) # posição aleatoria
	def set_name(self, name):
		self.name = name

	def send_message(self, message):
		self.conn.send(message.encode())