import numpy as np
def newGame():
    #tą funkcje pisze sobie na przyszlosc zeby pamietac co trzeba zrobic przy nowej grze
    global prepDone, board, shipsLeft, shipsSet

    board = np.array([[None for j in range(11)] for i in range(11)])
    board[0,] = [None, "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] #inicjalizuje tablice z plansza formatu 10x10 A1 to [0,0] --- pole 0 - puste; pole 1 - statek nietrafiony; pole 2 - spudlowane; pole 3 - statek trafiony; pole 4 - statek wlasnie stawiany
    board[:,0] = [None, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] #inicjalizuje tablice z plansza formatu 10x10 A1 to [0,0] --- pole 0 - puste; pole 1 - statek nietrafiony; pole 2 - spudlowane; pole 3 - statek trafiony; pole 4 - statek wlasnie stawiany
    board[1:,1:] = 0 #ustawiam pola od [1,1] do [10,10] na 0, czyli puste
    
    prepDone = bool(False)
    shipsLeft = [4,3,2,1] # shipsLeft[n] mowi ile zostalo statkow o dlugosci n+1    
    shipsSet = 0
    return

def get_idx(text):
    text = text.replace(" ", "")
    text = text.lower()
    tab = letters = ["a","b","c","d","e","f","g","h","i","j"]
    letters = list(text)
    if len(letters) ==0:
        i = 0
        j = 0
        print("proszę mnie nie denerwować pustymi frazesami")
    elif len(letters)>3:
        i = 0
        j = 0
        print("wiadomośc za długa, wiadomość musi być w formacie litera liczba np B3")
    elif(len(letters)==3):
        if(letters[0].isalpha() and letters[1].isdigit() and letters[2].isdigit()):
            if letters[0] not in tab:
                i = 0
                j = 0
                print("zakres liter od A do J")
            else:
                i = 1 +tab.index(letters[0])
                j = int(letters[1]+letters[2])
        elif(letters[0].isdigit() and letters[1].isdigit() and letters[2].isalpha()):
            if letters[2] not in tab:
                i = 0
                j = 0
                print("zakres liter od A do J")
            else:
                i = 1 +tab.index(letters[2])
                j = int(letters[0]+letters[1])
        else:
            i = 0
            j = 0
            print("wiadomość musi być w formacie litera liczba np. D6")
    else:
        if(letters[0].isalpha() and letters[1].isdigit()):
            if letters[0] not in tab:
                i = 0
                j = 0
                print("zakres liter od A do J")
            else:
                i = 1 +tab.index(letters[0])
                j = letters[1]
        elif(letters[0].isdigit() and letters[1].isalpha()):
            if letters[1] not in tab:
                i = 0
                j = 0
                print("zakres liter od A do J")
            else:
                i = 1 +tab.index(letters[1])
                j = letters[0]
        else:
            i = 0
            j = 0
            print("wiadomość musi być w formacie litera liczba np. D6")
    return [i,j]

def setShip(startXY, endXY):
    if(True): return True

class BreakLoop(Exception): pass

def prepGame():
    global prepDone, shipsSet, shipsLeft, board
    
    shipnumdict = ["pierwszego", "drugiego", "trzeciego", "czwartego", "piatego", "szostego", "siodmego", "osmego", "dziewiatego", "dziesiatego"]

    print(f"=====ETAP 1: STAWIANIE STATKOW=====\nMożesz postawić: {shipsLeft[0]} statki wielkości jednej kratki, {shipsLeft[1]} statki wielkości dwóch kratek, {shipsLeft[2]} statki wielkości trzech kratek i  {shipsLeft[3]} statki wielkości czterech kratek\n")

    while(not(prepDone)):
        try:
            xy_1 = list(get_idx(input("Podaj pole na ktorym znajduje sie początek statku " + shipnumdict[shipsSet] +"\n")))
            if (xy_1 == [0,0]):
                print("input error")
                continue
            else:
                curXY1 = np.array(xy_1, dtype='int')
                if(board[curXY1[1], curXY1[0]] == 1):
                    print("Pole zajęte przez inny statek! Spróbuj ponownie!")
                    continue
            
            xy_2 = list(get_idx(input("Podaj pole na ktorym znajduje sie koniec statku " + shipnumdict[shipsSet] + "\n")))
            
            if (xy_2 == [0,0]):
                print("input error")
                continue
            
            else:
                curXY2 = np.array(xy_2, dtype='int')
                if(board[curXY2[1], curXY2[0]] == 1):
                    print("Pole zajęte przez inny statek! Spróbuj ponownie!")
                    continue
            
            print(curXY1)
            print(curXY2)

            
            if (curXY1[1] == curXY2[1]): #jesli statek horyzontalny lub o rozm 1
                if(curXY2[0] < curXY1[0]): curXY1, curXY2 = curXY2, curXY1
                curShipLen = curXY2[0]- curXY1[0] + 1 #dlugosc statku poziomego to roznice jego xow
                curShipOrientation = 0 #daje int a nie bool, bo tak mozna dodac trzeci kierunek po przekatnej
            elif(curXY1[0] == curXY2[0]): #jesli statek wertykalny
                if(curXY2[1] < curXY1[1]): curXY1, curXY2 = curXY2, curXY1
                curShipLen = curXY2[1] - curXY1[1] + 1 #dlugosc statku pionowego to roznica jego yow
                curShipOrientation = 1 
            else:
                print("Statek musi być w jednej linii, np. A1,D1. Spróbuj ponownie!")
                continue

            if(curShipLen>4): #jesli hor dluzszy niz 4
                print("Statek zbyt długi! Powinien być nie dluzszy niz 4 pola!")
                continue
            else:
                if(shipsLeft[curShipLen-1]): #jesli moge jeszcze stawic taki
                    print(f"STAWIAM STATEK O DLUGOSCI {curShipLen}, POCZATKU W PUNKCIE [{curXY1[0]},{curXY1[1]}] I KONCU W PUNKCIE [{curXY2[0]},{curXY2[1]}]!!!")
                    shipError = False
                
                    if(curShipOrientation==1): #wertykalny, poruszamy sie po yach
                        for y in range(curXY1[1], curXY2[1]+1):
                            try:
                                if(board[y, curXY1[0]] == 1):
                                    print("Nie można postawić statku na polu zajętym przez inny statek! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            try:
                                if(board[y-1, curXY1[0]] == 1):
                                    print("Nie można postawić statku na polu obok innego statku! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            try:
                                if(board[y+1, curXY1[0]] == 1):
                                    print("Nie można postawić statku na polu obok innego statku! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            try:
                                if(board[y, curXY1[0]-1] == 1):
                                    print("Nie można postawić statku na polu obok innego statku! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            try:
                                if(board[y, curXY1[0]+1] == 1):
                                    print("Nie można postawić statku na polu obok innego statku! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            #else:
                            #    board[y, curXY1[0]] = 4
                    
                        if(not(shipError)):
                            board[curXY1[1]:curXY2[1]+1,curXY1[0]] = 1 #ustawiam statek na planszy, !!!uwaga dla np.array jest [y,x]
                            shipsLeft[curShipLen-1] -= 1
                            shipsSet += 1

                    elif(curShipOrientation==0): #if jest tu abundant ale dla czytelnosci - hoyzontalny, porusza sie po xach
                        for x in range(curXY1[0], curXY2[0]+1):
                            try:
                                if(board[curXY1[1], x] == 1):
                                    print("Nie można postawić statku na polu zajętym przez inny statek! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            try:
                                if(board[curXY1[1]-1, x] == 1):
                                    print("Nie można postawić statku na polu obok innego statku! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            try:
                                if(board[curXY1[1]+1, x] == 1):
                                    print("Nie można postawić statku na polu obok innego statku! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            try:
                                if(board[curXY1[1], x-1] == 1):
                                    print("Nie można postawić statku na polu obok innego statku! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            try:
                                if(board[curXY1[1], x+1] == 1):
                                    print("Nie można postawić statku na polu obok innego statku! Spróbuj ponownie!")
                                    raise BreakLoop
                            except(IndexError):
                                pass
                            #else:
                            #    board[curXY1[1], x] = 4
                        if(not(shipError)): 
                            board[curXY1[1],curXY1[0]:curXY2[0]+1] = 1 #ustawiam statek na planszy, w zaleznosci od orientacji
                            shipsLeft[curShipLen-1] -= 1
                            shipsSet += 1
                else:
                    print(f"postawiono już wszystkie statki o długości {curShipLen}\nMożesz jeszcze postawić: {shipsLeft[0]} statki wielkości jednej kratki, {shipsLeft[1]} statki wielkości dwóch kratek, {shipsLeft[2]} statki wielkości trzech kratek i  {shipsLeft[3]} statki wielkości czterech kratek\n")
                    

                #elif(tempShipLen==4): #hor nie dlz niz 4 rowny 4
            
            
            
            if(shipsLeft == [0,0,0,0]): prepDone = True
        except BreakLoop:
            pass
        print(board)


newGame()
prepGame()