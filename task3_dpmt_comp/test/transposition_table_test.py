import os
import sys
import unittest
import pyspiel
import random as r
import MARL.task3.test.pyspiel_examples as ex

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)

import source.transposition_table as T 

class TestTransposition_Table(unittest.TestCase):
    def test_get_and_set(self):
        table = T.Transposition_Table()

        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(1, 10)
        y = r.randint(1, 10)

        num_rows = x
        num_cols = y
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
        game = pyspiel.load_game(game_string)

        state1 = game.new_initial_state()
        state2 = game.new_initial_state()

        value1 = 1
        value2 = 2

        table.set(state1, value1)
        self.assertEqual(table.get(state1), value1)

        table.set(state1, value2)
        self.assertEqual(table.get(state1), value2)

        
        state2.apply_action(0)
        self.assertIsNotNone(table.get(state1))
        self.assertIsNone(table.get(state2))

    def test_cache_hits_and_misses(self):
        table = T.Transposition_Table()
 
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(1, 10)
        y = r.randint(1, 10)

        num_rows = x
        num_cols = y
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
        game = pyspiel.load_game(game_string)

        state1 = game.new_initial_state()
        state2 = game.new_initial_state()
        state2.apply_action(0)
        value = "value"

        table.set(state1, value)

        table.get(state1)  # Hit
        table.get(state2)  # Miss
        table.get(state1)  # Hit
        table.get(state1)  # Hit

        self.assertEqual(table.get_hits(), 3)
        self.assertEqual(table.get_misses(), 1)

class TestTEmpty_Table(unittest.TestCase):
    def test_get_and_set(self):
        table = T.TEmpty_Table()
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(1, 10)
        y = r.randint(1, 10)

        num_rows = x
        num_cols = y
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
        game = pyspiel.load_game(game_string)

        state1 = game.new_initial_state()
        state2 = game.new_initial_state()

        value1 = 1
        value2 = 2

        table.set(state1, value1)
        self.assertIsNone(table.get(state1))

        table.set(state1, value2)
        self.assertIsNone(table.get(state1))

        state2.apply_action(0)
        self.assertIsNone(table.get(state1))
        self.assertIsNone(table.get(state2))

    def test_cache_hits_and_misses(self):
        table = T.TEmpty_Table()
        
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(1, 10)
        y = r.randint(1, 10)

        num_rows = x
        num_cols = y
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
        game = pyspiel.load_game(game_string)

        state1 = game.new_initial_state()
        state2 = game.new_initial_state()
        state2.apply_action(0)
        value = "value"

        table.set(state1, value)

        table.get(state1)  # Hit
        table.get(state2)  # Miss
        table.get(state1)  # Hit
        table.get(state1)  # Hit

        self.assertEqual(table.get_hits(), 0)
        self.assertEqual(table.get_misses(), 4)

class TestTOptimised_Table(unittest.TestCase):
    def test_get_and_set(self):
        table = T.TOptimised_Table()

        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(1, 10)
        y = r.randint(1, 10)

        num_rows = x
        num_cols = y

        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
        game = pyspiel.load_game(game_string)

        state1 = game.new_initial_state()
        state2 = game.new_initial_state()

        value1 = 1
        value2 = 2

        table.set(state1, value1)
        self.assertEqual(table.get(state1), value1)

        table.set(state2, value2)
        self.assertEqual(table.get(state1), value2)
        
        state2.apply_action(0)
        self.assertIsNotNone(table.get(state1))
        self.assertIsNone(table.get(state2))

    def test_cache_hits_and_misses(self):
        table = T.TOptimised_Table()

        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(1, 10)
        y = r.randint(1, 10)

        num_rows = x
        num_cols = y
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
        game = pyspiel.load_game(game_string)

        state1 = game.new_initial_state()
        state2 = game.new_initial_state()
        state2.apply_action(0)
        value = "value"

        table.set(state1, value)

        table.get(state1)  # Hit
        table.get(state2)  # Miss
        table.get(state1)  # Hit
        table.get(state1)  # Hit

        self.assertEqual(table.get_hits(), 3)
        self.assertEqual(table.get_misses(), 1)
    
    # horizontal_closed_chain is symmetrisch tegenover vertical_closed_chain
    def test_symmetries(self):
        table = T.TOptimised_Table()
        
        seed = None
        if seed:
            r.seed(seed)

        x = r.randint(4, 20)

        num_rows = x
        num_cols = x
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
        game1 = pyspiel.load_game(game_string)
        game2 = pyspiel.load_game(game_string)
        game3 = pyspiel.load_game(game_string)
        game4 = pyspiel.load_game(game_string)
        game5 = pyspiel.load_game(game_string)

        state1 = game1.new_initial_state()
        state2 = game2.new_initial_state()
        state3 = game3.new_initial_state()
        state4 = game4.new_initial_state()
        state5 = game5.new_initial_state()

        ex.horizontal_closed_chain(state1)
        ex.vertical_closed_chain(state2)
        ex.horizontal_half_open_chain1(state3)
        ex.vertical_half_open_chain(state4)
        ex.horizontal_half_open_chain2(state5)

        value = "value"
        table.set(state1, value)
        table.set(state3, value)

        self.assertEqual(table.get(state1), value)
        self.assertEqual(table.get(state2), value)
        self.assertEqual(table.get(state3), value)
        self.assertEqual(table.get(state4), value)
        self.assertNotEqual(table.get(state5), value)

if __name__ == '__main__':
    unittest.main()
