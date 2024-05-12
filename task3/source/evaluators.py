import numpy as np

"""
Chains are sequences of one or more capturable boxes ("corridors").

2 kinds of chains exist:
    1. half-open chains: only one end of chain is capturable. (= corridor with 3 edges filled in)
    2. closed chains: both ends of chain are capturable.      (= corridor with 4 edges filled in)

Most moves on a state with chains are suboptimal, using this knowledge can reduce the branching 
factor of the game tree.

Half-open chains, only 2 moves are part of a optimal strategy:
    1.  Capture every available box in that chain and make an additional move.
    2.  Capture all but 2 boxes in that chain and fill in the end of the chain.
        This creates a hard-hearted handout.

Closed chains, only 2 moves is part of a optimal strategy:
    1.  Capture every available box in that chain and make an additional move.
    2.  Capture all but 4 boxes in that chain and fill in the edge that separates it in 
        2 hard-hearted handouts.

More than 1 chain available:
    1. Fill all but 1 available chains, and follow the above mentioned strategies for the remaining
        chain. If possible choose half-open chain as the last one. (Sacrifices only 2 instead of 4)
   

Stackoverflow:

The first is the double-cross strategy: The same double-cross strategy applies no 
matter how many long chains there are: a player using this strategy will take all 
but two boxes in each chain and take all the boxes in the last chain. If the chains 
are long enough, then this player will win. 

Second, the parity rule for long chains. This follows from three facts about the majority of well-played games:

    1.The long chains will be played out at the very end of the game.
    2.There will be a double cross in every chain except the last one.
    3.The player who first has to play in any long chain loses the game.

    
The third and most powerful observation is that dots and boxes is an impartial game: 
the available moves are the same regardless of whose turn it is to play, and in typical 
positions that arise in the course of play (that is, ones containing long chains of boxes) 
it's also a normal game: the last player to move wins. The combination of these properties 
means that positions can be analyzed statically using Sprague–Grundy theory.
"""

"""
Max player goes first, min player goes second.

For board m x n (boxes):
    if m and n are both even:
        max: amt long chains odd
    else:
        max: amt long chains even
"""


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


