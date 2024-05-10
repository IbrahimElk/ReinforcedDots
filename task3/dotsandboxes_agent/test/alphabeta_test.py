import os
import sys
import unittest
import pyspiel
import random as r

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, parent_dir)

from chains.chains_strategy import StrategyAdvisor
from transposition_table import TOptimised_Table
from alphabeta import minimax_alphabeta_search
from evaluators import eval_maximize_difference
import chains.pyspiel_examples as exp
import chains.examples as ex
from chains.util import CellOrientation
from symmetry.util import dbn_to_vectors

# TODO: gegeven de voorbeelden, predict het de juiste volgende actie.
# checken of de juiste persoon heeft gewonnen. 

class TestAlphaBeta(unittest.TestCase):
    def test_alphabeta_single_singleton(self):
        games_list = pyspiel.registered_names()
        assert "dots_and_boxes" in games_list

        # x = r.randint(1, 10)
        # y = r.randint(1, 10)

        num_rows = 2
        num_cols = 2
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        state = game.new_initial_state()
        SA = StrategyAdvisor(num_rows, num_cols)
        allowed_depth = 8

        exp.single_singleton(state)
        ex.single_singleton_2x2(SA)

        maximizing_player_id = state.current_player()

        TT = TOptimised_Table()
        value, best_action = minimax_alphabeta_search(game=game,
                                            state=state,
                                            transposition_table=TT, 
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
        state.apply_action(best_action, )
        print(state)

        self.assertEqual(best_action, SA.action_id(CellOrientation.VERTICAL, 0, 0))

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

    # def test_alphabeta_example_paper(self):
    #     games_list = pyspiel.registered_names()
    #     assert "dots_and_boxes" in games_list

    #     # x = r.randint(1, 10)
    #     # y = r.randint(1, 10)

    #     num_rows = 3
    #     num_cols = 6
    #     game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    #     print("Creating game: {}".format(game_string))
    #     game = pyspiel.load_game(game_string)
    #     state = game.new_initial_state()
    #     SA = StrategyAdvisor(num_rows, num_cols)
    #     allowed_depth = 1

    #     exp.example_paper(state)
    #     ex.example_paper(SA)

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

    #     self.assertEqual(best_action, SA.action_id(CellOrientation.VERTICAL, 0, 3))

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