# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

See https://ringsdb.com/api/doc
"""



import numpy as np
#import Enum
import random

class Color:
    EMPTY = 0
    RED = 1
    BLUE = -1

class Result:
    RED = 1
    BLUE = 2
    DRAW = 3
    INPROGRESS = 4

class Game:
    def __init__(self):
        self.n_rows = 6
        self.n_cols = 7
        self.turn = Color.RED
        self.board = np.full((self.n_rows,self.n_cols),Color.EMPTY)
        self.players = (Player(Color.RED),Player(Color.BLUE))
        self.status = Result.INPROGRESS
        
    def drop_checker(self,col_num,color):
        row_num = np.where(self.board[:,col_num]==Color.EMPTY)[0][-1]
        self.board[row_num,col_num] = color
        
        
    def play(self):
        while self.status == Result.INPROGRESS:
            for p in self.players:
                
                # Player makes the next move
                next_move = p.make_move(self)
                print("Play {} at column {}".format(p.color,next_move))
                self.drop_checker(next_move,p.color)
                
                # Evaluate position after move
                if len(self.get_available_moves())==0:
                    self.status = Result.DRAW
                    break
            
        print("result is {}".format(self.status))
        print(self.board)
            
    def get_available_moves(self):
        return [j for j in range(self.n_cols) if self.board[0,j] == Color.EMPTY]
        
class Player:
    def __init__(self,color):
        self.color=color
        
    def make_move(self,game):
        return random.choice(game.get_available_moves())
    

def main():

    n_games = 10
    for i in range(n_games):
        g = Game()
        g.play()
    
    
if __name__ == "__main__":
    main()
