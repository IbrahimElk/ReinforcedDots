import os
import sys
import unittest
import pyspiel
import chains.pyspiel_examples as ex

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, parent_dir)

import evaluators as ev

class TestEvaluators(unittest.TestCase):
    def test_eval_function_difference(self):
        num_rows = 3
        num_cols = 1
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)

        initial_state = game.new_initial_state()
        maximizing_player_id = initial_state.current_player()
        ex.single_singleton(initial_state)
        print("state")
        print(initial_state)
        
        val = ev.eval_maximize_difference(initial_state, maximizing_player_id) 
        self.assertEqual(val, 0)

        val = ev.eval_maximize_difference(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, 0)

        # add vertical line
        initial_state.apply_action(4)
        print("state")
        print(initial_state)

        val = ev.eval_maximize_difference(initial_state, maximizing_player_id) 
        self.assertEqual(val, -1)
        
        val = ev.eval_maximize_difference(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, 1)

        # add horizontal line
        initial_state.apply_action(2)
        print("state")
        print(initial_state)

        val = ev.eval_maximize_difference(initial_state, maximizing_player_id) 
        self.assertEqual(val, -1)

        val = ev.eval_maximize_difference(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, 1)

        # add vertical line
        initial_state.apply_action(7)
        print("state")
        print(initial_state)

        val = ev.eval_maximize_difference(initial_state, maximizing_player_id) 
        self.assertEqual(val, -1)
        
        val = ev.eval_maximize_difference(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, 1)

        # add vertical line
        initial_state.apply_action(9)
        print("state")
        print(initial_state)

        val = ev.eval_maximize_difference(initial_state, maximizing_player_id) 
        self.assertEqual(val, -1)

        val = ev.eval_maximize_difference(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, 1)

        initial_state.apply_action(6)
        print("state")
        print(initial_state)

        val = ev.eval_maximize_difference(initial_state, maximizing_player_id) 
        self.assertEqual(val, 0)

        val = ev.eval_maximize_difference(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, 0)


if __name__ == '__main__':
    unittest.main()