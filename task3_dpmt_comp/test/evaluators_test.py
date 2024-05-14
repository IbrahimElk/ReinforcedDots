import os
import sys
import unittest
import pyspiel
import MARL.task3.test.pyspiel_examples as ex

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, parent_dir)

import source.evaluators as ev

class TestEvaluators(unittest.TestCase):
    def test_eval_function_difference_singleton(self):
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

    def test_eval_function_chains_singleton(self):
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
        
        val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        self.assertEqual(val, -1)

        val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, 0)

        # add vertical line
        initial_state.apply_action(4)
        print("state")
        print(initial_state)

        val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        self.assertEqual(val, -2)
        
        val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, -1)

        # add horizontal line
        initial_state.apply_action(2)
        print("state")
        print(initial_state)

        val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        self.assertEqual(val, 0)

        val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, -1)

        # add vertical line
        initial_state.apply_action(7)
        print("state")
        print(initial_state)

        val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        self.assertEqual(val, -1) 
        
        val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, 0)

        # add vertical line
        initial_state.apply_action(9)
        print("state")
        print(initial_state)

        val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        self.assertEqual(val, 0)

        val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, -1)

        initial_state.apply_action(6)
        print("state")
        print(initial_state)

        val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        self.assertEqual(val, 0 )

        val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        self.assertEqual(val, -1)

    def test_eval_function_chains_example_paper(self):
        num_rows = 3
        num_cols = 6
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)

        initial_state = game.new_initial_state()
        maximizing_player_id = initial_state.current_player()

        ex.example_paper(initial_state)
        
        print("state")
        print(initial_state)

        print("initial_state.current_player()")
        print(initial_state.current_player())

        val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        print(f"eval value for max player {1 + maximizing_player_id} : {val}")
        self.assertEqual(val, 1) # IS NIET NUL WEGENS DIE EXTRA CHAIN RULE!! ONDANKS GEEN BOXES GECAPTURED. 

        val = ev.eval_function_chains(initial_state, 1- maximizing_player_id)
        print(f"eval value for max player {1 + ( 1 - maximizing_player_id)}  : {val}") 
        self.assertEqual(val, -1)  

        # add vertical line
        initial_state.apply_action(27)
        print("state")
        print(initial_state)

        print("current player")
        print(initial_state.current_player() + 1)

        val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        print(f"eval value for max player {1 + maximizing_player_id} : {val}")
        self.assertEqual(val, 0) 

        val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        print(f"eval value for max player {1 + ( 1 - maximizing_player_id)}  : {val}") 
        self.assertEqual(val, 0)

        # # add horizontal line
        # initial_state.apply_action(28)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # print(f"eval value for max player {1 + maximizing_player_id} : {val}")
        # self.assertEqual(val, -2)

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # print(f"eval value for max player {1 + ( 1 - maximizing_player_id)}  : {val}") 
        # self.assertEqual(val, 2)

        # add vertical line
        # initial_state.apply_action(29)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -3) 
        
        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 3) 
        # # add vertical line
        # initial_state.apply_action(11)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -5)

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 5)

        # initial_state.apply_action(17)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -7)

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 7)

        # initial_state.apply_action(6)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -8)

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 8)

        # initial_state.apply_action(12)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -9)

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 9)

        # initial_state.apply_action(39)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -10)

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 10)

        # initial_state.apply_action(40)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -11)

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 11)

        # initial_state.apply_action(42)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -10)

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 10)

        # initial_state.apply_action(41)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -8)

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 8)

        # initial_state.apply_action(1)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -9 )

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 9)

        # initial_state.apply_action(7)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -10 )

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 10)

        # initial_state.apply_action(33)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -11 )

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 11) 

        # initial_state.apply_action(34)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -12 )

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 12)

        # initial_state.apply_action(35)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -12 )

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 12)

        # initial_state.apply_action(16)
        # print("state")
        # print(initial_state)

        # print("initial_state.current_player()")
        # print(initial_state.current_player())
        
        # print("maximizing_player_id")
        # print(maximizing_player_id)

        # val = ev.eval_function_chains(initial_state, maximizing_player_id) 
        # self.assertEqual(val, -13 )

        # val = ev.eval_function_chains(initial_state, 1- maximizing_player_id) 
        # self.assertEqual(val, 13)

if __name__ == '__main__':
    unittest.main()