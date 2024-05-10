import os
import sys
import math
parent_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

import random as r
import numpy as np
from util import CellOrientation, Directions

# type Alias
Action = int

# FIXME:
# An obvious heuristic would be to consider capturing
# moves first; however, all such moves are part of chains and
# are dealt with by the rules of the previous section. Thus,
# our move ordering only considers non-capturing moves. Of
# those, the heuristic considers moves that fill in the third edge
# of a box last, as they leave a capturable box for the opponent.
# The remaining moves are explored by considering edges in
# an order radiating outwards from the center of the board.
# This is a very effective heuristic, despite its extreme sim-
# plicity. On the 4 × 4 solution, for example, this approach
# reduced the runtime by a factor of 17 over a simple left-to-
# right, top-to-bottom move order.

class StrategyAdvisor : 
    def __init__(self, rows, cols):
        self.num_rows = rows
        self.num_cols = cols
        
        self.rows = rows
        self.cols = cols

        self.h_ = [[0] * cols for _ in range(rows + 1)]
        self.v_ = [[0] * (cols + 1) for _ in range(rows)]
        self.cells = [[0] * cols for _ in range(rows)]
        self.chains = {"half_open": [], "closed": []}

    def clone(self):
        cloned_advisor = StrategyAdvisor(self.num_rows, self.num_cols)
        cloned_advisor.h_ = [row[:] for row in self.h_]
        cloned_advisor.v_ = [row[:] for row in self.v_]
        cloned_advisor.cells = [row[:] for row in self.cells]
        cloned_advisor.chains = {"half_open": self.chains["half_open"][:], "closed": self.chains["closed"][:]}
        return cloned_advisor

    def get_tabular_form(self, action):
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
        
    def update_action(self, action):
        orien, i, j = self.get_tabular_form(action)
        if orien.value == CellOrientation.HORIZONTAL.value : 
            self.set_h_edge(i,j)
        else : 
            self.set_v_edge(i,j)         

    def update_edge(self, orien:CellOrientation, i, j):
        if orien.value == CellOrientation.HORIZONTAL.value : 
            self.set_h_edge(i,j)
        else : 
            self.set_v_edge(i,j)

    def set_h_edge(self, x, y):
        self.h_[x][y] = 1
        if x > 0:
            self.cells[x - 1][y] += 1
        if x < self.rows:
            self.cells[x][y] += 1

    def set_v_edge(self, x, y):
        self.v_[x][y] = 1
        if y > 0:
            self.cells[x][y - 1] += 1
        if y < self.cols:
            self.cells[x][y] += 1


    def action_id(self, orientation_:CellOrientation, row_:int, col_:int):
        """
        - Translate the row, column and orientation of the edge to an Action. 
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

    def safe3(self):
        """
        - Returns an actions that capture a singleton or a doubleton.
        """
        for row in range(0,self.rows):
            for col in range(0,self.cols):
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
                        if col == self.cols-1 or self.cells[row][col+1] != 2:
                            action = self.action_id(CellOrientation.VERTICAL, row, col+1)
                            return [action]
                    else :
                        if row == self.rows-1 or self.cells[row+1][col] != 2:
                            action = self.action_id(CellOrientation.HORIZONTAL, row+1, col)
                            return [action]
        return None
    
    def side3(self):
        side3_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j] == 3:
                    side3_list.append((i,j)) 
        return side3_list
    
    def find_all_chains(self):
        self.chains = {"half_open": [], "closed": []}
        points = self.side3()
        while points:
            u, v = points.pop(0)
            count = 0
            loop = False
            cellshist = []
            dirhist = []
            cellshist.append((u, v))
            count, loop = self.incount(0, u, v, count, loop, cellshist, dirhist)
            points = list(filter(lambda p: p not in cellshist, points))
            if loop:
                data_chain = {
                    "directions": dirhist,
                    "chain": cellshist,
                    "count" : count
                }
                self.chains["closed"].append(data_chain)
            else:
                data_chain = {
                    "directions": dirhist,
                    "chain": cellshist,
                    "count" : count
                }
                self.chains["half_open"].append(data_chain)

    def amount_of_capturable_boxes(self):
        # aantal boxes in een chain opgeteld over alle chains.
        amnt = 0
        for closed_chain in self.chains["closed"]:
            amnt += closed_chain["count"]
        
        for half_open_chain in self.chains["half_open"]:
            amnt += half_open_chain["count"]
        return amnt

    def unsafe3(self):
        self.find_all_chains()

        # check if there are closed chains first. 
        amount_of_closed_chains     = len(self.chains["closed"])
        amount_of_half_open_chains  = len(self.chains["half_open"])
        amount_of_capturable_boxes  = self.amount_of_capturable_boxes()
        
        if self.chains["closed"]:
            if (amount_of_closed_chains == 1 and 
                amount_of_half_open_chains == 0 and 
                amount_of_capturable_boxes == 4):

                chain_data = self.chains["closed"][0]
                dhh_action = self.get_double_half_haerted(
                    chain_data["chain"],
                    chain_data["directions"])
                fb_action = self.get_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                
                return [dhh_action, fb_action]
            
            else :
                chain_data = self.chains["closed"][0]
                fb_action = self.get_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                return [fb_action]
          
        if self.chains["half_open"]:
            if (amount_of_closed_chains == 0 and 
                amount_of_half_open_chains == 1 and 
                amount_of_capturable_boxes == 2):

                chain_data = self.chains["half_open"][0]
                shh_action = self.get_single_half_haerted(
                    chain_data["chain"],
                    chain_data["directions"])
                fb_action = self.get_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                
                return [shh_action, fb_action]
            
            else :
                chain_data = self.chains["half_open"][0]
                fb_action = self.get_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                return [fb_action]
        return None

    def get_single_half_haerted(self, half_open_chain: list[(int,int)], directions:list[Directions]):
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
        elif directions.value == Directions.LEFT.value:
            action = self.action_id(CellOrientation.VERTICAL, u, v)
            return action
        else : 
            action = self.action_id(CellOrientation.VERTICAL, u, v+1)
            return action

    def get_fill_box(self, closed_chain:list[(int,int)], directions:list[Directions]):
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

    def incount(self, k, i, j, count, loop, cellshist, dirhist):
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
            if (j < self.cols-1):

                if (self.cells[i][j+1]>2):
                    count+=1
                    loop=True
                    cellshist.append((i,j+1))

                elif (self.cells[i][j+1]>1):
                    cellshist.append((i,j+1))
                    count, loop = self.incount(1,i,j+1, count, loop, cellshist, dirhist)
                

        elif (k!=4 and self.h_[i+1][j]<1):
            dirhist.append(Directions.DOWN)
            if (i< self.rows-1):

                if (self.cells[i+1][j] > 2):
                    count+=1
                    loop= True
                    cellshist.append((i+1,j))

                elif (self.cells[i+1][j] > 1):
                    cellshist.append((i+1,j))
                    count, loop = self.incount(2,i+1,j, count, loop, cellshist, dirhist)

        return count, loop

    # na de actie1 of actie2 beste actie te weten, dan beste actie na die actie te ondernemen? za
    def get_available_action(self, state):
        # 1) singletons and doubletons
        action = self.safe3()
        if action :
            return action
        
        # 2) chains
        actions = self.unsafe3()
        if actions :
            return actions
        
        # 3) random safe edge 
        action = self.side1()
        if action : 
            return action
        
        # 4) last resort
        return state.legal_actions()

    def side1(self, seed=None):
        if seed is not None:
            r.seed(seed)

        if r.random() < 0.5: 
            orien = CellOrientation.HORIZONTAL
        else :
            orien = CellOrientation.VERTICAL

        i = r.randint(0, self.rows - 1)
        j = r.randint(0, self.cols - 1)

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

    def rand_hedge(self, i, j):
        x = i
        y = j
        while True:
            if self.safe_hedge(x, y):
                return x, y
            else:
                y += 1
                if y == self.cols:
                    y = 0
                    x += 1
                    if x > self.rows:
                        x = 0
            if x == i and y == j:
                break
        return None

    def rand_vedge(self, i, j):
        x = i
        y = j
        while True:
            if self.safe_vedge(x, y):
                return x, y 
            else:
                y += 1
                if y > self.cols:
                    y = 0
                    x += 1
                    if x == self.rows:
                        x = 0
            if x == i and y == j:
                break
        return None

    def safe_hedge(self, i, j):
        if self.h_[i][j] < 1:
            if i == 0:
                if self.cells[i][j] < 2:
                    return True
            elif i == self.rows:
                if self.cells[i - 1][j] < 2:
                    return True
            elif self.cells[i][j] < 2 and self.cells[i - 1][j] < 2:
                return True
        return False

    def safe_vedge(self, i, j):
        if self.v_[i][j] < 1:
            if j == 0:
                if self.cells[i][j] < 2:
                    return True
            elif j == self.cols:
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
