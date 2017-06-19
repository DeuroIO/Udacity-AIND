import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras


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
    pass


### TODO: list all unique characters in the text and remove any non-english ones
def clean_text(text):
    # find all unique characters in the text


    # remove as many non-english characters and character sequences as you can 


### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text,window_size,step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
    

    
    return inputs,outputs
