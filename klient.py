import socket
from clientLogicTest import get_idx, newGame,prepGame
import numpy as np
import json
from printBoard import printBoard


GAME_PORT = 5005
DISCOVERY_PORT = 5006

def find_server():
    discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    discovery_sock.settimeout(3)

    discovery_sock.sendto(
        "FIND_BATTLESHIP_SERVER".encode(),
        ("255.255.255.255", DISCOVERY_PORT)
    )

    try:
        data, addr = discovery_sock.recvfrom(1024)

        if data.decode() == "BATTLESHIP_SERVER_HERE":
            return (addr[0], GAME_PORT)

    except socket.timeout:
        return None


server_addr = find_server()

if server_addr is None:
    print("Nie znaleziono serwera")
    exit()

print("Znaleziono serwer:", server_addr)


########################
# okazuje się że główna pętla gry to maszyna stanów
########################


joined = False


######
#schemat protokołu komunikacji od strony player
#{
#    "type": "game_start",
#    "game_id": 1,
#    "player_id": 1,
#    "board": None,
#    "move": None,
#    "result": None,
#    "message": "Znaleziono przeciwnika. Jesteś graczem 1"
#}

enemy_board = [
        [None, "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        ["1 ",  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["2 ",  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["3 ",  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["4 ",  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["5 ",  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["6 ",  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["7 ",  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["8 ",  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["9 ",  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["10", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]


# tworzenie socketu UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# automatyczny lokalny port klienta
sock.bind(("", 0))

print("Klient uruchomiony wpisz 'join' żeby dołączyć i 'exit' żeby wyjść\n")



while not joined:
    starting_msg = input("wiadomość:").strip().lower() #usuwamy spacje na koncach i zmieniamy na male litery

    if starting_msg == 'join':
        # newGame()
        # board = prepGame()
        # board = board.tolist()
        #tablica do testów 
        board = [
        [None, "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        ["1",  1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["2",  1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["3",  1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["4",  1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["5",  0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        ["6",  0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        ["7",  0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        ["8",  0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
        ["9",  0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ["10", 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                ]
        
        packet = {
            "type":"join",
            "game_id":None,
            "player_id":None,
            "board":board,
            "move": None,
            "result":None,
            "message":None
        }
        msg = json.dumps(packet)
        msg = msg.encode()
        sock.sendto(msg,server_addr)
        joined = True
        state = "idle"
    elif starting_msg == 'exit':
        print("opuszczanie programu")
        break
    else:
        print("niepoprawna wiadomość")
        continue


print("Zasady są proste, podajesz pole np A4 i próbujesz trafić statek wroga, powodzenia!!\n")

while joined:
    ###
    # maszyna stanów
    ###
    while state == "idle":
        
        
        print("proszę czekać\n")
        data, addr = sock.recvfrom(1024)
        data = data.decode()
        #od serv_msg będzie zależało w jaki stan przechodzi maszyna
        packet = json.loads(data)
        state = packet["type"]
        if packet["board"] is not None:
            board = packet["board"]
        


    
    if state == "waiting":
        print(packet["message"])
        state = "idle"
    
    if state == "game_start":
        print(state)
        print(packet["message"])
        print("towja plansza: ")
        printBoard(board)
        player_id = packet["player_id"]
        if player_id == 1:
            state = "your_turn"
        elif player_id == 2:
            print("czekasz na ruch przeciwnika...")
            state = "idle"
        else:
            print("wywaliło się player id")
            break
    if state == "your_turn":
        print(state)
        if packet["result"] is not None:
            print(packet["result"])

        if packet["board"] is not None:
            board = packet["board"]
        
        print("Twoja plansza:\n")
        printBoard(board)

        print("Twoja mapa strzałów:\n")
        printBoard(enemy_board)
        
        print("Twoja tura!\n")

        correct_msg = False
        while not correct_msg:
            msg = input("Podaj pole w które chcesz strzelić: \n")
            i,j = get_idx(msg)
            if i == 0 or j == 0:
                print("podano niepoprawne pole")
                continue
            else:
                print(f"Strzelono w pole o indexie [{i},{j}]\n")
                correct_msg = True
            response = {
                "type":"move",
                "game_id":packet["game_id"],
                "player_id":packet["player_id"],
                "board":board,
                "move": [i,j],
                "result":None,
                "message":None
            }
            msg = json.dumps(response).encode()
            sock.sendto(msg, server_addr)
            state = "idle"
    if state == "move_result":
        print(state)
        print(packet["result"])

        shot_result = packet["move"]
        j = shot_result[0]
        i = shot_result[1]
        move_id = shot_result[2]
        enemy_board[j][i] = move_id
        print("Twoja mapa strzałów:\n ")
        printBoard(enemy_board)

        state = "idle"
    if state == "end_game":
        print(state)
        print(packet["result"])
        print(packet["message"])
        print("dziękujemy za grę!")
        joined = False
        break

print("zakończono program")





