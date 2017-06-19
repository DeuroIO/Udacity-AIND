import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras

import re

# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(array,window_size):
    first_index = 0
    my_x_array = []
    my_y_array = []
    while first_index + window_size + 1< len(array):
        tmp_array = []
        for x in range(first_index,first_index+window_size):
            tmp_array.append(array[x])
        my_x_array.append(tmp_array)
        my_y_array.append(array[first_index+window_size])
        first_index += 1
    return (np.array(my_x_array),my_y_array)

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(step_size, window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    model.add(Dense(1))
    model.summary()
    return model


### TODO: list all unique characters in the text and remove any non-english ones
def clean_text(text):
    # find all unique characters in the text
    chars = sorted(list(set(text)))
    for char in chars:
        print(char)

    # remove as many non-english characters and character sequences as you can 
    text = re.sub('([^a-zA-Z\s])+', '', text)
    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text,window_size,step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
    

    
    return inputs,outputs
