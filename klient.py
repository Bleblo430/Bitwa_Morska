import socket
from clientLogicTest import get_idx
import numpy as np
import json

UDP_IP = "127.0.0.1"   # IP serwera
UDP_PORT = 5005

server_addr = (UDP_IP,UDP_PORT)

########################
# okazuje się że główna pętla gry to maszyna stanów
########################

state = "idle"
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


# tworzenie socketu UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# automatyczny lokalny port klienta
sock.bind(("", 0))

print("Klient uruchomiony wpisz 'join' żeby dołączyć i 'exit' żeby wyjść")

board = np.array([]) #plansza testowa

while not joined:
    starting_msg = input("wiadomość:").strip().lower() #usuwamy spacje na koncach i zmieniamy na male litery

    if starting_msg == 'join':
        board = board.tolist()
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

print("wyjście z pierwszego while")
print("((przed będzie tworzenie tablicy)) zasady są proste, podajesz pole np A4 i próbujesz trafić statek wroga, powodzenia!!")

while joined:
    
    #trzeba dodać odebranie wiadomości od serwera który mówi czyja jest tura
    print("jesteś w głównej pętli")


    ###
    # maszyna stanów
    ###
    while state == "idle":
        data, addr = sock.recvfrom(1024)
        data = data.decode()
        #od serv_msg będzie zależało w jaki stan przechodzi maszyna
        packet = json.loads(data)
        state = packet["type"]
    
    if state == "waiting":
        print(packet["message"])
        state = "idle"
    
    if state == "game_start":
        print(packet["message"])
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
        correct_msg = False
        while not correct_msg:
            msg = input("Podaj pole w które chcesz strzelić")
            i,j = get_idx(msg)
            if i == 0 or j == 0:
                print("podano niepoprawne pole")
                continue
            else:
                print(f"Strzelono w pole o indexie [{i},{j}]")
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
        print(packet["result"])
        state = "idle"
    if state == "end_game":
        print(packet["result"])
        print(packet["message"])
        print("dziękujemy za grę!")
        joined = False
        break

print("zakończono program")





