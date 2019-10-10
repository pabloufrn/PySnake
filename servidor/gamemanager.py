class GameManager:
    #initializing
    def __init__(self):
        try:
            # carregar configuração      
            # spawn em maca
            # esperar jogador

        except Exception as e:
            print(e)
            self.sock.close()
            exit()
    def play(self):
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
                playerid = len(players)
                players.append(Player(conn))
                log_player_event(playerid, "um player foi conectado.")
                send_command_to_player(playerid, "accept", str(playerid))
            else:
                data = sock.recv(1024)
                if data:
                    cmd, playerid, arg = data.decode("utf-8").split(".")
                    playerid = int(playerid)
                    self.process_command(cmd, playerid, arg)
                    # todo: mandar eventos do jogo a cada intervalo
                else:
                    sock.close()
                    read_list.remove(sock)

    def process_command(cmd, playerid, arg):
        if(cmd == "conn"):
            self.log_player_event(playerid, "Conectou-se ao servidor")
            self.send_command_to_all(playerid, "conn", arg)
        elif(cmd == "move"):
            log_player_event(playerid, f"se moveu para {arg}")
            self.send_command_to_all(playerid, "move", arg)

    def log_player_event(self, playerid, message):
        player = self.players[playerid]
        print(f"{player.name} {message}.")

    def send_command_to_all(self, playerid, command, arg):
        for player in self.players:
            player.send_message(f"{command}.{playerid}.{arg}")

     def send_command_to_player(self, playerid, command, arg):
        players[playerid].send_message(f"{command}.{playerid}.{arg}")

    def gameOver(self):
        print "Game Over\n"