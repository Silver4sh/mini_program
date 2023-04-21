import os
import tkinter as tk

## Choose game
def game(choose_game):
    if choose_game == 1:
        from guess_number import guess_number
    elif choose_game == 2:
       from rock_paper_scissor import rock_paper_scissor_v2
    elif choose_game == 3:
        from rolling_dice import rolling_dice
    elif choose_game == 4:
        from hang_man import hang_man
    else :
        return ("i'm sorry %s not exist", choose_game)

## Main Menu
class mini_games:
    list_game = 'Guess Number [1], Rock Paper Scissor [2], Rolling Dice [3], Hang Man[4]'
    def __init__(self):
        self.name = str(input("What's your name ?\n"))
        os.system('cls')
        print('Hello,', self.name)
        print(mini_games.list_game)
        self.game = int(input('What game you wanna play ?\n'))
        os.system('cls')
        game(self.game)
        
    
## Running
mini_games()