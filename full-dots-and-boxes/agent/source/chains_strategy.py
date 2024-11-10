"""
This module implements a strategy advisor for the Dots and Boxes game. 
The `StrategyAdvisor` class provides methods to analyze the 
board state, identify optimal moves, and apply various game
strategies to maximize the player's score.

source : 
- https://www.math.ucla.edu/~tom/Games/dots&boxes.html
- Joseph Kelly Barker and Richard E. Korf. Solving dots-and-boxes.

Author: Ibrahim El Kaddouri
April - 2024
"""

import os
import sys
import math
import random as r
import numpy as np
import time as t

parent_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

from util import CellOrientation, Directions, vectors_to_dbn
from evaluators import game_state_tensor, pvector_for_tensor, box_state_for_pvector
from transposition_table import Transposition_Table_Chains

# type Alias
Action = int


class StrategyAdvisor : 
    """
    Analyzes the state of a Dots and Boxes game board and provides recommended actions.
    
    Attributes:
        num_rows (int): Number of rows in the game board.
        num_cols (int): Number of columns in the game board.
        h_ (list): Horizontal edges of the board.
        v_ (list): Vertical edges of the board.
        p_ (list): Player scores.
        cells (list): Track cells' edge completion status.
        chains (dict): Chains data including open and closed chains on the board.
    """

    def __init__(self, rows:int, cols:int):
        self.num_rows = rows
        self.num_cols = cols

        self.h_ = [[0] * cols for _ in range(rows + 1)]
        self.v_ = [[0] * (cols + 1) for _ in range(rows)]
        self.p_ = [0, 0]
        self.cells = [[0] * cols for _ in range(rows)]
        self.chains = {"half_open": [], "closed": [], "count": 0 }

    def clone(self):
        """
        Creates a deep copy of the current `StrategyAdvisor` instance.

        Returns:
            StrategyAdvisor: A clone of the current StrategyAdvisor instance.
        """
        cloned_advisor = StrategyAdvisor(self.num_rows, self.num_cols)
        cloned_advisor.h_ = [row[:] for row in self.h_]
        cloned_advisor.v_ = [row[:] for row in self.v_]
        cloned_advisor.p_ = [self.p_[0], self.p_[1]]
        cloned_advisor.cells = [row[:] for row in self.cells]
        return cloned_advisor

    def get_tabular_form(self, action:Action):
        """
        Converts an action ID to a grid position and orientation.

        Args:
            action (int): The action ID.

        Returns:
            tuple: Orientation, row, and column of the edge.
        """
        maxh = (self.num_rows + 1) * self.num_cols
        if (action < maxh) : 
            # Horizontal
            orien = CellOrientation.HORIZONTAL
            row = math.floor(action / self.num_cols)
            col = action % self.num_cols
        else : 
            # Vertical
            action -= maxh
            orien = CellOrientation.VERTICAL
            row = math.floor(action / (self.num_cols + 1))
            col = action % (self.num_cols + 1)

        return orien, row, col
        
    def update_action(self, action:Action, current_player:int):
       """
       Updates the board based on an action taken by a player.
       Args:
           action (int): The action taken.
           current_player (int): The player taking the action.
       """
       orien, i, j = self.get_tabular_form(action)
       if orien.value == CellOrientation.HORIZONTAL.value : 
           self.set_h_edge(i,j, current_player)
       else : 
           self.set_v_edge(i,j, current_player)         

    def update_edge(self, orien:CellOrientation, i:int, j:int, current_player:int):
        """
        Updates the board with a specific edge.

        Args:
            orien (CellOrientation): Orientation of the edge.
            i (int): Row index.
            j (int): Column index.
            current_player (int): Player taking the action.
        """
        if orien.value == CellOrientation.HORIZONTAL.value : 
            self.set_h_edge(i,j, current_player)
        else : 
            self.set_v_edge(i,j, current_player)

    def set_h_edge(self, x:int, y:int, current_player:int):
        """Sets a horizontal edge on the board and updates cell counts.

        Args:
            x (int): Row index.
            y (int): Column index.
            current_player (int): Player taking the action.
        """
        self.h_[x][y] = 1
        if x > 0:
            self.cells[x - 1][y] += 1
            if self.cells[x - 1][y] == 4: 
                self.p_[current_player] += 1

        if x < self.num_rows:
            self.cells[x][y] += 1
            if self.cells[x][y] == 4: 
                self.p_[current_player] += 1

    def set_v_edge(self, x:int, y:int, current_player:int):
        """
        Sets a vertical edge on the board and updates cell counts.

        Args:
            x (int): Row index.
            y (int): Column index.
            current_player (int): Player taking the action.
        """
        self.v_[x][y] = 1
        if y > 0:
            self.cells[x][y - 1] += 1
            if self.cells[x][y - 1] == 4: 
                self.p_[current_player] += 1

        if y < self.num_cols:
            self.cells[x][y] += 1
            if self.cells[x][y] == 4: 
                self.p_[current_player] += 1

    def action_id(self, orientation_:CellOrientation, row_:int, col_:int) -> Action :
        """Translates row, column, and orientation into an action ID.
        Args:
            orientation_ (CellOrientation): Orientation of the edge.
            row_ (int): Row index.
            col_ (int): Column index.

        Returns:
            Action: An integer representing the action.
        
        Raises:
            ValueError: If `orientation_` is not a valid `CellOrientation`.
        """
        action = 0
        maxh  = (self.num_rows + 1) * self.num_cols
        if (orientation_.value == CellOrientation.HORIZONTAL.value):
            action = row_ * self.num_cols + col_
        elif (orientation_.value == CellOrientation.VERTICAL.value):
            action = maxh + row_ * (self.num_cols + 1) + col_
        else : 
            raise ValueError("The orientation_ parameter must be of type CellOrientation")

        return action

    def safe3(self) -> list[Action] | None :
        """Returns actions that capture singletons or doubletons.

        Returns:
            list: A list containing an action ID to capture a box or None if unavailable.
        """
        for row in range(0,self.num_rows):
            for col in range(0,self.num_cols):
                if self.cells[row][col] == 3:
                    if self.v_[row][col] < 1:
                        if col == 0 or self.cells[row][col-1] != 2 :
                            action = self.action_id(CellOrientation.VERTICAL, row, col)
                            return [action]
                        
                    elif self.h_[row][col] < 1:
                        if row == 0 or self.cells[row-1][col] != 2:
                            action = self.action_id(CellOrientation.HORIZONTAL, row, col)
                            return [action]

                    elif self.v_[row][col+1] < 1:
                        if col == self.num_cols-1 or self.cells[row][col+1] != 2:
                            action = self.action_id(CellOrientation.VERTICAL, row, col+1)
                            return [action]
                    else :
                        if row == self.num_rows-1 or self.cells[row+1][col] != 2:
                            action = self.action_id(CellOrientation.HORIZONTAL, row+1, col)
                            return [action]
        return None
    
    def find_all_chains(self):
        """Identifies and categorizes all chains on the board."""
        self.chains = {"half_open": [], "closed": [], "count": 0}
        points = self.side3()
        while points:
            u, v = points.pop(0)
            count = 0
            loop = False
            cellshist = []
            dirhist = []
            cellshist.append((u, v))
            count, loop = self.incount(0, u, v, count, loop, cellshist, dirhist)
            data_chain = {
                    "directions": dirhist,
                    "chain": cellshist,
                    "count" : count
                }
            
            if loop:
                self.chains["closed"].append(data_chain)
            else:
                self.chains["half_open"].append(data_chain)
            
            points = list(filter(lambda p: p not in cellshist, points))

            # We say a chain is long if it contains at least three boxes.
            # It must be pointed out that in this rule, loops do not count as long chains. 
            if count >= 3:
                self.chains["count"] += 1 

    def side3(self):
        """
        Returns a list of coordinates of cells with value 3 (potential to be captured).
        
        Returns:
            list: A list of tuples representing the coordinates of cells with value 3.
        """
        side3_list = []
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.cells[i][j] == 3:
                    side3_list.append((i,j)) 
        return side3_list
    
    def amount_of_capturable_boxes(self):
        """Returns the total number of boxes in closed and half-open chains.
        
        Returns:
            int: The total number of capturable boxes in all chains.
        """
        amnt = 0
        for closed_chain in self.chains["closed"]:
            amnt += closed_chain["count"]
        
        for half_open_chain in self.chains["half_open"]:
            amnt += half_open_chain["count"]
        return amnt

    def amount_of_boxes_captured(self):
        """Returns the number of boxes that have all 4 edges.
        
        Returns:
            int: The total number of captured boxes (i.e., boxes with 4 edges).
        """
        return sum(self.p_)
    
    def unsafe3(self):
        """
        Returns actions for unsafe chains, including both single and double half-hearted actions.
        
        If there are closed or half-open chains, this method computes and returns actions
        to handle those chains. It ensures that chains are filled appropriately or handles special cases.

        Returns:
            list: A list of actions to take in unsafe chains.
            None: If no unsafe actions are found.
        """

        amount_of_closed_chains     = len(self.chains["closed"])
        amount_of_half_open_chains  = len(self.chains["half_open"])
        amount_of_capturable_boxes  = self.amount_of_capturable_boxes()
        boxes_already_captured      = self.amount_of_boxes_captured()
        amount_of_boxes             = self.num_rows * self.num_cols

        # check if there are closed chains first. 
        if self.chains["closed"]:
            if (amount_of_closed_chains == 1 and 
                amount_of_half_open_chains == 0 and 
                amount_of_capturable_boxes == 4 and 
                # at the end of the game, no half haerted handout:
                amount_of_boxes - boxes_already_captured != amount_of_capturable_boxes):
                
                chain_data = self.chains["closed"][0]
                dhh_action = self.get_double_half_haerted(
                    chain_data["chain"],
                    chain_data["directions"])
                fb_action = self.get_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                
                return [fb_action, dhh_action]
            
            else :
                chain_data = self.chains["closed"][0]
                fb_action = self.get_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                return [fb_action]
          
        if self.chains["half_open"]:
            if (amount_of_closed_chains == 0 and 
                amount_of_half_open_chains == 1 and 
                amount_of_capturable_boxes == 2 and 
                # at the end of the game, no half haerted handout:
                amount_of_boxes - boxes_already_captured != amount_of_capturable_boxes):

                chain_data = self.chains["half_open"][0]
                shh_action = self.get_single_half_haerted(
                    chain_data["chain"],
                    chain_data["directions"])
                fb_action = self.get_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                
                return [fb_action, shh_action]
            
            else :
                chain_data = self.chains["half_open"][0]
                fb_action = self.get_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                return [fb_action]
        return None

    def get_single_half_haerted(self, half_open_chain: list[(int,int)], directions:list[Directions]):
       """
       Computes an action for a single half-hearted chain.
        
       Args:
           half_open_chain (list): A list of coordinates (tuples) representing the half-open chain.
           directions (list): A list of directions that follows the half-open chain.
       
       Returns:
           Action: The action ID for the computed move.
       
       Raises:
           ValueError: If the half-open chain or directions are not valid.
        """
       assert len(half_open_chain) == 2
       assert len(directions) == 2

       u1, v1 = half_open_chain[0]
       u2, v2 = half_open_chain[1]

       if self.cells[u1][v1] == 3:
           nu, nv = u2, v2
           nd = directions[1]
       elif self.cells[u2][v2] == 3: 
           nu, nv = u1, v1
           nd = directions[0]
       else :
           assert ValueError("Error in get_single_half_haerted")

       if nd.value == Directions.DOWN.value:
           action = self.action_id(CellOrientation.HORIZONTAL, nu+1, nv)
           return action
       elif nd.value == Directions.UP.value:
           action = self.action_id(CellOrientation.HORIZONTAL, nu, nv)
           return action
       elif nd.value == Directions.LEFT.value:
           action = self.action_id(CellOrientation.VERTICAL, nu , nv)
           return action
       else : 
           action = self.action_id(CellOrientation.VERTICAL, nu, nv+1)
           return action

    def get_double_half_haerted(self, closed_chain:list[(int,int)], directions:list[Directions]):
        """
        Computes an action for a double half-hearted chain.
        
        Args:
            closed_chain (list): A list of coordinates (tuples) representing the closed chain.
            directions (list): A list of directions for the closed chain.
        
        Returns:
            Action: The action ID for the computed move.
        """
        assert len(closed_chain) == 4
        assert len(directions) == 3

        u, v = closed_chain[1]
        direction = directions[1]

        if direction.value == Directions.DOWN.value:
            action = self.action_id(CellOrientation.HORIZONTAL, u+1, v)
            return action
        elif direction.value == Directions.UP.value:
            action = self.action_id(CellOrientation.HORIZONTAL, u-1, v)
            return action
        elif direction.value == Directions.LEFT.value:
            action = self.action_id(CellOrientation.VERTICAL, u, v)
            return action
        else : 
            action = self.action_id(CellOrientation.VERTICAL, u, v+1)
            return action

    def get_fill_box(self, closed_chain:list[(int,int)], directions:list[Directions]):
        """
        Computes the action to fill a box in a closed chain.
        
        Args:
            closed_chain (list): A list of coordinates (tuples) representing the closed chain.
            directions (list): A list of directions for the closed chain.
        
        Returns:
            Action: The action ID for filling the box.
        """
        assert len(closed_chain) >= 1
        assert len(directions) >= 1

        counter = 0
        for u, v in closed_chain :
            if self.cells[u][v] == 3:
                nu, nv = u, v
                nd = directions[counter]
                break
            counter += 1

        if nd.value == Directions.UP.value:
            action = self.action_id(CellOrientation.HORIZONTAL, nu, nv)
        
        elif nd.value == Directions.LEFT.value:
            action = self.action_id(CellOrientation.VERTICAL, nu, nv)
        
        elif nd.value == Directions.DOWN.value:
            action = self.action_id(CellOrientation.HORIZONTAL, nu+1, nv)
        else : 
            action = self.action_id(CellOrientation.VERTICAL, nu, nv+1)

        return action

    def incount(self, k:int, i:int, j:int, count:int, loop:bool, cellshist:list, dirhist:list):
        """
        Recursively counts the boxes in a chain and tracks the direction of movement.
        
        Args:
            k (int): Direction of movement (1, 2, 3, or 4).
            i (int): Row index of the current cell.
            j (int): Column index of the current cell.
            count (int): Current count of steps.
            loop (bool): Flag to check if a loop is formed.
            cellshist (list): List of visited cells in the chain.
            dirhist (list): List of directions taken in the chain.

        Returns:
            tuple: Updated count of steps and a loop flag.
        """
        count+=1    

        if (k!=1 and self.v_[i][j]<1) :
            dirhist.append(Directions.LEFT)
            if (j>0):  
                if (self.cells[i][j-1]>2): 
                    count+=1
                    loop=True
                    cellshist.append((i,j-1))

                elif (self.cells[i][j-1]>1):
                    cellshist.append((i,j-1))
                    count, loop = self.incount(3,i,j-1, count, loop, cellshist, dirhist)
                
        elif (k!=2 and self.h_[i][j]<1) :
            dirhist.append(Directions.UP)
            if (i>0):
                if (self.cells[i-1][j]>2):
                    count+=1
                    loop=True
                    cellshist.append((i-1,j))
                    
                elif (self.cells[i-1][j]>1):
                    cellshist.append((i-1,j))
                    count, loop = self.incount(4,i-1,j, count, loop, cellshist, dirhist)
            
        elif (k!=3 and self.v_[i][j+1]<1):
            dirhist.append(Directions.RIGHT)
            if (j < self.num_cols-1):

                if (self.cells[i][j+1]>2):
                    count+=1
                    loop=True
                    cellshist.append((i,j+1))

                elif (self.cells[i][j+1]>1):
                    cellshist.append((i,j+1))
                    count, loop = self.incount(1,i,j+1, count, loop, cellshist, dirhist)
                

        elif (k!=4 and self.h_[i+1][j]<1):
            dirhist.append(Directions.DOWN)
            if (i< self.num_rows-1):

                if (self.cells[i+1][j] > 2):
                    count+=1
                    loop= True
                    cellshist.append((i+1,j))

                elif (self.cells[i+1][j] > 1):
                    cellshist.append((i+1,j))
                    count, loop = self.incount(2,i+1,j, count, loop, cellshist, dirhist)

        return count, loop

    def get_available_action(self, 
                             state, 
                             cache_chains:Transposition_Table_Chains,  
                             maximizing_player_id:int):
        """
        Returns the best available action based on different strategies.

        Args:
            state (State): The current game state. (pyspiel)
            cache_chains (Transposition_Table_Chains): A cache of previously computed chains.
            maximizing_player_id (int): The ID of the maximizing player.

        Returns:
            list: A list of possible actions.
        """

        # TODO: use caching for the chains.
        # self.obtain_chains(cache_chains, state)
        
        self.find_all_chains()
        
        # 1) singletons and doubletons
        possible_actions = self.safe3()
        if possible_actions :
            return possible_actions
        
        # 2) chains
        possible_actions = self.unsafe3()
        if possible_actions :
            return possible_actions

        # 3) random safe edge 
        possible_actions = self.side1()
        if possible_actions : 
            return possible_actions
                
        # 4) last resort
        # instead of returning all legal actions
        # filter the actions that do not respect the 
        # long chain rule, which causes the braching
        # factor to lower as well.
        
        # TODO: use lcr rule to reduce possible actions.
        # long_chain_rule_actions = self.get_lcr_actions(possible_actions, cache_chains, maximizing_player_id)
        
        # The remaining moves are explored by considering edges in
        # an order radiating outwards from the center of the board. 
        
        # This is a very effective heuristic, despite its extreme sim-
        # plicity. On the 4 × 4 solution, for example, this approach
        # reduced the runtime by a factor of 17 over a simple left-to-
        # right, top-to-bottom move order. (see paper by Barker and Korf)

        # TODO: use move_ordering heuristcs.
        # actions  = self.moveOrdening(state, long_chain_rule_actions, maximizing_player_id)

        actions = state.legal_actions()
        
        # TODO: Last resort, you have to limit the actions if the 
        # algorithm needs to be scalable to every possible game.
        # but this should a paramter, not hardcoded.
        num_to_pick = min(10, len(actions))
        actions = r.sample(actions, num_to_pick)
        
        return actions

    def obtain_chains(self, cache_chains:list, state):
        """
        Retrieves the cached chains or computes them if not available.

        Args:
            cache_chains (Transposition_Table_Chains): A cache of previously computed chains.
            state (State): The current game state.
        """
        chains_object = cache_chains.get(state.dbn_string())
        if chains_object:
            self.chains = chains_object
        else : 
            self.find_all_chains()
            cache_chains.set(state.dbn_string(), self.chains)
    
    # TODO: implement the long chain rule in an efficient manner
    def get_lcr_actions(self, actions, cache_chains, maximizing_player_id):
        pass

    # TODO: implement move ordering in order to sort the possible
    # actions from the center of the board to the outer walls
    def moveOrdening(self, state, lcr_actions, maximizing_player_id):
        pass
    
    def side1(self, seed=None):
        """
        Randomly selects a valid horizontal or vertical edge to place a move.

        Args:
            seed (int, optional): Random seed for reproducibility.

        Returns:
            list: A list containing the selected action (or None if no valid move is found).
        """
        if seed is not None:
            r.seed(seed)

        if r.random() < 0.5: 
            orien = CellOrientation.HORIZONTAL
        else :
            orien = CellOrientation.VERTICAL

        i = r.randint(0, self.num_rows - 1)
        j = r.randint(0, self.num_cols - 1)

        if orien.value == CellOrientation.HORIZONTAL.value:
            pos = self.rand_hedge(i, j)
            if pos:
                x, y = pos
                action = self.action_id(CellOrientation.HORIZONTAL, x, y)
                return [action]
            
            else:
                pos = self.rand_vedge(i, j)
                if pos:
                    x, y = pos
                    action = self.action_id(CellOrientation.VERTICAL, x, y)
                    return [action]
                
        else:
            pos = self.rand_vedge(i, j)
            if pos:
                x, y = pos
                action = self.action_id(CellOrientation.VERTICAL, x, y)
                return [action]
            else:
                pos = self.rand_hedge(i, j)
                if pos:
                    x, y = pos
                    action = self.action_id(CellOrientation.HORIZONTAL, x, y)
                    return [action]
                
        return None

    def rand_hedge(self, i:int, j:int):
        """
        Searches for a valid horizontal edge to place a move.

        Args:
            i (int): Row index of the current cell.
            j (int): Column index of the current cell.

        Returns:
            tuple: Coordinates (x, y) of the valid edge or None if no valid edge is found.
        """
        x = i
        y = j
        while True:
            if self.safe_hedge(x, y):
                return x, y
            else:
                y += 1
                if y == self.num_cols:
                    y = 0
                    x += 1
                    if x > self.num_rows:
                        x = 0
            if x == i and y == j:
                break
        return None

    def rand_vedge(self, i:int, j:int):
        """
        Searches for a valid vertical edge to place a move.

        Args:
            i (int): Row index of the current cell.
            j (int): Column index of the current cell.

        Returns:
            tuple: Coordinates (x, y) of the valid edge or None if no valid edge is found.
        """
        x = i
        y = j
        while True:
            if self.safe_vedge(x, y):
                return x, y 
            else:
                y += 1
                if y > self.num_cols:
                    y = 0
                    x += 1
                    if x == self.num_rows:
                        x = 0
            if x == i and y == j:
                break
        return None

    def safe_hedge(self, i:int, j:int):
        """
        Checks if a horizontal edge is safe to place a move.

        Args:
            i (int): Row index of the current cell.
            j (int): Column index of the current cell.

        Returns:
            bool: True if the edge is safe, False otherwise.
        """
        if self.h_[i][j] < 1:
            if i == 0:
                if self.cells[i][j] < 2:
                    return True
            elif i == self.num_rows:
                if self.cells[i - 1][j] < 2:
                    return True
            elif self.cells[i][j] < 2 and self.cells[i - 1][j] < 2:
                return True
        return False

    def safe_vedge(self, i:int, j:int):
        """
        Checks if a vertical edge is safe to place a move.

        Args:
            i (int): Row index of the current cell.
            j (int): Column index of the current cell.

        Returns:
            bool: True if the edge is safe, False otherwise.
        """
        if self.v_[i][j] < 1:
            if j == 0:
                if self.cells[i][j] < 2:
                    return True
            elif j == self.num_cols:
                if self.cells[i][j - 1] < 2:
                    return True
            elif self.cells[i][j] < 2 and self.cells[i][j - 1] < 2:
                return True
        return False

if __name__ == "__main__":
    SA = StrategyAdvisor(10,10)
    # example_paper(SA)
    # horizontal_closed_chain(SA)
    # vertical_closed_chain(SA)
    # SA.unsafe3()
    # closed_chain_data = SA.chains["closed"][0]
    # closed_chain = closed_chain_data["chain"]
    # closed_dir   = closed_chain_data["directions"]
    # SA.get_double_half_haerted(closed_chain,closed_dir)
