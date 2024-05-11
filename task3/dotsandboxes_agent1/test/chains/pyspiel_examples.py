import pyspiel
import os 
import sys
import numpy as np

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)

from chains.chains_strategy import StrategyAdvisor
from chains.util import CellOrientation


#      *----*
#  	        |
#      *----*
def single_singleton(IS):
    """
    player 2 is aan de beurt
    """
    params = IS.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    
    SA = StrategyAdvisor(num_rows, num_cols)

    action1 = SA.action_id(CellOrientation.HORIZONTAL,  0, 0)
    action2 = SA.action_id(CellOrientation.HORIZONTAL,  1, 0)
    action3 = SA.action_id(CellOrientation.VERTICAL,    0, 1)

    IS.apply_action(action1)
    IS.apply_action(action2)
    IS.apply_action(action3)

# ┌───┬───┐
# │ 2 │ 2 │
# ├───┼───┤
# │       │
# └───┴╴ ╶┘
def debug_example1(IS):
    """
    player 2 is aan de beurt
    """
    params = IS.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    
    SA = StrategyAdvisor(num_rows ,num_cols)

    # 1
    action1 = SA.action_id(CellOrientation.HORIZONTAL,  0, 0)
    # print(action1)
    # 2
    action2 = SA.action_id(CellOrientation.HORIZONTAL,  1, 0)
    # print(action2)
    # 1
    action3 = SA.action_id(CellOrientation.VERTICAL,    0, 1)
    # print(action3)
    # 2
    action4 = SA.action_id(CellOrientation.VERTICAL,    0, 0)
    # print(action4)
    # 2
    action5 = SA.action_id(CellOrientation.HORIZONTAL, 1, 1)
    # print(action5)
    # 1
    action6 = SA.action_id(CellOrientation.HORIZONTAL, 2, 0)
    # print(action6)
    # 2
    action7 = SA.action_id(CellOrientation.VERTICAL, 1, 2)
    # print(action7)
    # 1
    action8 = SA.action_id(CellOrientation.HORIZONTAL, 0, 1)
    # print(action8)
    # 2
    action9 = SA.action_id(CellOrientation.VERTICAL, 0, 2)
    # print(action9)
    # 2
    action10 = SA.action_id(CellOrientation.VERTICAL, 1, 0)
    # print(action10)

    # action11 = SA.action_id(CellOrientation.HORIZONTAL, 2, 1)
    # print(action11)

    # action12 = SA.action_id(CellOrientation.VERTICAL, 1, 1)
    # print(action12)

    IS.apply_action(action1)
    IS.apply_action(action2)
    IS.apply_action(action3)

    IS.apply_action(action4)
    IS.apply_action(action5)
    IS.apply_action(action6)

    IS.apply_action(action7)
    IS.apply_action(action8)
    IS.apply_action(action9)
    IS.apply_action(action10)
    
#      *----*----*
#  	   |         |  
#      *----*----*
def single_doubleton(IS):
    """
    player 1 is aan de beurt
    """
    params = IS.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    
    SA = StrategyAdvisor(num_rows,num_cols)

    action1 = SA.action_id(CellOrientation.HORIZONTAL,  0, 0)
    action2 = SA.action_id(CellOrientation.HORIZONTAL,  0, 1)
    action3 = SA.action_id(CellOrientation.HORIZONTAL,  1, 0)
    action4 = SA.action_id(CellOrientation.HORIZONTAL,  1, 1)

    action5 = SA.action_id(CellOrientation.VERTICAL,    0, 0)
    action6 = SA.action_id(CellOrientation.VERTICAL,    0, 2)

    IS.apply_action(action1)
    IS.apply_action(action2)
    IS.apply_action(action3)
    IS.apply_action(action4)
    IS.apply_action(action5)
    IS.apply_action(action6)

#  
#      *----*
#  	   |    |
#      * 	*
#  	   |    |
#  	   *    *
def vertical_half_open_chain(IS):
    """
    player 2 is aan de beurt
    """
    params = IS.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    
    SA = StrategyAdvisor(num_rows,num_cols)

    action1 = SA.action_id(CellOrientation.VERTICAL,  0, 0)
    action2 = SA.action_id(CellOrientation.VERTICAL,  0, 1)
    action3 = SA.action_id(CellOrientation.VERTICAL,  1, 0)
    action4 = SA.action_id(CellOrientation.VERTICAL,  1, 1)

    action5 = SA.action_id(CellOrientation.HORIZONTAL,    0, 0)

    IS.apply_action(action1)
    IS.apply_action(action2)
    IS.apply_action(action3)
    IS.apply_action(action4)
    IS.apply_action(action5)


