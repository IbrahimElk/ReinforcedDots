import os
import sys
import unittest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)

from chains.util import CellOrientation, Directions
from chains.chains_strategy import StrategyAdvisor


class TestAlphaBeta(unittest.TestCase):
    pass


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