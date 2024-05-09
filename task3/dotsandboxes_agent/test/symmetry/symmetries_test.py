import os
import sys
import unittest
import pyspiel

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, parent_dir)

import chains.pyspiel_examples as exp
from symmetry.symmetries import _find_all_symmetries

class TestSymmetries(unittest.TestCase):
    #      *----*
    #  	        |
    #      *----*
    def test_symmetries_single_singleton(self):
        num_rows = 1
        num_cols = 1

        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)

        initial_state = game.new_initial_state()
        exp.single_singleton(initial_state)

        # includes itself:
        symmetric_dbn_states = _find_all_symmetries(initial_state, num_rows, num_cols)

        self.assertSetEqual(set(symmetric_dbn_states), set(["0111", "1011", "1110", "1101"]))


    #      *----*----*
    #  	   |         |  
    #      *----*----*
    def test_symmetries_single_doubleton(self):
        num_rows = 1
        num_cols = 2

        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        initial_state = game.new_initial_state()

        exp.single_doubleton(initial_state)

        # includes itself:
        symmetric_dbn_states = _find_all_symmetries(initial_state, num_rows, num_cols)

        self.assertSetEqual(set(symmetric_dbn_states), set(["1111101"]))


    #      *----*
    #  	   |    |
    #      * 	*
    #  	   |    |
    #  	   *    *
    def test_symmetries_vertical_half_open_chain(self):
        num_rows = 2
        num_cols = 1
        
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)

        initial_state = game.new_initial_state()
        exp.vertical_half_open_chain(initial_state)

        # includes itself:
        symmetric_dbn_states = _find_all_symmetries(initial_state, num_rows, num_cols)
        # print(set(symmetric_dbn_states))
        self.assertSetEqual(set(symmetric_dbn_states), set(["1001111","0011111"]))

if __name__ == '__main__':
    unittest.main()