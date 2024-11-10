""" 
Evaluation Functions For Search Algorithms 

Author : Staf Rys
April - 2024
"""

import numpy as np
import time 

from deprecated import deprecated

def eval_maximize_difference(state, maximizing_player_id, SA): 
    """
    Evaluates the difference in points between the maximizing player and the minimizing player.
    """
    points_max_player = SA.p_[maximizing_player_id]
    points_min_player = SA.p_[1-maximizing_player_id]
    
    # print(f"points_max_player : {points_max_player}")
    # print(f"points_min_player: {points_min_player}")
    # print(f"difference: {points_max_player - points_min_player}")

    return (points_max_player - points_min_player)


# depreciated due to lack of optimisation, 
# needs to be more performant in order to be considered
# a viable alterantive for an evluation function.
@deprecated
def eval_function_chains(state, maximizing_player_id):
    """
    Considers The Long Chain Rule as heuristic.

    Calculate the heuristic value of a state.
    Arguments:
      state: The current state node of the game.
      maximizing_player_id: The id of the MAX player. The other player is assumed
        to be MIN.
    Returns:
        The heuristic value of the state.
    """
    heuristic = 0
    box_won = 0     
    box_lost = 0   

    num_rows = state.get_game().get_parameters()['num_rows']
    num_cols = state.get_game().get_parameters()['num_cols']

    tensor_data = game_state_tensor(state)
    boxes = box_state_for_pvector(pvector_for_tensor(tensor_data), num_rows, num_cols)
    
    for box in boxes:
        if box == maximizing_player_id + 1: 
            box_won += 1
            heuristic += 1
        elif box != 0:
            box_lost += 1
            heuristic -= 1

    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------
    # Take long chain rule into account # math.ucla.edu/~tom/Games/dots&boxes_hints.html

    # The Long Chain Rule: Suppose the playing field is a rectangle of m rows and n columns and so has mn boxes. 
    # [1] If either m or n is odd, then 
    #       1) the first player should play to make the number of long chains even.
    #       2) the second player should play to make the number of long chains odd. 
    # 
    # [2] If both m and n are even, then 
    #       1) The first player should play to make the number of long chains odd. 
    #       2) The second player should play to make the number of long chains even. 

    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------
    
    # t1 = time.time()
    count = count_chains(state)
    # t2 = time.time()

    if num_rows % 2 != 0 or num_cols % 2 != 0:
        if count % 2 == 0 and maximizing_player_id == 0: # als de max speler de eerste speler was.
                heuristic *= 2
                return heuristic
        elif count % 2 == 0 and maximizing_player_id == 1:
                heuristic /= 2
                return heuristic
        elif count % 2 != 0 and maximizing_player_id == 1: 
                heuristic *= 2
                return heuristic
        elif count % 2 != 0 and maximizing_player_id == 0: 
                heuristic /= 2
                return heuristic
    
    elif num_rows % 2 == 0 and num_cols % 2 == 0:        
        if count % 2 != 0 and maximizing_player_id == 0: 
                heuristic *= 2
                return heuristic
        elif count % 2 != 0 and maximizing_player_id == 1: 
                heuristic /= 2
                return heuristic
        elif count % 2 == 0 and maximizing_player_id == 0: 
                heuristic /= 2
                return heuristic
        elif count % 2 == 0 and maximizing_player_id == 1:
                heuristic *= 2
                return heuristic

    return heuristic

@deprecated
def count_chains(state):
    """
    Count the amount of long chains in a state.
    Arguments:
      state: The current state node of the game.
    Returns:
        The amount of chains in the state.
    """
    count_chains = 0
    chain_list = []
    
    num_rows = state.get_game().get_parameters()['num_rows']
    num_cols = state.get_game().get_parameters()['num_cols']

    for box_num in range(num_cols * num_rows):
        flag = False
        for chain in chain_list:
            if box_num in chain:
                flag = True
                break
        
        if not flag:
            chain_list.append([box_num])
            add_chain(state, chain_list, box_num)

    for chain in chain_list:
        if len(chain) >= 3:
            count_chains += 1

    return count_chains

