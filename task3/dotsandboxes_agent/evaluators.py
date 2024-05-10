import numpy as np

def eval_maximize_difference(state, maximizing_player_id): 
    params = state.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    num_dots = ((1 + num_rows) * (1 + num_cols))

    state_info = state.observation_tensor()    
    np_state_info = np.array(state_info)

    # {cellstates= (empty, player1, player2), num_cells , part_of_cell(horizontal, vertical, which_player_won) = 3},
    state_matrix = np_state_info.reshape(3, num_dots, 3)

    points_max_player = sum(state_matrix[maximizing_player_id+1,:,2])
    points_min_player = sum(state_matrix[2 - maximizing_player_id,:,2])
    return (points_max_player - points_min_player)