#      *----*---*
#  	   |		|
#  	   *----*   *
def horizontal_half_open_chain2(IS):
    """
    player 2 is aan de beurt
    """
    params = IS.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    
    SA = StrategyAdvisor(num_rows,num_cols)

    action1 = SA.action_id(CellOrientation.VERTICAL,  0, 0)
    action2 = SA.action_id(CellOrientation.VERTICAL,  0, 2)

    action3 = SA.action_id(CellOrientation.HORIZONTAL,    0, 0)
    action4 = SA.action_id(CellOrientation.HORIZONTAL,    0, 1)
    action5 = SA.action_id(CellOrientation.HORIZONTAL,    1, 0)

    IS.apply_action(action1)
    IS.apply_action(action2)
    IS.apply_action(action3)
    IS.apply_action(action4)
    IS.apply_action(action5)

#      *----*---*
#  	   |		
#  	   *----*---*
def horizontal_half_open_chain1(IS):
    """
    player 2 is aan de beurt
    """
    params = IS.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    
    SA = StrategyAdvisor(num_rows,num_cols)

    action1 = SA.action_id(CellOrientation.VERTICAL,  0, 0)
    action2 = SA.action_id(CellOrientation.HORIZONTAL,    0, 0)
    action3 = SA.action_id(CellOrientation.HORIZONTAL,    0, 1)
    action4 = SA.action_id(CellOrientation.HORIZONTAL,    1, 0)
    action5 = SA.action_id(CellOrientation.HORIZONTAL,    1, 1)

    IS.apply_action(action1)
    IS.apply_action(action2)
    IS.apply_action(action3)
    IS.apply_action(action4)
    IS.apply_action(action5)

#      *----*---*---*---*
#  	   |		        |
#  	   *----*---*---*---*
def horizontal_closed_chain(IS):
    """
    player 1 is aan de beurt
    """
    params = IS.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    
    SA = StrategyAdvisor(num_rows,num_cols)

    action1     = SA.action_id(CellOrientation.VERTICAL,  0, 0)
    action2     = SA.action_id(CellOrientation.VERTICAL,  0, 4)

    action3     = SA.action_id(CellOrientation.HORIZONTAL,    0, 0)
    action4     = SA.action_id(CellOrientation.HORIZONTAL,    0, 1)
    action5     = SA.action_id(CellOrientation.HORIZONTAL,    0, 2)
    action6     = SA.action_id(CellOrientation.HORIZONTAL,    0, 3)

    action8     = SA.action_id(CellOrientation.HORIZONTAL,    1, 0)
    action9     = SA.action_id(CellOrientation.HORIZONTAL,    1, 1)
    action10    = SA.action_id(CellOrientation.HORIZONTAL,    1, 2)
    action11    = SA.action_id(CellOrientation.HORIZONTAL,    1, 3)

    IS.apply_action(action1)
    IS.apply_action(action2)
    IS.apply_action(action3)
    IS.apply_action(action4)
    IS.apply_action(action5)
    IS.apply_action(action6)

    IS.apply_action(action8)
    IS.apply_action(action9)
    IS.apply_action(action10)
    IS.apply_action(action11)

