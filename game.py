# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

See https://ringsdb.com/api/doc

Environment needs:
h5py
tensorflow
keras
matplotlib
seaborn
"""



import numpy as np
from enum import IntEnum
import random
import h5py
from abc import ABC, abstractmethod
from copy import copy
from tqdm import tqdm

class Color(IntEnum):
    EMPTY = 0
    RED = 1
    BLUE = -1

class Result(IntEnum):
    DRAW = 0
    RED = 1
    BLUE = -1
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
        
        # Record states
        self.record = True
        self.state_history = []
        self.move_history = []
        
        # Game variables
        self.board = np.full((self.n_rows,self.n_cols),Color.EMPTY)
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
            ((0,1), (0,-1)),
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
                
                if self.record:
                    self.state_history.append(copy(self.board))
                
                
                # Player makes the next move
                next_move = p.make_move(self)
                if self.record:
                    self.move_history.append(next_move)
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
        
class Player(ABC):
    def __init__(self,color):
        self.color=color
        
    @abstractmethod
    def make_move(self,game):
        pass
    

class HumanPlayer(Player):
    def make_move(self,game):
        print(game.board)
        print(game.get_available_moves())
        return int(input("Choose column: "))

class RandomAI(Player):
    def make_move(self,game):
        return random.choice(game.get_available_moves())
    
class AIPlayer(Player):
    def make_move(self,game):
        return game.get_available_moves()[0]

def main():

    results = {
        Result.RED : 0,
        Result.BLUE : 0,
        Result.DRAW : 0
    }

    n_games = 10_000
    with h5py.File("connect4games2.hdf5", "w") as f:
        board_ds = f.create_dataset("board", (100, 6, 7), maxshape=(None, 6, 7))
        
        column_names = ["moves_before_finish",
         "game_id",
        "game_result",
        "whose_turn",
        "move_chosen"]
        ds_dt = np.dtype({"names": column_names,
                  "formats":[(int)]*len(column_names)
                  })
        dummy_data = np.rec.fromarrays([
            np.zeros(100) for _i in column_names], dtype=ds_dt
            )
        moves_ds = f.create_dataset("move", data=dummy_data, maxshape=(None,))
        
        first_row_ind = 0
        for i in tqdm(range(n_games)):
            
            # Create and play game
            g = Game()
            g.players = (RandomAI(Color.RED),RandomAI(Color.BLUE))
            g.play()
            
            # Record aggregate result
            results[g.status] += 1
            
            n_moves = len(g.move_history)
            last_row_ind_plus_one = first_row_ind + n_moves
            
            
            
            # Record result in HDF5
            if last_row_ind_plus_one > len(board_ds):
                board_ds.resize(last_row_ind_plus_one,axis=0)
                moves_ds.resize(last_row_ind_plus_one,axis=0)
            board_ds[first_row_ind:last_row_ind_plus_one,:,:] = g.state_history
            
            moves_ds["moves_before_finish",first_row_ind:last_row_ind_plus_one] = np.array(list(reversed(range((n_moves)))))
            moves_ds["game_id",first_row_ind:last_row_ind_plus_one] = np.full((n_moves,),i)
            moves_ds["game_result",first_row_ind:last_row_ind_plus_one] = np.full((n_moves,),g.status)
            moves_ds["whose_turn",first_row_ind:last_row_ind_plus_one] = np.array([(1,-1)[i%2] for i in range(n_moves)])
            moves_ds["move_chosen",first_row_ind:last_row_ind_plus_one] = g.move_history
            
            first_row_ind += n_moves
        
    print(results)
    
    
if __name__ == "__main__":
    main()
