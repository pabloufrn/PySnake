import json


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
                        send__message__to_player(playerid, "accept", str(playerid))
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

    def process_message(cmd, message):
        message = json.loads(json_message.decode("utf-8"))
        if(message["event"] == "setup"):
            player = self.players[message["playerid"]]
            player.name = message["playername"]
            # colocar em uma posição, definir o tamanho

    def log_player_event(self, playerid, message):
        player = self.players[playerid]
        print(f"{player.name} {message}.")

    def send__message__to_all(self, message):
        for player in self.players:
            player.send_message(message)

     def send__message__to_player(self, message):
        players[playerid].send_message(message)

    def gameOver(self):
        print "Game Over\n"


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
    "playername": 0
}
Setup (enviador pelo server):
{
    "playerid": 0,
    "height": 20,
    "width": 30 
}

'''