# hetvolgende maar transposed:
#      *----*---*---*---*
#  	   |		        |
#  	   *----*---*---*---*
def vertical_closed_chain(IS):
    """
    player 1 is aan de beurt
    """
    params = IS.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    
    SA = StrategyAdvisor(num_rows,num_cols)

    action1     = SA.action_id(CellOrientation.HORIZONTAL,  0, 0)
    action2     = SA.action_id(CellOrientation.HORIZONTAL,  4, 0)

    action3     = SA.action_id(CellOrientation.VERTICAL,    0, 0)
    action4     = SA.action_id(CellOrientation.VERTICAL,    1, 0)
    action5     = SA.action_id(CellOrientation.VERTICAL,    2, 0)
    action6     = SA.action_id(CellOrientation.VERTICAL,    3, 0)

    action8     = SA.action_id(CellOrientation.VERTICAL,    0, 1)
    action9     = SA.action_id(CellOrientation.VERTICAL,    1, 1)
    action10    = SA.action_id(CellOrientation.VERTICAL,    2, 1)
    action11    = SA.action_id(CellOrientation.VERTICAL,    3, 1)

    IS.apply_action(action1)
    IS.apply_action(action2)
    IS.apply_action(action3)
    IS.apply_action(action4)
    IS.apply_action(action5)
    IS.apply_action(action6)

    IS.apply_action(action8)
    IS.apply_action(action9)
    IS.apply_action(action10)
    IS.apply_action(action11)

# Solving Dots-And-Boxes
# Joseph K. Barker and Richard E Korf
# Figure 2: Examples of chains
def example_paper(IS):
    """
    player 2 is aan de beurt
    """
    params = IS.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    
    SA = StrategyAdvisor(num_rows,num_cols)
    action1    = SA.action_id(CellOrientation.HORIZONTAL,    0, 2)
    action2    = SA.action_id(CellOrientation.HORIZONTAL,    0, 3)
    action3    = SA.action_id(CellOrientation.HORIZONTAL,    0, 4)
    action4    = SA.action_id(CellOrientation.HORIZONTAL,    0, 5)

    action5    = SA.action_id(CellOrientation.HORIZONTAL,    1, 2)
    action6    = SA.action_id(CellOrientation.HORIZONTAL,    1, 3)
    action7    = SA.action_id(CellOrientation.HORIZONTAL,    1, 4)

    action8    = SA.action_id(CellOrientation.HORIZONTAL,    3, 5)

    action9     = SA.action_id(CellOrientation.VERTICAL,    0, 6)
    action10    = SA.action_id(CellOrientation.VERTICAL,    1, 6)
    action11    = SA.action_id(CellOrientation.VERTICAL,    2, 6)

    action12    = SA.action_id(CellOrientation.VERTICAL,    0, 2)
    action13    = SA.action_id(CellOrientation.VERTICAL,    1, 5)
    action14    = SA.action_id(CellOrientation.VERTICAL,    2, 5)

    action15    = SA.action_id(CellOrientation.VERTICAL,  0, 0)
    action16    = SA.action_id(CellOrientation.VERTICAL,  1, 0)
    action17    = SA.action_id(CellOrientation.VERTICAL,  2, 0)

    action18    = SA.action_id(CellOrientation.VERTICAL,  0, 1)
    action19    = SA.action_id(CellOrientation.VERTICAL,  1, 1)

    action20    = SA.action_id(CellOrientation.HORIZONTAL,  3, 0)
    action21    = SA.action_id(CellOrientation.HORIZONTAL,  3, 1)
    action22    = SA.action_id(CellOrientation.HORIZONTAL,  3, 2)
    action23    = SA.action_id(CellOrientation.HORIZONTAL,  3, 3)

    action24    = SA.action_id(CellOrientation.HORIZONTAL,  2, 1)
    action25    = SA.action_id(CellOrientation.HORIZONTAL,  2, 2)
    action26    = SA.action_id(CellOrientation.HORIZONTAL,  2, 3)

    action27    = SA.action_id(CellOrientation.HORIZONTAL,    0, 0)
    

    IS.apply_action(action1)
    IS.apply_action(action2)
    IS.apply_action(action3)
    IS.apply_action(action4)
    IS.apply_action(action5)
    IS.apply_action(action6)
    IS.apply_action(action7)
    IS.apply_action(action8)
    IS.apply_action(action9)
    IS.apply_action(action10)
    IS.apply_action(action11)
    IS.apply_action(action12)
    IS.apply_action(action13)
    IS.apply_action(action14)
    IS.apply_action(action15)
    IS.apply_action(action16)
    IS.apply_action(action17)
    IS.apply_action(action18)
    IS.apply_action(action19)
    IS.apply_action(action20)
    IS.apply_action(action21)
    IS.apply_action(action22)
    IS.apply_action(action23)
    IS.apply_action(action24)
    IS.apply_action(action25)
    IS.apply_action(action26)
    IS.apply_action(action27)