import os
import sys
import unittest
import pyspiel

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, parent_dir)

import chains.pyspiel_examples as exp
import symmetry.symmetries as s 

class TestSymmetries(unittest.TestCase):
    #      *----*
    #  	        |
    #      *----*
    def test_symmetries_single_singleton(self):
        num_rows = 2
        num_cols = 2

        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)

        initial_state = game.new_initial_state()
        exp.single_singleton(initial_state)

        symmetric_dbn_states = s._find_all_symmetries(initial_state, num_rows, num_cols)

        self.assertSetEqual(set(symmetric_dbn_states), set(["001010000010", 
                                                            "010100010000", 
                                                            "000101000010", 
                                                            "001000000110", 
                                                            "000100011000"]))

    #      *----*    *
    #  	        |
    #      *----*    *
    def test_symmetries_single_singleton(self):
        num_rows = 1
        num_cols = 2

        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)

        initial_state = game.new_initial_state()
        exp.single_singleton(initial_state)

        dbn4 = s.check_horizontal(initial_state, num_rows, num_cols)
        self.assertEqual(dbn4, "1010010")
        
        dbn5 = s.check_vertical(initial_state, num_rows, num_cols)
        self.assertEqual(dbn5, "0101010")        
        
        dbn6 = s.check_hv(initial_state, num_rows, num_cols)
        self.assertEqual(dbn6, "0101010")
        
        dbn7 = s.check_vh(initial_state, num_rows, num_cols)
        self.assertEqual(dbn7, "0101010")


    #      *----*----*
    #  	   |         |  
    #      *----*----*
    def test_symmetries_single_doubleton(self):
        num_rows = 2
        num_cols = 2

        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)
        initial_state = game.new_initial_state()

        exp.single_doubleton(initial_state)

        # includes itself:
        symmetric_dbn_states = s._find_all_symmetries(initial_state, num_rows, num_cols)

        self.assertSetEqual(set(symmetric_dbn_states), set(["111100101000",
                                                            "100010110110",
                                                            "010001011011",
                                                            "001111000101"]))


    #      *----*
    #  	   |    |
    #      * 	*
    #  	   |    |
    #  	   *    *
    def test_symmetries_vertical_half_open_chain(self):
        num_rows = 2
        num_cols = 2
        
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)

        initial_state = game.new_initial_state()
        exp.vertical_half_open_chain(initial_state)

        dbn1 = s.check_diag1(initial_state, num_rows, num_cols)
        self.assertEqual(dbn1, "111100001000")
        
        dbn2 = s.check_diag2(initial_state, num_rows, num_cols)
        self.assertEqual(dbn2, "001111000100")        
        
        dbn3 = s.check_h_diag1(initial_state, num_rows, num_cols)
        self.assertEqual(dbn3, "111100100000")

        dbn4 = s.check_horizontal(initial_state, num_rows, num_cols)
        self.assertEqual(dbn4, "000010110110")
        
        dbn5 = s.check_vertical(initial_state, num_rows, num_cols)
        self.assertEqual(dbn5, "010000011011")        
        
        dbn6 = s.check_hv(initial_state, num_rows, num_cols)
        self.assertEqual(dbn6, "000001011011")
        
        dbn7 = s.check_vh(initial_state, num_rows, num_cols)
        self.assertEqual(dbn7, "000001011011")  


    #      *----*---*---*---*
    #  	   |		        |
    #  	   *----*---*---*---*
    def test_symmetries_horizontal_closed_chain(self):
        num_rows = 4
        num_cols = 4
        
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

        # print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)

        initial_state = game.new_initial_state()
        exp.horizontal_closed_chain(initial_state)

        dbn1 = s.check_diag1(initial_state, num_rows, num_cols)
        self.assertEqual(dbn1, "0001 0000 0000 0000 0001 00011 00011 00011 00011".replace(" ", ""))
        
        dbn2 = s.check_diag2(initial_state, num_rows, num_cols)
        self.assertEqual(dbn2, "1000 0000 0000 0000 1000 11000 11000 11000 11000".replace(" ", ""))        
        
        dbn3 = s.check_h_diag1(initial_state, num_rows, num_cols)
        self.assertEqual(dbn3, "1000 0000 0000 0000 1000 11000 11000 11000 11000".replace(" ", ""))

        dbn4 = s.check_horizontal(initial_state, num_rows, num_cols)
        self.assertEqual(dbn4, "0000 0000 0000 1111 1111 00000 00000 00000 10001".replace(" ", ""))
        
        dbn5 = s.check_vertical(initial_state, num_rows, num_cols)
        self.assertEqual(dbn5, "1111 1111 0000 0000 0000 10001 00000 00000 00000".replace(" ", ""))        
        
        dbn6 = s.check_hv(initial_state, num_rows, num_cols)
        self.assertEqual(dbn6, "0000 0000 0000 1111 1111 00000 00000 00000 10001".replace(" ", ""))
        
        dbn7 = s.check_vh(initial_state, num_rows, num_cols)
        self.assertEqual(dbn7, "0000 0000 0000 1111 1111 00000 00000 00000 10001".replace(" ", ""))  

if __name__ == '__main__':
    unittest.main()