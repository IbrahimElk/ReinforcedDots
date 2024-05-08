import numpy as np

def eval_function_maximise_points(state, maximizing_player_id): 
    params = state.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    num_dots = ((1 + num_rows) * (1 + num_cols))
    
    state_info = state.observation_tensor()    
    np_state_info = np.array(state_info)
    
    # {cellstates= (empty, player1, player2), num_cells , part_of_cell(horizontal, vertical, which_player_won) = 3},
    state_matrix = np_state_info.reshape(3, num_dots, 3)
   
    player = state.current_player()
    points_player = sum(state_matrix[player+1,:,2])

    if player == maximizing_player_id:
        return points_player
    else :
        # minimum player wilt de punten van de maximum player minimaleren. 
        return -points_player

def eval_function_minimize_opponent_points(state, maximizing_player_id): 
    params = state.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    num_dots = ((1 + num_rows) * (1 + num_cols))
    
    state_info = state.observation_tensor()    
    np_state_info = np.array(state_info)
    
    # {cellstates= (empty, player1, player2), num_cells , part_of_cell(horizontal, vertical, which_player_won) = 3},
    state_matrix = np_state_info.reshape(3, num_dots, 3)
   
    player = state.current_player()
    points_empty = sum(state_matrix[0,:,2])
    points_player = sum(state_matrix[player+1,:,2])

    total_amnt_boxes = num_rows * num_cols

    points_opponent = (total_amnt_boxes - (points_empty + points_player))

    if player == maximizing_player_id:
        return -points_opponent
    else :
        # minimum player wilt de punten van de maximum player minimaleren. 
        return points_opponent
