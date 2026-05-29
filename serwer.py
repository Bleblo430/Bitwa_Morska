import socket 
import json
import threading

GAME_PORT = 5005
DISCOVERY_PORT = 5006

def discovery_server():
    discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_sock.bind(("", DISCOVERY_PORT))

    print("Discovery działa")

    while True:
        data, addr = discovery_sock.recvfrom(1024)
        msg = data.decode()

        if msg == "FIND_BATTLESHIP_SERVER":
            discovery_sock.sendto("BATTLESHIP_SERVER_HERE".encode(), addr)


threading.Thread(target=discovery_server, daemon=True).start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", GAME_PORT))

#=^-^=
#.,.

# game_data = [addr1,addr2,tab1,tab2,turn,score1,score2]

####
#schemat protokołu komunikacji od strony serwera
# {
#     "type": "your_turn",
#     "game_id": 1,
#     "player_id": 1,
#     "board": None,
#     "move": None,
#     "result": None,
#     "message": "Twoja tura"
# }
#####
#schemat player do queue
# {
#     "addr": addr,
#     "board": packet["board"],
#     "player_id": None
# }
print("serwer działa")

queue = []

games = []

while True:
    print("jestem przed recvfrom")
    #odbiór danych
    data, addr = sock.recvfrom(1024)
    data = data.decode()
    packet = json.loads(data)
    #rozpakowane dane z json
    move_type = packet["type"]
    

    #print(f"jestem za recvfrom type = {move_type}, move = {packet['move']}, board = {packet['board']}")
    #logika dołączania
    
    if move_type == "join":
        print(move_type)
        player = {
            "addr" : addr,
            "board" : packet["board"],
            "player_id" : None
        }
        already_in_queue = any(p["addr"] == addr for p in queue)
        if not already_in_queue:  
            queue.append(player)
            response = {
                "type": "waiting",
                "game_id": None,
                "player_id": None,
                "board": None,
                "move": None,
                "result": None,
                "message": "Dodano do kolejki, czekam na drugiego gracza"
            }
            msg = json.dumps(response).encode()
            sock.sendto(msg, addr)
        else:
            response = {
                "type": "waiting",
                "game_id": None,
                "player_id": None,
                "board": None,
                "move": None,
                "result": None,
                "message": "Już jesteś w kolejce, cierpliwości"
            }
            msg = json.dumps(response).encode()
            sock.sendto(msg, addr)
             
        if len(queue) == 2:
            player1 = queue.pop(0)
            player2 = queue.pop(0)
            player1["player_id"] = 1
            player2["player_id"] = 2

            new_game_id = len(games) + 1
            game = {
                "game_id":new_game_id,
                "players":[player1,player2],
                "move_count":0,
                "score":{
                    1: 0,
                    2: 0
                },
                "status":"running"
            }
            games.append(game)

            response_1 = {
                "type": "game_start",
                "game_id": new_game_id,
                "player_id": 1,
                "board": player1["board"],
                "move": None,
                "result": None,
                "message": "dołączono do gry, jesteś graczem nr 1, zaczynasz! "
            }
            response_2= {
                "type": "game_start",
                "game_id": new_game_id,
                "player_id": 2,
                "board": player2["board"],
                "move": None,
                "result": None,
                "message": "dołączono do gry, jesteś graczem nr 2, zaczekaj na ruch gracza nr1 "
            }   
            msg1= json.dumps(response_1).encode() 
            sock.sendto(msg1, player1["addr"])   
            msg2 = json.dumps(response_2).encode()  
            sock.sendto(msg2,player2["addr"])      
    if move_type == "move":
        print(move_type)
        # 0 - puste pole, woda 
        # 1 - statek przeciwnika
        # 2 - trafiony statek przeciwnika
        # 3 - trafione puste pole

        #znalezienie odpowiadającej gry
        game_id = packet["game_id"] 
        game = games[game_id-1]
        

        #odczytanie ruchu
        move = packet["move"]
        i = move[0]
        j = move[1]

        #znalezienie graczy
        players = game["players"]
        shooter_id = packet["player_id"] #kto wykonał ruch

        if shooter_id == 1:
            shooter = players[0]
            targeted_player = players[1]
        elif shooter_id == 2:
            shooter = players[1]
            targeted_player = players[0]
        
        #tablice graczy
        targeted_player_board = targeted_player["board"]
        shooter_board = shooter["board"]

        #rodzaj trafionego pola
        space_type = targeted_player_board[j][i]

        if space_type == 0:
            result_id = 3
            targeted_player_board[j][i] = 3
            result1 = "trafiono w wodę"
            result2 = "przeciwnik trafił w wodę"
        elif space_type == 1:
            result_id = 2
            targeted_player_board[j][i] = 2
            game["score"][shooter_id] +=1
            result1 = "trafiono statek przeciwnika!!!"
            result2 = "trafiono twój statek!!!"
        elif space_type ==2:
            result_id = 2
            result1 = "trafienie tego samego pola na statku 2 razy nie sprawi że zatopisz go bardziej"
            result2 = "przeciwnik jest debilem"
        elif space_type ==3:
            result_id = 3
            result1 = "trafienie 2 razy w to samo pole na wodzie jest nie ma sensu z perspektywy filozoficznej, filozoficznej a już napewno nie z punktu widzenia taktyki wojennej ¯\\_(ツ)_//¯"
            result2 = "przeciwnik jest debilem"

        targeted_player["board"] = targeted_player_board

        if game["score"][shooter_id] >= 20:
            #jeśli wygramy

            win_msg = f"Gratuluje! Wygrałeś wynikiem {game['score'][shooter_id]} do {game['score'][targeted_player['player_id']]}!!!"
            lose_msg = f"Przegrałeś... wynik starcia to {game['score'][shooter_id]} do {game['score'][targeted_player['player_id']]} powodzenia następnym razem"
            response1 = {
            "type": "end_game",
            "game_id": game_id,
            "player_id": shooter["player_id"],
            "board": shooter_board,
            "move": None,
            "result": result1,
            "message": win_msg
            }

            response2 = {
                "type": "end_game",
                "game_id": game_id,
                "player_id": targeted_player["player_id"],
                "board": targeted_player_board,
                "move": None,
                "result": result2,
                "message": lose_msg
            }
            game["status"]= "finished"
            game["move_count"] +=1
            msg1= json.dumps(response1).encode() 
            sock.sendto(msg1, shooter["addr"])   
            msg2 = json.dumps(response2).encode()  
            sock.sendto(msg2,targeted_player["addr"]) 
        else:
            #====
            #dodac żeby odsyłało wynik ruchu do lokalnej planszy przeciwnika
            #====
            shot_result = [j,i,result_id]
            #jeśli jeszcze nikt nie wygral
            response1 = {
            "type": "move_result",
            "game_id": game_id,
            "player_id": shooter["player_id"],
            "board": shooter_board,
            "move": shot_result, 
            "result": result1,
            "message": None
            }

            response2 = {
                "type": "your_turn",
                "game_id": game_id,
                "player_id": targeted_player["player_id"],
                "board": targeted_player_board,
                "move": None,
                "result": result2,
                "message": None
            }
            game["move_count"] +=1
            msg1= json.dumps(response1).encode() 
            sock.sendto(msg1, shooter["addr"])   
            msg2 = json.dumps(response2).encode()  
            sock.sendto(msg2,targeted_player["addr"]) 

        






        
        




            


    