@deprecated
def add_chain(state, chain_list, box_num):
    """
    Add chains to the chain_list in the given state.
    Arguments:
        state: The current state node of the game.
        chain_list: The list of chains.
        box_num: The box number.

    Returns:
        None
    """ 
    num_rows = state.get_game().get_parameters()['num_rows']
    num_cols = state.get_game().get_parameters()['num_cols']
    state_tensor = game_state_tensor(state)

    neigh_nums = [box_num - 1, box_num - num_cols, box_num + 1 , box_num + num_cols]

    for i in range(len(neigh_nums)):
        # Ensure that the neighbour is on the board or if it is in the same row as the current box for the 'left' and 'right' positions.
        if (
            neigh_nums[i] < 0 
            or neigh_nums[i] > num_cols * num_rows 
            or (i % 2 == 0 and neigh_nums[i] // num_cols != box_num // num_cols)):
                continue
        
        flag = False
        # Check if the neighbour is already in a chain.
        for chain in chain_list:
            if neigh_nums[i] in chain:
                flag = True
                break

        # Check if there is a between the current box and a vertical neighbour, if not add the neighbor to the chain and
        # call the function recursively on the neighbor.
        if not flag and i % 2 == 0:
            if not is_vedge_present(state,vvector_for_tensor(state_tensor), box_num, neigh_nums[i]):
                chain_list[-1].append(neigh_nums[i])
                add_chain(state, chain_list, neigh_nums[i])

        # Check if there is a between the current box and a horizootal neighbour, if not add the neighbor to the chain and
        # call the function recursively on the neighbor.
        if not flag and i % 2 != 0:
            if not is_hedge_present(state,hvector_for_tensor(state_tensor), box_num, neigh_nums[i]):
                chain_list[-1].append(neigh_nums[i])
                add_chain(state, chain_list, neigh_nums[i])

@deprecated
def game_state_tensor(state):
    state_info = state.observation_tensor()
    num_rows = state.get_game().get_parameters()['num_rows']
    num_cols = state.get_game().get_parameters()['num_cols']
    num_dots= ((1 + num_rows) * (1 + num_cols))

    np_state_info = np.array(state_info)
    state_matrix = np_state_info.reshape(3, num_dots, 3)
    
    return state_matrix

@deprecated
def pvector_for_tensor(tensor):
    p = np.zeros(len(tensor[0]))

    # Player 1
    for i in range(len(tensor[1])):
        if tensor[1][i][2] == 1:
            p[i] = 1

    # Player 2
    for i in range(len(tensor[2])):
        if tensor[2][i][2] == 1:
            p[i] = 2
    return p

@deprecated
def vvector_for_tensor(tensor):
    v = np.zeros(len(tensor[0]))

    # Player 1
    for i in range(len(tensor[1])):
        if tensor[1][i][1] == 1:
            v[i] = 1

    # Player 2
    for i in range(len(tensor[2])):
        if tensor[2][i][1] == 1:
            v[i] = 2
    return v

@deprecated
def hvector_for_tensor(tensor):
    h = np.zeros(len(tensor[0]))

    # Player 1
    for i in range(len(tensor[1])):
        if tensor[1][i][0] == 1:
            h[i] = 1

    # Player 2
    for i in range(len(tensor[2])):
        if tensor[2][i][0] == 1:
            h[i] = 2
    return h

@deprecated
def box_state_for_pvector(pvector, nrows, ncols):
    pmatrix = pvector.reshape(nrows+1, ncols+1)
    result = pmatrix[:-1, :-1].ravel()

    return result

@deprecated
def box_to_dot(boxnum, state):
    """
    Returns the dot number of the upper left corner of the given box number.
    """
    num_cols = state.get_game().get_parameters()['num_cols']

    row = boxnum // num_cols
    col = boxnum % num_cols

    dot = row * (num_cols + 1) + col
    return dot

@deprecated
def is_vedge_present(state,v_vector, box1, box2):
    """
    Checks if there is a vertical edge present between given boxes.
    """
    i = max(box1, box2)
    return v_vector[box_to_dot(i,state)] != 0

@deprecated
def is_hedge_present(state,h_vector, box1, box2):
    """
    Checks if there is a horizontal edge present between given boxes.
    """
    i = max(box1, box2)
    return h_vector[box_to_dot(i,state)] != 0
