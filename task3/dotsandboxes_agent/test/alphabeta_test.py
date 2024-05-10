import os
import sys
import unittest
import pyspiel

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, parent_dir)

from chains.chains_strategy import StrategyAdvisor
from transposition_table import TOptimised_Table
from alphabeta import minimax_alphabeta_search
from evaluators import eval_maximize_difference
import chains.pyspiel_examples as ex

# TODO: gegeven de voorbeelden, predict het de juiste volgende actie.
# checken of de juiste persoon heeft gewonnen. 

class TestAlphaBeta(unittest.TestCase):
    def test_alphabeta_single_singleton(self):
        games_list = pyspiel.registered_names()
        assert "dots_and_boxes" in games_list
        num_rows = 3
        num_cols = 3
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        state = game.new_initial_state()
        ex.single_singleton(state)

        TT = TOptimised_Table()
        SA = StrategyAdvisor(num_rows,num_cols)
        value, action = minimax_alphabeta_search(game=game,
                                            state=state,
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
    
        state.apply_action(action)
        print(state)


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