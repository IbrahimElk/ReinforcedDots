import os
import sys
import pyspiel
import numpy as np
from .. import chains

package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_directory)

from transposition_table import TTable
# from minimax.chains_minimax import chain_heuristic

# FIXME:
# HOW TO DRAW THE GAME TREE IN TERMINAL. 
# TO CHECK....

# TODO: output of evaluation function should it consider the output space of the terminal states? 
# I don't think so.
def eval_function(state, maximizing_player_id): 
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

    # normalize the points to [-1 , 1] region?  
    total_amnt_boxes = num_rows * num_cols

    if player == maximizing_player_id:
        return points_player/total_amnt_boxes
    else :
        return (total_amnt_boxes - (points_empty + points_player))/total_amnt_boxes

def _alpha_beta(state, depth, alpha, beta, value_function,
                maximizing_player_id, cache:TTable):

    if state.is_terminal():
        return state.player_return(maximizing_player_id), None
    
    # FIXME: zie MCTS, eval functie verandert, de huidige eval functie is a bad one. 
    # en mag niet gebruikt worden opt einde. 
    if depth == 0:
        return value_function(state, maximizing_player_id), None

    player = state.current_player()

    # transpostion table
    # FIXME: moet de val aangepast worden voor max of min speler, ik denk het niet
    # zie ook paper: "Solving Dots-And-Boxes" , maar niet zeker. 
    data = cache.get(state)
    if data != None:
        # FIXME: is this correct way  ?
        val , action = data 
        return val, action

    best_action = -1
    if player == maximizing_player_id:
        value = -float("inf")
        for action in state.legal_actions():
            child_state = state.clone()
            child_state.apply_action(action)
            child_value, _  = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id, cache)
            if child_value > value:
                value = child_value
                best_action = action
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut-off
        
        # transpostion table
        cache.set(state, value, best_action)

        return value, best_action
    else:
        value = float("inf")
        for action in state.legal_actions():
            child_state = state.clone()
            child_state.apply_action(action)
            child_value, _  = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id, cache)
            if child_value < value:
                value = child_value
                best_action = action
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cut-off
        
        # transpostion table
        cache.set(state, value, best_action)

        return value, best_action

def minimax_alphabeta_search(game,
                            transposition_table:TTable,
                            state=None,
                            value_function=None,
                            maximum_depth=10,
                            maximizing_player_id=None):
    #TODO: value_function wordt gehardcoded hier naar de chain evaluation function.
    """ functie met alles der op en der aan (van optimisaties) """

    game_info = game.get_type()

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
    
    # FIXME: no need for initial matrix to be stored in transposition table ?

    return _alpha_beta(
        state.clone(),
        maximum_depth,
        alpha=-float("inf"),
        beta=float("inf"),
        value_function=chains.eval_function_chains,
        maximizing_player_id=maximizing_player_id,
        cache=transposition_table)

def main():
    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    num_rows = 1
    num_cols = 1
    game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)
    
    value, _ = minimax_alphabeta_search(game)

    if value == 0:
        print("It's a draw")
    else:
        winning_player = 1 if value == 1 else 2
        print(f"Player {winning_player} wins.")
 

if __name__ == "__main__":
    main()
