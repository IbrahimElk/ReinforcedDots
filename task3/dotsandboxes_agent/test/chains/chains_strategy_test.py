import os
import sys
import unittest
import examples as ex

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)

from chains.util import CellOrientation, Directions
from chains.chains_strategy import StrategyAdvisor

def print_matrix(matrix):
    for row in matrix:
        for element in row:
            print(element, end=" ")  
        print()

class TestStrategyAdvisor(unittest.TestCase):
    # def test_double_half_haerted_vertical(self):
    #     SA = StrategyAdvisor(6,6)
        
    #     # initialise closed vertical chain of length 4. 
    #     ex.vertical_closed_chain(SA)

    #     # find all initialised chains
    #     SA.find_all_chains()

    #     chain_data = SA.chains["closed"][0]
    #     action = SA.get_double_half_haerted(chain_data["chain"], chain_data["directions"])
    #     ground_truth_action = SA.action_id(CellOrientation.HORIZONTAL, 2, 0)

    #     # print_matrix(SA.cells)
    #     # print_matrix(SA.h_)
    #     # print_matrix(SA.v_)

    #     self.assertTrue(ground_truth_action == action)

    # def test_double_half_haerted_horizontal(self):
    #     SA = StrategyAdvisor(10,10)

    #     # initialise closed horizontal chain of length 4. 
    #     ex.horizontal_closed_chain(SA)

    #     # find all initialised chains
    #     SA.find_all_chains()

    #     chain_data = SA.chains["closed"][0]
    #     action = SA.get_double_half_haerted(chain_data["chain"], chain_data["directions"])
    #     ground_truth_action = SA.action_id(CellOrientation.VERTICAL, 0, 2)
        
    #     self.assertTrue(ground_truth_action == action)

    # def test_single_half_haerted_horizontal_1(self):
    #     SA = StrategyAdvisor(10,10)

    #     # initialise half open horizontal chain of length 2.
    #     ex.horizontal_half_open_chain1(SA)

    #     # find all initialised chains
    #     SA.find_all_chains()

    #     chain_data = SA.chains["half_open"][0]
    #     action = SA.get_single_half_haerted(chain_data["chain"], chain_data["directions"])
    #     ground_truth_action = SA.action_id(CellOrientation.VERTICAL, 0, 2)

    #     self.assertTrue(ground_truth_action == action)

    # def test_single_half_haerted_horizontal_2(self):
    #     SA = StrategyAdvisor(10,10)

    #     # initialise half open horizontal chain of length 2.
    #     ex.horizontal_half_open_chain2(SA)

    #     # find all initialised chains
    #     SA.find_all_chains()

    #     chain_data = SA.chains["half_open"][0]
    #     action = SA.get_single_half_haerted(chain_data["chain"], chain_data["directions"])
    #     ground_truth_action = SA.action_id(CellOrientation.HORIZONTAL, 1, 1)

    #     self.assertTrue(ground_truth_action == action)

    
    # def test_single_half_haerted_vertical(self):
    #     SA = StrategyAdvisor(10,10)

    #     # initialise half open vertical chain of length 2.
    #     ex.vertical_half_open_chain(SA)

    #     # find all initialised chains
    #     SA.find_all_chains()

    #     chain_data = SA.chains["half_open"][0]
    #     action = SA.get_single_half_haerted(chain_data["chain"], chain_data["directions"])
    #     ground_truth_action = SA.action_id(CellOrientation.HORIZONTAL, 2, 0)

    #     self.assertTrue(ground_truth_action == action)

    # def test_find_all_chains(self):
    #     SA = StrategyAdvisor(10,10)

    #     # initialise 2 chains from paper.
    #     ex.example_paper(SA)

    #     # find all initialised chains
    #     SA.find_all_chains()

    #     chain_data = SA.chains
    #     ground_truth_chain_data = {
    #         "half_open":
    #         [
    #             {
    #                 "directions": [Directions.DOWN, Directions.DOWN, Directions.RIGHT, Directions.RIGHT, Directions.RIGHT, Directions.RIGHT], 
    #                 "chain": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3)], 
    #                 "count": 6
    #             }
    #         ], 
    #         "closed": 
    #         [
    #             {
    #                 "directions": [Directions.RIGHT, Directions.RIGHT, Directions.RIGHT, Directions.DOWN, Directions.DOWN], 
    #                 "chain": [(0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (2, 5)], 
    #                 "count": 6
    #             }
    #         ]
    #     }

    #     chain = chain_data["half_open"][0]["chain"]
    #     gchain = ground_truth_chain_data["half_open"][0]["chain"]

    #     for i in range(max(len(chain), len(gchain))): 
    #         self.assertTupleEqual(chain[i], gchain[i])

    #     directions = chain_data["half_open"][0]["directions"]
    #     gdirections = ground_truth_chain_data["half_open"][0]["directions"]

    #     for i in range(max(len(directions), len(gdirections))): 
    #         self.assertEqual(directions[i].value, gdirections[i].value)

    #     self.assertEqual(chain_data["half_open"][0]["count"], ground_truth_chain_data["half_open"][0]["count"])

    # def test_get_tabular_form(self):
    #     SA = StrategyAdvisor(10,10)

    #     action1 = SA.action_id(CellOrientation.HORIZONTAL, 2, 3)
    #     action2 = SA.action_id(CellOrientation.VERTICAL, 1, 2)

    #     orien1, row1, col1 = SA.get_tabular_form(action1)
    #     orien2, row2, col2 = SA.get_tabular_form(action2)

    #     self.assertEqual(orien1.value, CellOrientation.HORIZONTAL.value)
    #     self.assertEqual(row1, 2)
    #     self.assertEqual(col1, 3)

    #     self.assertEqual(orien2.value, CellOrientation.VERTICAL.value)
    #     self.assertEqual(row2, 1)
    #     self.assertEqual(col2, 2)

    # def test_update_with_action(self):
    #     SA = StrategyAdvisor(10,10)

    #     # Test update using action ID
    #     action1 = SA.action_id(CellOrientation.HORIZONTAL, 2, 3)
    #     SA.update_action(action1)
    #     self.assertEqual(SA.h_[2][3], 1)
    #     self.assertEqual(SA.cells[2][3], 1)

    #     action2 = SA.action_id(CellOrientation.VERTICAL, 1, 2)
    #     SA.update_action(action2)
    #     self.assertEqual(SA.v_[1][2], 1)
    #     self.assertEqual(SA.cells[1][2], 1)

    # def test_update_with_orientation_and_coords(self):
    #     SA = StrategyAdvisor(10,10)

    #     # Test update using orientation and coordinates
    #     SA.update_edge(CellOrientation.HORIZONTAL, 1, 2)
    #     self.assertEqual(SA.h_[1][2], 1)
    #     self.assertEqual(SA.cells[1][2], 1)

    #     SA.update_edge(CellOrientation.VERTICAL, 2, 3)
    #     self.assertEqual(SA.v_[2][3], 1)
    #     self.assertEqual(SA.cells[2][3], 1)

    # # -------------------------------------------------------------------
    # # -------------------------------------------------------------------
    # #                           SAFE3
    # # -------------------------------------------------------------------
    # # -------------------------------------------------------------------

    # def test_safe3_with_single_singleton(self):
    #     SA = StrategyAdvisor(10,10)

    #     ex.single_singleton(SA)
    #     actions = SA.safe3()
    #     self.assertEqual(len(actions), 1)
    #     expected_action = SA.action_id(CellOrientation.VERTICAL, 0, 0)
    #     self.assertEqual(actions[0], expected_action)

    #     SA.update_action(expected_action)
    #     actions = SA.safe3()
    #     self.assertEqual(actions, None)

    # def test_safe3_with_single_doubleton(self):
    #     SA = StrategyAdvisor(10,10)
        
    #     ex.single_doubleton(SA)
    #     actions = SA.safe3()
    #     self.assertEqual(len(actions), 1)
    #     expected_action = SA.action_id(CellOrientation.VERTICAL, 0, 1)
    #     self.assertEqual(actions[0], expected_action)
        
    #     SA.update_action(expected_action)
    #     actions = SA.safe3()
    #     self.assertEqual(actions, None)

    # def test_safe3_with_example_paper(self):
    #     SA = StrategyAdvisor(10,10)

    #     ex.example_paper(SA)
    #     actions = SA.safe3()
    #     self.assertIsNone(actions)

    # # -------------------------------------------------------------------
    # # -------------------------------------------------------------------
    # #                           SIDE3
    # # -------------------------------------------------------------------
    # # -------------------------------------------------------------------


    # def test_side3_with_example_paper(self):
    #     SA = StrategyAdvisor(10, 10)

    #     ex.example_paper(SA)
    #     cell3s = SA.side3()
    #     self.assertEqual([(0,0), (0,2), (2,5)], cell3s)


    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    #                           UNSAFE3 
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------

    #      *----*---*
    #  	   |		
    #  	   *----*---*
    def test_horizontal_half_open_chain1_unsafe3(self):
        SA = StrategyAdvisor(10, 10)

        ex.horizontal_half_open_chain1(SA)

        action1 = SA.action_id(CellOrientation.VERTICAL, 0, 1)
        action2 = SA.action_id(CellOrientation.VERTICAL, 0, 2)

        expected_actions = [[action2, action1], [action1]]
        actions = SA.unsafe3()
        counter = 0
        while actions :
            self.assertEqual(actions, expected_actions[counter])

            SA.update_action(actions[0])
            actions = SA.unsafe3()
            
            counter += 1

    def test_horizontal_half_open_chain2_unsafe3(self):
        ex.horizontal_half_open_chain2(self.SA)

    # def test_vertical_half_open_chain_unsafe3(self):
    #     ex.vertical_half_open_chain(self.SA)

    # def test_horizontal_closed_chain_unsafe3(self):
    #     ex.horizontal_closed_chain(self.SA)

    # def test_vertical_closed_chain_unsafe3(self):
    #     ex.vertical_closed_chain(self.SA)

    # def test_example_paper_unsafe3(self):
    #     ex.example_paper(self.SA)

if __name__ == '__main__':
    unittest.main()