def eval_function_chains(state, maximizing_player_id):
    """
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

    current_player = state.current_player()
    
    boxes = box_state_for_pvector(pvector_for_tensor(game_state_tensor(state)), num_rows, num_cols)
    
    for box in boxes:
        # current_player == 0, dan betekent het dat deze agent als eerste heeft gestart. 
        # current_player == 1, dan betekent het dat deze agent als tweede heeft gestart.

        # maximizing_player_id, duidt aan of onze agent dan als eerste heeft gestart of niet. 

        # als current_player == maximizing_player_id 
        # case 1: 
        #      current_player == 0 en maximising_player_id == 0
        #      dus onze agent als eerste heeft gestart. 
    
        #      current_player == 1 en maximising_player_id == 1
        #      dus onze agent als tweede heeft gestart 
    
        #      box == 1, betekent dat de eerste agent deze box heeft gecapteert. 
        #      dus afhankelijk of wij de eeerste agent zijn of niet, kan dat voordelig zijn voor ons. 
        #      dit is niet in rekening genomen in de volgende if statement. 

        # if current_player == maximizing_player_id: (als dus current_player , onze agent is.)
        #     if box == 1: (dit klopt niet, want wij kunnen ook de agent zijn die als tweede starten, dus box == 2. )
        #         box_won += 1
        #         heuristic += 1
        #     elif box == 2:
        #         box_lost += 1
        #         heuristic -= 1
        # else:
        #     if box == 1:
        #         box_lost += 1
        #         heuristic -= 1
        #     elif box == 2:
        #         box_won += 1
        #         heuristic += 1

        # als de box die gecapteerd werd , door ons werd gedaan: 
        # box == 1, de agent met eerste zet heeft deze box gecapteert. 
        # maximising_plyer_id == 0, wij zijn de agent met de eerste zet. 
        if box == maximizing_player_id + 1: 
            box_won += 1
            heuristic += 1
        elif box != 0:
            box_lost += 1
            heuristic -= 1

        # TODO: 
        # das dan eig niet zo verschillend van eig gwn de difference te nemen van de boxes van beide spelers? 
        # gwn dan op iterative manier? 

    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------
    # Take long chain rule into account # math.ucla.edu/~tom/Games/dots&boxes_hints.html

    # The Long Chain Rule: Suppose the playing field is a rectangle of m rows and n columns and so has mn boxes. 
    # [1] If either m or n is odd, then 
    #       1)  the first player should play to make the number of long chains even.
    #           - als wij de eerste speler zijn, dan extra reward als dit voldaan is.
    #           - als wij de eerste speler zin, dan bestraffen als dit niet voldaan is. (kleiner waarde is beter voor min player, voor opponent)

    #       2) the second player should play to make the number of long chains oneven. 
    #           - als wij de tweede speler zijn, dan extra reward als dit voldaan is.
    #           - als wij de tweede speler zin, dan bestraffen als dit niet voldaan is. 
    # 
    # [2] If both m and n are even, then 
    #       1) The first player should play to make the number of long chains odd. 
    #           - als wij de eerste speler zijn, dan extra reward als dit voldaan is.
    #           - als wij de eerste speler zin, dan bestraffen als dit niet voldaan is.  

    #       2) The second player should play to make the number of long chains even. 
    #           - als wij de eerste speler zijn, dan extra reward als dit voldaan is.
    #           - als wij de eerste speler zin, dan bestraffen als dit niet voldaan is.

    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------
    if num_rows % 2 != 0 or num_cols % 2 != 0:
        if count_chains(state) % 2 == 0 and maximizing_player_id == 0: # als de max speler de eerste speler was.
                heuristic += 1
                return heuristic
        elif count_chains(state) % 2 == 0 and maximizing_player_id == 1:
                heuristic -= 1
                return heuristic
        elif count_chains(state) % 2 != 0 and maximizing_player_id == 1: 
                heuristic += 1
                return heuristic
        elif count_chains(state) % 2 != 0 and maximizing_player_id == 0: 
                heuristic -= 1
                return heuristic
 
    elif num_rows % 2 == 0 and num_cols % 2 == 0:        
        if count_chains(state) % 2 != 0 and maximizing_player_id == 0: 
                heuristic += 1
                return heuristic
        elif count_chains(state) % 2 != 0 and maximizing_player_id == 1: 
                heuristic -= 1
                return heuristic
        elif count_chains(state) % 2 == 0 and maximizing_player_id == 0: 
                heuristic -= 1
                return heuristic
        elif count_chains(state) % 2 == 0 and maximizing_player_id == 1:
                heuristic += 1
                return heuristic

    # if box_won >= 5:
    #     heuristic = np.inf
    # elif box_lost >= 5:
    #     heuristic = -np.inf

    #FIXME: kdenk dat ge altijd de result van volgens de maximizing player id teruggeven. 
    # (want de min player zal dan de min() nemen, en de max zal dan de max() nemen van die value berekent volgens de max player)  
    # if p == maximizing_player_id:
    #     return heuristic
    # else:
    #     return -1*heuristic
    return heuristic
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




def game_state_tensor(state):
    # TODO: wrm 0 ?
    # 0 of 1 heeft geen effect, observation_tensor(0) == observation_tensor(), denk ik, als ik zo kijk naar de c++ code.
    state_info = state.observation_tensor(0)
    num_rows = state.get_game().get_parameters()['num_rows']
    num_cols = state.get_game().get_parameters()['num_cols']
    num_dots= ((1 + num_rows) * (1 + num_cols))

    np_state_info = np.array(state_info)
    state_matrix = np_state_info.reshape(3, num_dots, 3)
    
    return state_matrix


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

def box_state_for_pvector(pvector, nrows, ncols):
    pmatrix = pvector.reshape(nrows+1, ncols+1)
    result = pmatrix[:-1, :-1].ravel()

    # ibr: met de delete was er iets mis. 
    # result = np.delete(pvector,np.arange(2,len(pvector),3))
    # result = np.delete(result,np.arange(len(result)-ncols,len(result)))
    return result

def box_to_dot(boxnum, state):
    """
    Returns the dot number of the upper left corner of the given box number.
    """
    num_cols = state.get_game().get_parameters()['num_cols']

    row = boxnum // num_cols
    col = boxnum % num_cols

    dot = row * (num_cols + 1) + col
    return dot

def is_vedge_present(state,v_vector, box1, box2):
    """
    Checks if there is a vertical edge present between given boxes.
    """
    i = max(box1, box2)
    return v_vector[box_to_dot(i,state)] != 0


def is_hedge_present(state,h_vector, box1, box2):
    """
    Checks if there is a horizontal edge present between given boxes.
    """
    i = max(box1, box2)
    return h_vector[box_to_dot(i,state)] != 0
