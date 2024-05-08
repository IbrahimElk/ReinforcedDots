import numpy as np
import random as r

from MARL.task3.dotsandboxes_agent.util import CellOrientation, Directions
from examples import horizontal_closed_chain, vertical_closed_chain, example_paper, horizontal_half_open_chain1, horizontal_half_open_chain2, vertical_half_open_chain1
Action = int

class StrategyAdvisor : 
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.player = 1
        self.score = [0, 0]
        self.h_ = [[0] * cols for _ in range(rows + 1)]
        self.v_ = [[0] * (cols + 1) for _ in range(rows)]
        self.cells = [[0] * cols for _ in range(rows)]
        self.chains = {"half_open": [], "closed": []}

    def action_id(self, orientation_:CellOrientation, row_:int, col_:int):
        """
        - Translate the row, column and orientation of the edge to an Action. 
        """
        action = 0
        maxh  = (self.rows + 1) * self.cols
        if (orientation_ == CellOrientation.HORIZONTAL):
            action = row_ * self.cols + col_
        else :
            action = maxh + row_ * (self.cols + 1) + col_
        return action

    def safe3(self):
        """
        - Returns an actions that capture a singleton or a doubleton.
        """
        for row in range(0,self.rows):
            for col in range(0,self.cols):
                if self.cells[row][col] == 3:
                    if self.vedge[row][col] < 1:
                        if col == 0 or self.cells[row][col-1] != 2 :
                            action = self.action_id(CellOrientation.VERTICAL,row,col)
                            return [action]
                        
                    elif self.h_[row][col] < 1:
                        if row == 0 or self.cells[row-1][col] != 2:
                            action = self.action_id(CellOrientation.HORIZONTAL,row,col)
                            return [action]

                    elif self.v_[row][col+1] < 1:
                        if col == self.cols-1 or self.cells[row][col+1] != 2:
                            action = self.action_id(CellOrientation.VERTICAL,row,col)
                            return [action]

                    else :
                        if row == self.rows-1 or self.cells[row+1][col] != 2:
                            action = self.action_id(CellOrientation.HORIZONTAL,row,col)
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
        # TODO: to increase efficiency, dont calculate this evrytime: 
        # if not self.chains["half_open"] and not self.chains["closed"]:
        self.find_all_chains()
        print("closed chains")
        print(self.chains["closed"])
        print("half open chains")
        print(self.chains["half_open"])

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
                fb_action = self.draw_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                
                return [dhh_action, fb_action]
            
            else :
                chain_data = self.chains["closed"][0]

                fb_action = self.draw_fill_box(
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
                fb_action = self.draw_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                
                return [shh_action, fb_action]
            
            else :
                chain_data = self.chains["half_open"][0]

                fb_action = self.draw_fill_box(
                    chain_data["chain"],
                    chain_data["directions"])
                return [fb_action]
        return None

    def get_single_half_haerted(self, half_open_chain: list[(int,int)], directions:list[Directions]):
        assert len(half_open_chain) == 2

        u, v = half_open_chain[1]
        direction = directions[1]

        if direction == Directions.DOWN:
            print(CellOrientation.HORIZONTAL, u+1, v)
            action = self.action_id(CellOrientation.HORIZONTAL, u+1, v)
            return action
        elif direction == Directions.UP:
            print(CellOrientation.HORIZONTAL, u-1, v)
            action = self.action_id(CellOrientation.HORIZONTAL, u-1, v)
            return action
        elif directions == Directions.LEFT:
            print(CellOrientation.VERTICAL, u, v)
            action = self.action_id(CellOrientation.VERTICAL, u, v)
            return action
        else : 
            print(CellOrientation.VERTICAL, u, v+1)
            action = self.action_id(CellOrientation.VERTICAL, u, v+1)
            return action

    def get_double_half_haerted(self, closed_chain:list[(int,int)], directions:list[Directions]):
        assert len(closed_chain) == 4
        assert len(directions) == 3

        u, v = closed_chain[1]
        direction = directions[1]

        if direction == Directions.DOWN:
            print(CellOrientation.HORIZONTAL, u+1, v)
            action = self.action_id(CellOrientation.HORIZONTAL, u+1, v)
            return action
        elif direction == Directions.UP:
            print(CellOrientation.HORIZONTAL, u-1, v)
            action = self.action_id(CellOrientation.HORIZONTAL, u-1, v)
            return action
        elif directions == Directions.LEFT:
            print(CellOrientation.VERTICAL, u, v)
            action = self.action_id(CellOrientation.VERTICAL, u, v)
            return action
        else : 
            print(CellOrientation.VERTICAL, u, v+1)
            action = self.action_id(CellOrientation.VERTICAL, u, v+1)
            return action

    def get_fill_box(self, closed_chain:list[(int,int)], directions:list[Directions]):
        u, v = closed_chain[0]
        direction = directions[0]

        if direction == Directions.DOWN:
            print(CellOrientation.HORIZONTAL, u+1, v)
            action = self.action_id(CellOrientation.HORIZONTAL, u+1, v)
        elif direction == Directions.UP:
            print(CellOrientation.HORIZONTAL, u-1, v)
            action = self.action_id(CellOrientation.HORIZONTAL, u-1, v)
        elif directions == Directions.LEFT:
            print(CellOrientation.VERTICAL, u, v)
            action = self.action_id(CellOrientation.VERTICAL, u, v)
        else : 
            print(CellOrientation.VERTICAL, u, v+1)
            action = self.action_id(CellOrientation.VERTICAL, u, v+1)

        return action

    def incount(self, k, i, j, count, loop, cellshist, dirhist):
        count+=1    

        if (k!=1 and self.v_[i][j]<1) :
            if (j>0):  
                dirhist.append(Directions.LEFT)

                if (self.cells[i][j-1]>2): 
                    count+=1
                    loop=True
                    cellshist.append((i,j-1))
                    # dirhist.append(Directions.LEFT)

                elif (self.cells[i][j-1]>1):
                    # dirhist.append(Directions.LEFT)
                    cellshist.append((i,j-1))
                    count, loop = self.incount(3,i,j-1, count, loop, cellshist, dirhist)
                
                dirhist.append(Directions.LEFT)

        elif (k!=2 and self.h_[i][j]<1) :
            if (i>0):
                dirhist.append(Directions.UP)

                if (self.cells[i-1][j]>2):
                    count+=1
                    loop=True
                    cellshist.append((i-1,j))
                    # dirhist.append(Directions.UP)
                    
                elif (self.cells[i-1][j]>1):
                    cellshist.append((i-1,j))
                    # dirhist.append(Directions.UP)
                    count, loop = self.incount(4,i-1,j, count, loop, cellshist, dirhist)
            
        elif (k!=3 and self.v_[i][j+1]<1):
            if (j < self.cols-1):
    
                dirhist.append(Directions.RIGHT)

                if (self.cells[i][j+1]>2):
                    count+=1
                    loop=True
                    cellshist.append((i,j+1))
                    # dirhist.append(Directions.RIGHT)

                elif (self.cells[i][j+1]>1):
                    cellshist.append((i,j+1))
                    # dirhist.append(Directions.RIGHT)
                    count, loop = self.incount(1,i,j+1, count, loop, cellshist, dirhist)
                

        elif (k!=4 and self.h_[i+1][j]<1):
            if (i< self.rows-1):
            
                dirhist.append(Directions.DOWN)

                if (self.cells[i+1][j] > 2):
                    count+=1
                    loop= True
                    cellshist.append((i+1,j))
                    # dirhist.append(Directions.DOWN)

                elif (self.cells[i+1][j] > 1):
                    cellshist.append((i+1,j))
                    # dirhist.append(Directions.DOWN)
                    count, loop = self.incount(2,i+1,j, count, loop, cellshist, dirhist)

        return count, loop

    # na de actie1 of actie2 beste actie te weten, dan beste actie na die actie te ondernemen? za
    def get_available_action(self, state):
        # 1 singletons and doubletons
        action = self.safe3()
        if action :
            return action
        
        # 2 chains
        actions = self.unsafe3()
        if actions :
            return actions
        
        # 3 random safe edge 
        action = self.side1()
        if action : 
            return action
        
        # last resprt: 
        return state.legal_actions()

    def side1(self):
        if r.random() < 0.5: 
            orien = CellOrientation.HORIZONTAL
        else :
            orien = CellOrientation.VERTICAL

        i = r.randint(0, self.rows - 1)
        j = r.randint(0, self.cols - 1)

        if orien == CellOrientation.HORIZONTAL:
            if self.rand_hedge(i, j):
                action = self.action_id(CellOrientation.HORIZONTAL, i, j)
                return action
            
            else:
                if self.rand_vedge(i, j):
                    action = self.action_id(CellOrientation.VERTICAL, i, j)
                    return action
                
        else:
            if self.rand_vedge(i, j):
                action = self.action_id(CellOrientation.VERTICAL, i, j)
                return action
                                    
            else:
                if self.rand_hedge(i, j):
                    action = self.action_id(CellOrientation.HORIZONTAL, i, j)
                    return action
                
        return None
    
    def rand_hedge(self, i, j):
        for x in range(i, self.rows + 2):
            for y in range(j, self.cols + 1):
                if self.safe_hedge(x, y):
                    return True
                
        for x in range(0, i):
            for y in range(0, j):
                if self.safe_hedge(x, y):
                    return True
        return False

    def rand_vedge(self, i ,j):
        for x in range(i, self.rows + 1):
            for y in range(j, self.cols + 2):
                if self.safe_vedge(x, y):
                    return True
                
        for x in range(0, i):
            for y in range(0, j):
                if self.safe_vedge(x, y):
                    return True
        return False

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


    #FIXME: dit is in andere file: 
    # eval functie moet zijn om de punten van de tegenstander te minimaliseren !!!
    # niet uw eigen munten maximalisreen in limited depth !!
    # zo denk ik ook wanneer ik het spel speel!

    # def minimax(self):
    #     # ipv state.legal_actions, gebruik : 
    #     possible_action = self.get_available_action(state)

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

# UNIT TEST get_double_half_haerted

    # vertical_closed_chain(SA)
    # SA.find_all_chains()

    # horizontal_closed_chain(SA)
    # SA.find_all_chains()

    # print(SA.chains)
    # chain_data = SA.chains["closed"][0]
    # SA.get_double_half_haerted(chain_data["chain"], chain_data["directions"])

# UNIT TEST get_single_half_haerted

    # horizontal_half_open_chain1(SA)
    # SA.find_all_chains()

    # horizontal_half_open_chain2(SA)
    # SA.find_all_chains()

    # vertical_half_open_chain1(SA)
    # SA.find_all_chains()

    # print(SA.chains)
    # chain_data = SA.chains["half_open"][0]
    # SA.get_single_half_haerted(chain_data["chain"], chain_data["directions"])