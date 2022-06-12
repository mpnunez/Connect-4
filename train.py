"""
Code for training an AI model on historical data
"""


import h5py
import pandas as pd

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models


def train(h5file):

    with h5py.File(h5file, "r") as f:
        board_data = f["board"][:]
        df = pd.DataFrame(f["move"][:])
    

    df["whose_turn"] = ((df["whose_turn"] + 1) / 2).astype(int)
    
    
    discount = 0.95
    df["position_eval"] = df.apply(lambda row: row["game_result"] * discount ** row["moves_before_finish"],axis=1)
    
    
    df["weight"] = df["position_eval"].apply(lambda x: 0.1 if x==0 else 1)
    
    print(board_data.shape)
    
    b_channel = np.array([np.where(board_data==1,1,0),np.where(board_data==-1,1,0)])
    print(b_channel.shape)
    b_channel = np.swapaxes(b_channel,0,1)
    b_channel = np.swapaxes(b_channel,1,2)
    b_channel = np.swapaxes(b_channel,2,3)
    
    print(b_channel.shape)
    
    #game_result_onehot = keras.utils.to_categorical(df["game_result"], 3) # BUG, the -1 are not mapped correctly

    
    move_chosen_onehot = keras.utils.to_categorical(df["move_chosen"], 7)

    
    
    whose_turn_onehot = keras.utils.to_categorical(df["whose_turn"], 2)
    print(whose_turn_onehot)
    
    inputs = keras.Input(shape=b_channel.shape[1:])
    
    
    
    x = layers.Conv2D(16, (4, 4), activation='relu')(inputs)
    x = layers.MaxPooling2D((2,2))(x)
    x = layers.Flatten()(x)
    
    inputs2 = keras.Input(shape=move_chosen_onehot.shape[1:])
    inputs3 = keras.Input(shape= whose_turn_onehot.shape[1:])
    #y = models.Model(inputs=inputs2,output=y)
    combined = tf.keras.layers.concatenate([x, inputs2])
    combined2 = tf.keras.layers.concatenate([combined, inputs3])
    
    output = layers.Dense(1,activation="linear")(combined2)
    
    
    model = keras.Model([inputs,inputs2,inputs3], output, name = "connect4cnn2")
    model.summary()
    
    
    model.compile(loss='mean_absolute_error', optimizer="adam")
    model.fit(x=[b_channel, move_chosen_onehot, whose_turn_onehot], y=df["position_eval"].values, batch_size=100, epochs=10, validation_split=0.1, sample_weight=df["weight"].values)
    
    return model

if __name__=="__main__":
    train("E:\Coding\spyder_projects\connect4\connect4games2.hdf5")

