import numpy as np
import hashlib

def hash_state(state, num_rows, num_cols):
    state_info = state.observation_tensor()
    num_cells = ((1 + num_rows) * (1 + num_cols))

    np_state_info = np.array(state_info)
    state_matrix = np_state_info.reshape(3, num_cells, 3)
    filtered_state_matrix = np.stack([state_matrix[:,:,0], state_matrix[:,:,1]], axis=-1)
    filtered_state_matrix = filtered_state_matrix.astype(int)
    merged_array = np.bitwise_or(filtered_state_matrix[1], filtered_state_matrix[2])
    
    # arr_bytes = merged_array.tobytes()
    # hash_object = hashlib.sha256(arr_bytes)
    # hash_hex = hash_object.hexdigest()
    # return hash_hex
    return state_matrix

# DOC: 

# def in_cache(state, cache, num_rows, num_cols):
#     # hashed_state -> [lower_bound, upper_bound] #lowerbound of minimax value.
#     # state will be the configuration of the edges, but it should also be that 
#     # state who are symmetries of each other, to result in the same lower and 
#     # upperbound of the minimax value, as they encode the same state.
    
#     # Also, the underlying game object in open_spiel encodes the game via 3 vectors, 
#     # _v, _h and _p. See seperate PDF, We don't need _p as per the paper "Solving Dots-And-Boxes".

#     # Also, the vectors _v and _h contain entries of types '0', '1' or '2'. We will merge the 
#     # values '1' and '2' together to the value '1'. As any notion of players is not of importance.
#     # Once again, refer to the paper.
    
#     # we must make sure that symmestries of the state, result in the same hash, how do wo do this? 
    
    
#     hashed_state = hash_state(state, num_rows, num_cols)
#     return hashed_state in cache

# def hash_state(state, num_rows, num_cols):
#     # state.observation_tensor() returns a 3-d tensor.
#     # see respective dots_and_boxes.cc file
#     # 
#     #   TensorView<3> view(values,
#     #                      {/*cellstates=*/3, num_cells_,
#     #                       /*part of cell (h, v, p)=*/3},
#     #                      true);

#     # cellstate = empty , player1 , player2 
#     # num_cells = aantal (x,y) punten in dots and boxes waaruit edjes vertrekt. 
#     #           | zie aparte pdf file in doc folder.
#     # part of cell = defines if the edge is horizontal, vertical or p 
#     #              | p => player points, defines if it results in player i's point towards a box.)
    
#     # we zijn ekel geinteresseerd in player1 + player2 dimensies, waarvan alle num_cells en waarvan 
#     # enkel horizontal of vertical van belang is. 

#     state_info = state.observation_tensor()
#     num_cells = ((1 + num_rows) * (1 + num_cols))
#     # print(len(state_info), 3*num_cells*3)
    
#     # info: 
#     # empty player = indices van 0 -> 3 * num_cells
#     # first player = indices van 3 * num_cells -> 2 * 3 * num_cells
#     # thrid player = indices van 2 * 3 * num_cells -> 3 * 3 * num_cells

#     # we hebben niet elke 3 * num_cells nodig. 
#     # enkel 2 * num_cells
    
#     np_state_info = np.array(state_info)
#     state_matrix = np_state_info.reshape(3, num_cells, 3)

#     # (3, 9, 3)
#     # [[[1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]]

#     #  [[0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]]

#     #  [[0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]]]

#     # [ 1  1  1] => [horinzontal vertical dezeplayerheeftdezeboxofniet]
#     # derde index niet nodig. 
#     # [[1 1 1] ... ] => 16 cells of 9 cells voor aantal xy punten in x keer y dots and boxes game.
#     # [[ [1 1 1] ... ] ... ] => voor elk player, waarbij de eerste de null player is. 

#     # print(state_matrix.shape)
#     # print(state_matrix)

#     filtered_state_matrix = np.stack([state_matrix[:,:,0], state_matrix[:,:,1]], axis=-1)

#     # print(filtered_state_matrix.shape)
#     # print(filtered_state_matrix)

#     arr_bytes = filtered_state_matrix.tobytes()
#     hash_object = hashlib.sha256(arr_bytes)
#     hash_hex = hash_object.hexdigest()
#     return hash_hex


# # Original array
    # original_array = np.array([
    #                         [[1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1]],
                            
    #                         [[0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0]],
                            
    #                         [[0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0]]])

    # # Merge the last two lists of the first dimension using binary OR operation
    # merged_array = np.bitwise_or(original_array[1], original_array[2])

    # print(merged_array)