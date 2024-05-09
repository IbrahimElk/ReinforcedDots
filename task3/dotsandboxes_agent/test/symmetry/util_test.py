import os
import sys
import unittest
import random as r
import pyspiel

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, parent_dir)

import chains.pyspiel_examples as exp
import chains.examples as ex

import chains.chains_strategy as cs
from symmetry.util import dbn_to_vectors, vectors_to_dbn

class TestDBNToVectors(unittest.TestCase):
    def test_dbn_to_vectors_single_singleton(self):
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(2, 10)
        y = r.randint(2, 10)

        num_rows = x
        num_cols = y

        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        SA = cs.StrategyAdvisor(num_rows, num_cols)

        initial_state = game.new_initial_state()

        exp.single_singleton(initial_state)
        ex.single_singleton(SA)

        dbn = initial_state.dbn_string()

        # print(initial_state)

        h, v = dbn_to_vectors(num_rows, num_cols, dbn)

        self.assertListEqual(h, SA.h_)
        self.assertListEqual(v, SA.v_)

    def test_dbn_to_vectors_single_doubleton(self):
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(2, 10)
        y = r.randint(3, 10)

        num_rows = x
        num_cols = y

        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        SA = cs.StrategyAdvisor(num_rows, num_cols)

        initial_state = game.new_initial_state()

        exp.single_doubleton(initial_state)
        ex.single_doubleton(SA)

        dbn = initial_state.dbn_string()

        # print(initial_state)

        h, v = dbn_to_vectors(num_rows, num_cols, dbn)

        self.assertListEqual(h, SA.h_)
        self.assertListEqual(v, SA.v_)

    def test_dbn_to_vectors_vertical_half_open_chain(self):
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(3, 10)
        y = r.randint(2, 10)

        num_rows = x
        num_cols = y
        
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        SA = cs.StrategyAdvisor(num_rows, num_cols)

        initial_state = game.new_initial_state()

        exp.vertical_half_open_chain(initial_state)
        ex.vertical_half_open_chain(SA)

        dbn = initial_state.dbn_string()

        # print(initial_state)

        h, v = dbn_to_vectors(num_rows, num_cols, dbn)

        self.assertListEqual(h, SA.h_)
        self.assertListEqual(v, SA.v_)


    def test_dbn_to_vectors_horizontal_closed_chain(self):
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(2, 10)
        y = r.randint(5, 10)

        num_rows = x
        num_cols = y
        
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        SA = cs.StrategyAdvisor(num_rows, num_cols)

        initial_state = game.new_initial_state()

        exp.horizontal_closed_chain(initial_state)
        ex.horizontal_closed_chain(SA)

        dbn = initial_state.dbn_string()

        # print(initial_state)

        h, v = dbn_to_vectors(num_rows, num_cols, dbn)

        self.assertListEqual(h, SA.h_)
        self.assertListEqual(v, SA.v_)

class TestVectorsTODBN(unittest.TestCase):
    def test_vectors_to_dbn_single_singleton(self):
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(2, 10)
        y = r.randint(2, 10)

        num_rows = x
        num_cols = y
        
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        SA = cs.StrategyAdvisor(num_rows, num_cols)
        initial_state = game.new_initial_state()

        exp.single_singleton(initial_state)
        ex.single_singleton(SA)

        gdbn = initial_state.dbn_string()
        dbn = vectors_to_dbn(num_rows, num_cols, SA.h_, SA.v_)

        self.assertEqual(dbn, gdbn)

    def test_vectors_to_dbn_single_doubleton(self):
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(2, 10)
        y = r.randint(3, 10)

        num_rows = x
        num_cols = y
        
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        SA = cs.StrategyAdvisor(num_rows, num_cols)
        initial_state = game.new_initial_state()

        exp.single_doubleton(initial_state)
        ex.single_doubleton(SA)

        gdbn = initial_state.dbn_string()
        dbn = vectors_to_dbn(num_rows, num_cols, SA.h_, SA.v_)

        self.assertEqual(dbn, gdbn)

    def test_vectors_to_dbn_vertical_half_open_chain(self):
        # seed = None
        # if seed:
        #     r.seed(seed)

        x = r.randint(3, 10)
        y = r.randint(2, 10)

        num_rows = x
        num_cols = y
        
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        SA = cs.StrategyAdvisor(num_rows, num_cols)
        initial_state = game.new_initial_state()

        exp.vertical_half_open_chain(initial_state)
        ex.vertical_half_open_chain(SA)

        gdbn = initial_state.dbn_string()
        dbn = vectors_to_dbn(num_rows, num_cols, SA.h_, SA.v_)

        self.assertEqual(dbn, gdbn)

    def test_vectors_to_dbn_horizontal_closed_chain(self):
        # seed = None
        # if seed:
        #     r.seed(seed)
        
        x = r.randint(2, 10)
        y = r.randint(5, 10)

        num_rows = x
        num_cols = y
        
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        SA = cs.StrategyAdvisor(num_rows, num_cols)
        initial_state = game.new_initial_state()

        exp.horizontal_closed_chain(initial_state)
        ex.horizontal_closed_chain(SA)

        gdbn = initial_state.dbn_string()
        dbn = vectors_to_dbn(num_rows, num_cols, SA.h_, SA.v_)

        self.assertEqual(dbn, gdbn)

if __name__ == '__main__':
    unittest.main()