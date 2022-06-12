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

import random
import h5py
from abc import ABC, abstractmethod
from copy import copy
from tqdm import tqdm

from game import Game
from utils import Result, Color
from players import RandomAI

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
