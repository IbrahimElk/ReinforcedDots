import os
import sys
import pyspiel
import numpy as np

package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_directory)

from transposition_table import TOptimised_Table
from chains.chains_strategy import StrategyAdvisor
from evaluators import eval_maximize_difference
from chains import eval_function_chains

def _alpha_beta(state, depth, alpha, beta, value_function,
                maximizing_player_id, cache:TOptimised_Table, SA:StrategyAdvisor):
    
    if state.is_terminal():
        return state.player_return(maximizing_player_id)

    if depth <= 0:
        heuristic = value_function(state, maximizing_player_id)
        return heuristic

    val = cache.get(state)
    if val:
        return val

    possible_actions = SA.get_available_action(state)

    player = state.current_player()
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
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut-off
        
        # transpostion table
        cache.set(state, value)
        return value
    
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
                        maximum_depth-1,
                        alpha=-float("inf"),
                        beta=float("inf"),
                        value_function=value_function,
                        maximizing_player_id=maximizing_player_id,
                        cache=transposition_table,
                        SA=child_SA.clone())
        
        if child_value > value:
            value = child_value
            best_action = action  

    return value, best_action

def main():
    num_rows = 7
    num_cols = 7
    game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)
    state = game.new_initial_state()
    SA = StrategyAdvisor(num_rows, num_cols)
    max_allowed_depth = 50

    maximizing_player_id = state.current_player()

    TT = TOptimised_Table()
    value, best_action = minimax_alphabeta_search(game=game,
                                        transposition_table=TT, 
                                        strategy_advisor=SA,
                                        maximum_depth=max_allowed_depth,
                                        # TODO: can be changed to eval_maximize_difference
                                        value_function=eval_maximize_difference,
                                        state=state.clone())

    print("next recommended action: ")
    print(SA.get_tabular_form(best_action))  

    print("the minimax value")
    print(value)  

    if value > 0 :
        print(f"In the simulation, Player {maximizing_player_id + 1} wins.")
    elif value < 0 : 
        print(f"In the simulation, Player {maximizing_player_id} wins.")
    else : 
        print("In the simulation, It's a draw")

    print("Applying the recommended action to the state")
    state.apply_action(best_action, )
    print(state)


if __name__ == "__main__":
    main()
