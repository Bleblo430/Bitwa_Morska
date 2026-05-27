import socket 

UDP_IP = ""
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("serwer działa")

queue= []

games = []

# game_data = [addr1,addr2,tab1,tab2,turn,score1,score2]

while True:


    data, addr = sock.recvfrom(1024)

    msg = data.decode()

    if msg == "join":
        #logika dołączania
        if addr in queue:
            print("cierpliwości, jesteś w kolejce")
        else:
            for game_data in games:
                if addr == game_data[0] or addr == game_data[1]:
                    game_nr = games.index(game_data)
                    print(f"znajdujesz się w grze {game_nr}")
                else:
                    addr.append(queue)
                    print("dodano do kolejki")

    elif msg == "exit":
        for game_data in games:
                if addr == game_data[0] or addr == game_data[1]:
                    #trzeba dorobić 
                    game_nr = games.index(game_data)
                    games.remove(game_nr)
                    print("rozłączoni")
    else:
        #tutaj tylko modyfikujemy plansze zrobione po stronie klienta tzn data to tuple indexów z get_idx
        print("gramy")

    #logika zapełnienia kolejki
    if len(queue) ==2:
        games.append([queue[0],queue[1]])

        queue.clear()
        

    







