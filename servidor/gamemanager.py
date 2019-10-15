import json


class GameManager:
    #initializing
    def __init__(self):
        try:
            players = []
            # carregar configuração  
            self.load_config()
            # spawn em maca
            # esperar jogador

        except Exception as e:
            print(e)
            self.sock.close()
            exit()

    def get_random_valid_position():
        x = randint(1, self.width-1)
        y = randint(1, self.height-1)
        invalid = False
        for _ in range(0, (self.width-1)*(self.height-1)-1):
            for player in self.player:
                invalid = False
                if((x, y) in player.body):
                    if(x == self.width-2):
                        x = 0
                        if(y == self.height-2):
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

    def spawn_player(self):
        # todo: pode não vai retornar, e sim alterar o player
        pos = self.get_random_valid_position()
        body = []
        for _ in range(self.min_player_size):
            body.append(pos)
        return body

    def log_event(self, eventbytes):
        print(eventbytes.decode("utf-8"))

    def send_event_to_all(self, dictjson):
        for player in self.players:
            player.send_message(json.dumps(dictjson))

    def send_event__to_player(self, dictjson):
        players[playerid].send_message(json.dumps(dictjson))

    def print_apple_board(self):
        for x in range(self.board_width):
            for y in range(self.board_height):
                continue

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

    def play(self):
        read_list = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setblocking(0)
            s.bind(('', self.port))
            s.listen(5)
            read_list.append(s)
            while True :
                readable, writeable, error = select.select(read_list,[],[])
                for sock in readable:
                    if sock is s:
                        conn, info = sock.accept()
                        read_list.append(conn)
                        print("connection received from ", info)
                        strplayerid = str(len(players))
                        self.players.append(Player(info))
                        # todo: send_event_to_all
                    else:
                        data = sock.recv(1024)
                        '''
                        if data:
                            cmd, playerid, arg = data.decode("utf-8").split(".")
                            playerid = int(playerid)
                            if(cmd == "conn"):
                                players[playerid].name = arg
                                msg = f"Jogador {arg} conectado."
                                send_message_to_all(read_list, msg.encode("utf-8"))
                            elif(cmd == "move"):
                                print(f"Jogador {players[playerid].name} se moveu para {arg}.")
                        else:
                            sock.close()
                            read_list.remove(sock)'''

    def process_events(cmd, eventbytes):
        event = json.loads(eventbytes.decode("utf-8"))
        if(event["eventname"] == "setup"):
            player = self.players[event["playerid"]]
            player.name = event["playername"]
            player.body = self.get_random_body()

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