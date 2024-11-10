"""
This module provides functions and enumerations to work with the Dots-and-Boxes game, 
specifically related to converting between different representations of the game state.

Author : Ibrahim El Kaddouri
April - 2024
"""


from enum import Enum
import numpy as np

class CellOrientation(Enum):  
    HORIZONTAL = 1
    VERTICAL = 2

class Directions(Enum):  
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

def vectors_to_dbn(num_rows, num_cols, h_, v_):
    """
    Constructs a string as follows : 
    [b | for r in [0,num_rows+1], for c in [0,num_cols]:
         b=1 if horizontal line[r,c] set else 0] 
    
    ++
    
    [b | for r in [0,num_rows_], for c in [0,num_cols+1]:
         b=1 if vertical line[r,c] set else 0]
    """
    matrix1 = np.array(h_)
    matrix2 = np.array(v_)

    flattened_matrix1 = matrix1.flatten()
    flattened_matrix2 = matrix2.flatten()

    h_string = ''.join(map(str, flattened_matrix1))
    v_string = ''.join(map(str, flattened_matrix2))

    return h_string + v_string

def dbn_to_vectors(num_rows, num_cols, dbn:str):
    """
    Create horizontal and vertical edge vectors from the Dots-and-Boxes Notation.
    """
    
    h_ = [[0] * num_cols for _ in range(num_rows + 1)]
    v_ = [[0] * (num_cols + 1) for _ in range(num_rows)]
    num_moves = 0
    
    idx = 0
    for row in range(num_rows + 1):
        for col in range(num_cols):
            if dbn[idx] == '1':
                h_[row][col] = 1
                num_moves += 1
            idx += 1
    
    for row in range(num_rows):
        for col in range(num_cols + 1):
            if dbn[idx] == '1':
                v_[row][col] = 1
                num_moves += 1
            idx += 1
    
    max_moves = (num_rows + 1) * num_cols + num_rows * (num_cols + 1)
    assert num_moves <= max_moves, "Number of moves exceeds maximum possible moves"

    return h_, v_
