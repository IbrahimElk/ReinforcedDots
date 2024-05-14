import os
import sys
import unittest
import pyspiel
import random as r
import numpy  as np
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, parent_dir)

from source.chains_strategy import StrategyAdvisor
from source.transposition_table import TOptimised_Table, Transposition_Table_Chains
from source.alphabeta import minimax_alphabeta_search
from source.evaluators import eval_maximize_difference
import pyspiel_examples as exp
import examples as ex
from source.util import CellOrientation, dbn_to_vectors

# TODO: gegeven de voorbeelden, predict het de juiste volgende actie.
# checken of de juiste persoon heeft gewonnen. 

class TestAlphaBeta(unittest.TestCase):
    # def test_alphabeta_single_singleton(self):
    #     games_list = pyspiel.registered_names()
    #     assert "dots_and_boxes" in games_list

    #     # x = r.randint(1, 10)
    #     # y = r.randint(1, 10)

    #     num_rows = 2
    #     num_cols = 2
    #     game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    #     print("Creating game: {}".format(game_string))
    #     game = pyspiel.load_game(game_string)
    #     state = game.new_initial_state()
    #     SA = StrategyAdvisor(num_rows, num_cols)
    #     allowed_depth = 8

    #     exp.single_singleton(state)
    #     ex.single_singleton_2x2(SA)

    #     maximizing_player_id = state.current_player()

    #     TT = TOptimised_Table()
    #     value, best_action = minimax_alphabeta_search(game=game,
    #                                         state=state,
    #                                         transposition_table=TT, 
    #                                         strategy_advisor=SA,
    #                                         maximum_depth=allowed_depth,
    #                                         value_function=eval_maximize_difference)

    #     print("next recommended action: ")
    #     print(best_action)  

    #     print("the minimax value")
    #     print(value)  

    #     if value > 0 :
    #         print(f"Player {maximizing_player_id + 1} wins.")
    #     elif value < 0 : 
    #         print(f"Player {maximizing_player_id} wins.")
    #     else : 
    #         print("It's a draw")
    
    #     print("Applying the recommended action to the state")
    #     state.apply_action(best_action, )
    #     print(state)

    #     self.assertEqual(best_action, SA.action_id(CellOrientation.VERTICAL, 0, 0))

    # def test_alphabeta_debug_example1(self):
    #     games_list = pyspiel.registered_names()
    #     assert "dots_and_boxes" in games_list

    #     # x = r.randint(1, 10)
    #     # y = r.randint(1, 10)

    #     num_rows = 2
    #     num_cols = 2
    #     game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    #     print("Creating game: {}".format(game_string))
    #     game = pyspiel.load_game(game_string)
    #     state = game.new_initial_state()
    #     SA = StrategyAdvisor(num_rows, num_cols)
    #     allowed_depth = 1

    #     exp.debug_example1(state)
    #     ex.debug_example1(SA)

    #     maximizing_player_id = state.current_player()
        
    #     TT = TOptimised_Table()
    #     value, best_action = minimax_alphabeta_search(game=game,
    #                                         state=state,
    #                                         transposition_table=TT, 
    #                                         strategy_advisor=SA,
    #                                         maximum_depth=allowed_depth,
    #                                         value_function=eval_maximize_difference)

    #     print("next recommended action: ")
    #     print(best_action)  

    #     print("the minimax value")
    #     print(value)  

    #     if value > 0 :
    #         print(f"Player {maximizing_player_id + 1} wins.")
    #     elif value < 0 : 
    #         print(f"Player {maximizing_player_id} wins.")
    #     else : 
    #         print("It's a draw")
    
    #     print("Applying the recommended action to the state")
    #     state.apply_action(best_action, )
    #     print(state)

    #     self.assertEqual(best_action, SA.action_id(CellOrientation.VERTICAL, 1, 1))

    def test_alphabeta_example_paper(self):
        games_list = pyspiel.registered_names()
        assert "dots_and_boxes" in games_list

        # x = r.randint(1, 10)
        # y = r.randint(1, 10)

        num_rows = 3
        num_cols = 6
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        state = game.new_initial_state()
        SA = StrategyAdvisor(num_rows, num_cols)
        allowed_depth = 9

        exp.example_paper(state)
        ex.example_paper(SA)

        obs_tensor = state.observation_tensor()
        obs_tensor = np.array(obs_tensor)

        SA.update_action(6, state.current_player())
        state.apply_action(6)

        SA.update_action(12, state.current_player())
        state.apply_action(12)
        
        SA.update_action(39, state.current_player())
        state.apply_action(39)
        
        SA.update_action(40, state.current_player())
        state.apply_action(40)
        
        SA.update_action(41, state.current_player())
        state.apply_action(41)
        
        SA.update_action(42, state.current_player())
        state.apply_action(42)

        state.apply_action(27)
        SA.update_action(27, state.current_player())
        
        state.apply_action(28)
        SA.update_action(28, state.current_player())

        maximizing_player_id = state.current_player()
        
        TT = TOptimised_Table(num_rows, num_cols)
        TTC = Transposition_Table_Chains()
        value, best_action = minimax_alphabeta_search(game=game,
                                            state=state,
                                            transposition_table=TT, 
                                            transposition_table_chains=TTC,
                                            strategy_advisor=SA,
                                            maximum_depth=allowed_depth,
                                            value_function=eval_maximize_difference)

        print("next recommended action: ")
        print(best_action)  

        print("the minimax value")
        print(value)  

        if value > 0 :
            print(f"Player {maximizing_player_id + 1} wins.")
        elif value < 0 : 
            print(f"Player {maximizing_player_id} wins.")
        else : 
            print("It's a draw")
    
        print("Applying the recommended action to the state")
        state.apply_action(best_action)
        print(state)

        self.assertEqual(best_action, SA.action_id(CellOrientation.HORIZONTAL, 1, 5))

# NOT HERE, in alpha beta test.
    # def test_which_eval_function_is_best(self):
    #     """
    #     use alpha beta search with each eval function, 
    #     on the examples provided in the file pyspiel_examples, 
    #     see what the recommended value and action could be. 

    #     the ideal action and value is known for these examples
    #     """
    #     # TODO: 
    #     pass

if __name__ == '__main__':
    unittest.main()