
from termcolor import colored, cprint
def widePrintBoard(board):
    for i in board:
        for j in i:
            if type(j) == int:
                if j == 0:
                    cprint(" ■ ", "cyan", end="")
                elif j == 1:
                    cprint(" ■ ", "green", end="")
                elif j == 2:
                    cprint(" ■ ", "red", end="")
                elif j == 3:
                    cprint(" ■ ", "magenta", end="")
                elif j == 4:
                    cprint(" ■ ", "yellow", end="")
            else:
                print(j, end="")
        print("", end="\n")

def printBoard(board):
    for i in board:
        for j in i:
            if type(j) == int:
                if j == 0: # woda, puste pole
                    cprint("■", "cyan", end="")
                elif j == 1: # statek ktory stoi
                    cprint("■", "green", end="")
                elif j == 2: # trafione pole
                    cprint("■", "red", end="")
                elif j == 3: #pudlo
                    cprint("■", "magenta", end="")
                elif j == 4: # to sie nigdy nie stanie, to jest legacy, mozna z tego zrobic statek wlasnie stawiony
                    cprint("■", "yellow", end="")
            else:
                print(j, end="")
        print("", end="\n")