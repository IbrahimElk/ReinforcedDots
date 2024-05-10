import os
import sys
import pyspiel
import numpy as np

package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_directory)

from transposition_table import TOptimised_Table
from chains.chains_strategy import StrategyAdvisor
from evaluators import eval_maximize_difference
# FIXME: draw game tree to see if it makes sense. 
# TODO: output of evaluation function, should it consider the output space of the terminal states? 

def _alpha_beta(state, depth, alpha, beta, value_function,
                maximizing_player_id, cache:TOptimised_Table, SA:StrategyAdvisor):
    
    if state.is_terminal():
        return state.player_return(maximizing_player_id)
    
    if depth == 0:
        return value_function(state, maximizing_player_id)

    val = cache.get(state)
    if val:
        return val

    possible_actions = SA.get_available_action(state)

    player = state.current_player()
    best_action = -1
    if player == maximizing_player_id:
        value = -float("inf")
        for action in possible_actions:
            child_state = state.clone()
            child_SA = SA.clone()

            child_state.apply_action(action)
            child_SA.update_action(action)

            child_value = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id, cache, child_SA)
            if child_value > value:
                value = child_value
                best_action = action
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut-off
        
        # transpostion table
        cache.set(state, value)
        return value, best_action
    
    else:
        value = float("inf")
        for action in possible_actions:
            child_state = state.clone()
            child_SA = SA.clone()

            child_state.apply_action(action)
            child_SA.update_action(action)

            child_value  = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id, cache, child_SA)
            if child_value < value:
                value = child_value
                best_action = action
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cut-off
        
        # transpostion table
        cache.set(state, value)
        return value

def minimax_alphabeta_search(game,
                            transposition_table:TOptimised_Table,
                            strategy_advisor:StrategyAdvisor,
                            state=None,
                            value_function=None,
                            maximum_depth=10,
                            maximizing_player_id=None):
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
    
    
    possible_actions = strategy_advisor.get_available_action(state)

    value = -float("inf")
    for action in possible_actions:
        child_state = state.clone()
        child_SA = strategy_advisor.clone()

        child_state.apply_action(action)
        child_SA.update_action(action)

        child_value = _alpha_beta(
                        child_state,
                        maximum_depth,
                        alpha=-float("inf"),
                        beta=float("inf"),
                        value_function=value_function,
                        maximizing_player_id=maximizing_player_id,
                        cache=transposition_table,
                        strategy_advisor=strategy_advisor.clone())
        
        if child_value > value:
            value = child_value
            best_action = action  

    return value, best_action

def main():
    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    num_rows = 3
    num_cols = 3
    game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)
    
    TT = TOptimised_Table()
    SA = StrategyAdvisor(num_rows,num_cols)
    value, action = minimax_alphabeta_search(game=game,
                                        transposition_table=TT, 
                                        strategy_advisor=SA,
                                        value_function=eval_maximize_difference)

    print("next recommended action: ")
    print(action)    

    if value == 0:
        print("It's a draw")
    else:
        winning_player = 1 if value == 1 else 2
        print(f"Player {winning_player} wins.")
 

if __name__ == "__main__":
    main()
