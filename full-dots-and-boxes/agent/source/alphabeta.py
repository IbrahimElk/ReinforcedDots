"""
This module implements the Minimax algorithm with alpha-beta pruning 
and transposition table optimization for a 2-player, 
perfect information, turn-based, deterministic, zero-sum game.

Author: Ibrahim El Kaddouri
April - 2024
"""

import os
import sys
import pyspiel
import numpy as np

package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_directory)

from transposition_table import TOptimised_Table, Transposition_Table_Chains
from chains_strategy import StrategyAdvisor
from evaluators import eval_maximize_difference

import pstats
import cProfile
# from memory_profiler import profile

def _alpha_beta(state, depth, alpha, beta, value_function,
                maximizing_player_id, 
                cache:TOptimised_Table,
                cache_chains:Transposition_Table_Chains, 
                SA:StrategyAdvisor):
    """
    Recursively applies the Minimax algorithm with alpha-beta pruning to evaluate the best move in a game.

    Args:
        state (pyspiel.State): The current state of the game.
        depth (int): The maximum search depth.
        alpha (float): The best value that the maximizing player can guarantee so far.
        beta (float): The best value that the minimizing player can guarantee so far.
        value_function (callable): A function that evaluates the state of the game for a given player.
        maximizing_player_id (int): The ID of the maximizing player.
        cache (TOptimised_Table): A transposition table used to cache previously evaluated game states.
        cache_chains (Transposition_Table_Chains): A transposition table for storing chains.
        SA (StrategyAdvisor): An advisor that provides strategies for the current game state.

    Returns:
        float: The evaluated value of the game state, the minmax value
    """   
    if state.is_terminal():
        return state.player_return(maximizing_player_id)

    if depth <= 0:
        return value_function(state, maximizing_player_id, SA)
    
    val = cache.get(state, state.current_player())
    if val:
        return val
    
    possible_actions = SA.get_available_action(state, cache_chains, maximizing_player_id)

    player = state.current_player()
    if player == maximizing_player_id:
        value = -float("inf")
        for action in possible_actions:
            child_state = state.clone()
            child_SA = SA.clone()

            child_state.apply_action(action)
            child_SA.update_action(action, state.current_player())

            child_value = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id, cache, cache_chains, child_SA)

            if child_value > value:
                value = child_value
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut-off
 
        # transpostion table
        cache.set(state, state.current_player(), value)
        return value
    
    else:
        value = float("inf")
        for action in possible_actions:
            child_state = state.clone()
            child_SA = SA.clone()

            child_state.apply_action(action)
            child_SA.update_action(action, state.current_player())
            
            child_value  = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id, cache, cache_chains, child_SA)
            
            if child_value < value:
                value = child_value
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cut-off

        # transpostion table
        cache.set(state, state.current_player(), value)
        return value

# @profile
def minimax_alphabeta_search(game,
                            transposition_table:TOptimised_Table,
                            transposition_table_chains:Transposition_Table_Chains,
                            strategy_advisor:StrategyAdvisor,
                            state=None,
                            value_function=None,
                            maximum_depth=10,
                            maximizing_player_id=None):
    """
    Perform Minimax search with alpha-beta pruning and transposition table optimization to find the best move
    in a 2-player, perfect information, deterministic game.

    Args:
        game (pyspiel.Game): The game object that provides game mechanics.
        transposition_table (TOptimised_Table): A transposition table used for caching game states.
        transposition_table_chains (Transposition_Table_Chains): A transposition table used for storing chains.
        strategy_advisor (StrategyAdvisor): An advisor that provides strategies for the current game state.
        state (pyspiel.State, optional): The current state of the game. If not provided, the initial state will be used.
        value_function (callable, optional): A function to evaluate the game state for a given player. If not
            provided, a default evaluation function will be used.
        maximum_depth (int): The maximum depth of the search tree.
        maximizing_player_id (int, optional): The ID of the maximizing player. If not provided, the current
            player in the state will be used.

    Returns:
        tuple: A tuple containing:
            - value (float): The evaluated value of the best move, minmax value.
            - best_action (Action): The best action to take based on the search.
    
    Raises:
        ValueError: If the game is not a 2-player, deterministic, perfect-information, zero-sum, sequential game.
    """
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
    
    possible_actions = strategy_advisor.get_available_action(state, transposition_table_chains, maximizing_player_id)
    
    value = -float("inf")
    for action in possible_actions:
        child_state = state.clone()
        child_SA = strategy_advisor.clone()

        child_state.apply_action(action)
        child_SA.update_action(action, state.current_player())
        
        child_value = _alpha_beta(
                        child_state,
                        maximum_depth-1,
                        alpha=-float("inf"),
                        beta=float("inf"),
                        value_function=value_function,
                        maximizing_player_id=maximizing_player_id,
                        cache=transposition_table,
                        cache_chains = transposition_table_chains,
                        SA=child_SA.clone())
        
        if child_value > value:
            value = child_value
            best_action = action  

    return value, best_action

def main():
    num_rows = 7
    num_cols = 7
    game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
    # print("Creating game: {}".format(game_string))

    game = pyspiel.load_game(game_string)
    state = game.new_initial_state()
    SA = StrategyAdvisor(num_rows, num_cols)
    max_allowed_depth = 1000

    maximizing_player_id = state.current_player()

    TT = TOptimised_Table(num_rows, num_cols)
    TTC = Transposition_Table_Chains()

    value, best_action = minimax_alphabeta_search(game=game,
                                        transposition_table=TT, 
                                        transposition_table_chains=TTC,
                                        strategy_advisor=SA,
                                        maximum_depth=max_allowed_depth,
                                        value_function=eval_maximize_difference, # can be changed to eval_chain
                                        state=state.clone())

    # print("next recommended action: ")
    # print(SA.get_tabular_form(best_action))  

    # print("the minimax value")
    # print(value)  

    # print("Applying the recommended action to the state")
    # state.apply_action(best_action, )
    # print(state)

if __name__ == "__main__":
    # with cProfile.Profile() as profile: 
    main() 
    
    # results = pstats.Stats(profile)
    # results.sort_stats(pstats.SortKey.TIME)
    # results.print_stats()
    # results.dump_stats("results.prof")
