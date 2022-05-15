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

color_to_result = {
    Color.RED: Result.RED,
    Color.BLUE: Result.BLUE
    }

class Game:
    
    def __init__(self):
        
        # Game configuration
        self.n_rows = 6
        self.n_cols = 7
        self.n_in_a_row = 4
        
        self.turn = Color.RED
        self.board = np.full((self.n_rows,self.n_cols),Color.EMPTY)
        self.players = (Player(Color.RED),Player(Color.BLUE))
        self.status = Result.INPROGRESS
        
    def drop_checker(self,col_num,color):
        row_num = np.where(self.board[:,col_num]==Color.EMPTY)[0][-1]
        self.board[row_num,col_num] = color
        return row_num
        
    def count_connections_in_dir(self,new_row,new_col,color,dir_row,dir_col):
        n_seq = 0
        for i in range(1,self.n_in_a_row):
            r = new_row + i * dir_row
            c = new_col + i * dir_col
            if r < 0 or r >= self.n_rows or c < 0 or c >= self.n_cols:
                break
            
            if self.board[r,c] == color:
                n_seq += 1
            else:
                break
            
        return n_seq
            
    
    def check_connections(self,new_row,new_col,color):
        """
        
        """
        
        victory_directions = (
            ((-1,0), (1,0)),
            ((0,1), (1,0)),
            ((-1,-1), (1,1)),
            ((-1,1),(1,-1))
            )
        
        for vd in victory_directions:
            if sum(
                self.count_connections_in_dir(new_row,new_col,color,*d) for d in vd
                ) >= self.n_in_a_row:
                return True
            
        
        return False
        
    def play(self):
        while self.status == Result.INPROGRESS:
            for p in self.players:
                
                # Player makes the next move
                next_move = p.make_move(self)
                #print("Play {} at column {}".format(p.color,next_move))
                next_row = self.drop_checker(next_move,p.color)
                
                # Check for a win
                self.status = color_to_result[p.color] if self. check_connections(next_row,next_move,p.color) else Result.INPROGRESS
                if self.status != Result.INPROGRESS:
                    break
                
                # Check for end of the game
                if len(self.get_available_moves())==0:
                    self.status = Result.DRAW
                    break
            
        #print("result is {}".format(self.status))
        #print(self.board)
            
    def get_available_moves(self):
        return [j for j in range(self.n_cols) if self.board[0,j] == Color.EMPTY]
        
class Player:
    def __init__(self,color):
        self.color=color
        
    def make_move(self,game):
        return random.choice(game.get_available_moves())
    

def main():

    results = {
        Result.RED : 0,
        Result.BLUE : 0,
        Result.DRAW : 0
    }

    n_games = 100
    for i in range(n_games):
        g = Game()
        g.play()
        results[g.status] += 1
        
    print(results)
    
    
if __name__ == "__main__":
    main()
