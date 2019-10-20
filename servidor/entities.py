
class Player:
	def __init__(self, conn, address):
		self.snake_size = 3
		self.conn = conn
		self.address = address
		self.snake = []
		self.last_move = "up"
		self.next_move = "right"
		self.name = None
		# self.set_position((0,0)) # posição aleatoria
	def set_name(self, name):
		self.name = name

	def send_message(self, message):
		self.conn.send(message.encode())