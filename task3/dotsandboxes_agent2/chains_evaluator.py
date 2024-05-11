import numpy as np
# import os 
# import sys

# current_dir = os.path.dirname(__file__)
# mdir = os.path.abspath(os.path.join(current_dir, os.pardir, "dotsandboxes_agent"))
# sys.path.append(mdir)

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
import pyspiel
from absl import app

def game_state_tensor(state):
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

def box_state_for_pvector(pvector, ncols):
    result = np.delete(pvector,np.arange(2,len(pvector),3))
    result = np.delete(result,np.arange(len(result)-ncols,len(result)))
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


def _minimax(state, maximizing_player_id,depth=6):
    """
    Implements a min-max algorithm
    Arguments:
      state: The current state node of the game.
      maximizing_player_id: The id of the MAX player. The other player is assumed
        to be MIN.

    Returns:
      The optimal value of the sub-game starting in state
    """
    if state.is_terminal() or depth == 0:
        return eval_function_chains(state,maximizing_player_id)
        
    player = state.current_player()

    if player == maximizing_player_id:
        selection = max
    else:
        selection = min
    values_children = [_minimax(state.child(action), maximizing_player_id,depth-1) for action in state.legal_actions()]
    return selection(values_children)


def eval_function_chains(state,maximizing_player_id):
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

    p = state.current_player()
    
    boxes = box_state_for_pvector(pvector_for_tensor(game_state_tensor(state)),state.get_game().get_parameters()['num_cols'])

    # Take box loss and win into account
    for box in boxes:
        if p == maximizing_player_id:
            if box == 1:
                box_won += 1
                heuristic += 1
            elif box == 2:
                box_lost += 1
                heuristic -= 1
        else:
            if box == 1:
                box_lost += 1
                heuristic -= 1
            elif box == 2:
                box_won += 1
                heuristic += 1

    # Take long chain rule into account # math.ucla.edu/~tom/Games/dots&boxes_hints.html
    if num_rows % 2 != 0 or num_cols % 2 != 0:
        if count_chains(state) % 2 == 0 and p == maximizing_player_id:
            heuristic += 1
        elif count_chains(state) % 2 != 0 and p != maximizing_player_id:
            heuristic += 1
    elif num_rows % 2 == 0 and num_cols % 2 == 0:
        if count_chains(state) % 2 != 0 and p == maximizing_player_id:
            heuristic += 1
        elif count_chains(state) % 2 == 0 and p != maximizing_player_id:
            heuristic += 1

    if box_won >= 5:
        heuristic = 9999
    elif box_lost >= 5:
        heuristic = -9999

    if p == maximizing_player_id:
        return heuristic
    else:
        return -1*heuristic

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

def heuristic_to_win(value):
    if value > 0:
        return 1
    elif value < 0:
        return 2
    else:
        return 0

def minimax_search(game,
                   state=None,
                   maximizing_player_id=None,
                   state_to_key=lambda state: state):
    """Solves deterministic, 2-players, perfect-information 0-sum game.

    For small games only! Please use keyword arguments for optional arguments.

    Arguments:
      game: The game to analyze, as returned by `load_game`.
      state: The state to run from.  If none is specified, then the initial state is assumed.
      maximizing_player_id: The id of the MAX player. The other player is assumed
        to be MIN. The default (None) will suppose the player at the root to be
        the MAX player.

    Returns:
      The value of the game for the maximizing player when both player play optimally.
    """
    game_info = game.get_type()

    num_cols = game.get_parameters()['num_cols']
    num_rows = game.get_parameters()['num_rows']

    edgesamt = num_cols * (num_rows + 1) + num_rows * (num_cols + 1)    #Barker solving dots&boxes

    if game.num_players() != 2:
        raise ValueError("Game must be a 2-player game")
    if game_info.chance_mode != pyspiel.GameType.ChanceMode.DETERMINISTIC:
        raise ValueError("The game must be a Deterministic one, not {}".format(
            game.chance_mode))
    if game_info.information != pyspiel.GameType.Information.PERFECT_INFORMATION:
        raise ValueError(
            "The game must be a perfect information one, not {}".format(
                game.information))
    if game_info.dynamics != pyspiel.GameType.Dynamics.SEQUENTIAL:
        raise ValueError("The game must be turn-based, not {}".format(
            game.dynamics))
    if game_info.utility != pyspiel.GameType.Utility.ZERO_SUM:
        raise ValueError("The game must be 0-sum, not {}".format(game.utility))

    if state is None:
        state = game.new_initial_state()
    if maximizing_player_id is None:
        maximizing_player_id = state.current_player()
    v = _minimax(
        state.clone(),
        maximizing_player_id=maximizing_player_id,depth=int(edgesamt/2))
    return heuristic_to_win(v)


def main(_):
    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    game_string = "dots_and_boxes(num_rows=2,num_cols=2)"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)

    value = minimax_search(game)

    if value == 0:
        print("It's a draw")
    else:
        winning_player = 1 if value == 1 else 2
        print(f"Player {winning_player} wins.")


if __name__ == "__main__":
    app.run(main)
