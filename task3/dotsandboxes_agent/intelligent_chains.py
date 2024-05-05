import math 
import random
from cell_orientation import CellOrientation

def action_id(num_rows_:int, num_cols_:int, orientation_:CellOrientation, row_:int, col_:int):
  action = 0
  maxh  = (num_rows_ + 1) * num_cols_
  if (orientation_ == CellOrientation.HORIZONTAL):
    action = row_ * num_cols_ + col_
  else :
    action = maxh + row_ * (num_cols_ + 1) + col_
  return action

def safe3s(rows, cols, cells, vedge, hedge):
    """
    - Take all singleton and doubleton 3's.	

    - box[i][j-1]!=2: This constraint checks if the box to the left 
    of the current box (i, j) does not have a value of 2 
    (which means it is not a doubleton). 
    If this condition is true, it allows setting the vertical edge 
    to the left of the current box (i, j).
    in other words, you dont create a 3-edge chain to the left of this box. 
    """
    # legal_actions_in_order = [] 
    for row in range(0,rows):
        for col in range(0,cols):
            if cells[row][col] == 3:
                if vedge[row][col] < 1:
                    if col == 0 or cells[row][col-1] != 2 :
                        # setvedge(i,j)
                        # find the action that represents this. 
                        # vertical edge at (i,j)
                        action = action_id(rows,cols,CellOrientation.VERTICAL,row,col)
                        # legal_actions_in_order.append(action)
                        return action
                    
                elif hedge[row][col] < 1:
                    if row == 0 or cells[row-1][col] != 2:
                        # sethedge(i,j)
                        action = action_id(rows,cols,CellOrientation.HORIZONTAL,row,col)
                        # legal_actions_in_order.append(action)
                        return action

                elif vedge[row][col+1] < 1:
                    if col == cols-1 or cells[row][col+1] != 2:
                        # setvedge(i,j+1)
                        action = action_id(rows,cols,CellOrientation.VERTICAL,row,col)
                        # legal_actions_in_order.append(action)
                        return action

                else :
                    if row == rows-1 or cells[row+1][col] != 2:
                        # sethedge(i,j)
                        action = action_id(rows,cols,CellOrientation.HORIZONTAL,row,col)
                        # legal_actions_in_order.append(action)
                        return action
    return None
    # return legal_actions_in_order

def sides3(rows, cols, cells) :    # Returns u,v if there is a box(u,v)=3.
	for i in range(0, rows) :
		for j in range(0, cols):
			if (cells[i][j]==3):
				return i, j
	return None

def safehedge(i, j, h_, cells, rows):
    if h_[i][j] < 1:
        if i == 0:
            if cells[i][j] < 2:
                return True
        elif i == rows:
            if cells[i - 1][j] < 2:
                return True
        elif cells[i][j] < 2 and cells[i - 1][j] < 2:
            return True
    return False

def safevedge(i, j, v_, cells, cols):
    if v_[i][j] < 1:
        if j == 0:
            if cells[i][j] < 2:
                return True
        elif j == cols:
            if cells[i][j - 1] < 2:
                return True
        elif cells[i][j] < 2 and cells[i][j - 1] < 2:
            return True
    return False

def rand_hedge(i, j, h_, cells, rows, cols):
    x = i
    y = j
    while True:
        if safehedge(x, y, h_, cells, rows):
            return x, y
        else:
            y += 1
            if y == cols:
                y = 0
                x += 1
                if x > rows:
                    x = 0
        if x != i or y != j:
            break
    return None

def rand_vedge(i, j, v_ , cells, rows, cols):
    x = i
    y = j
    while True:
        if safevedge(x, y, v_, cells, cols):
            return x, y
        else:
            y += 1
            if y > cols:
                y = 0
                x += 1
                if x == rows:
                    x = 0
        if x != i or y != j:
            break
    return None

def sides01(rows, cols, h_, v_, cells) :
    """
    Returns true and orien, x, y if there is a safe edge (x,y).
    """
    # zz=1 if horizontal, zz=2 if vertical
    if random.random()< 0.5:
        zz=1 
    else: 
        zz=2  

    i = math.floor(rows*random.random())
    j = math.floor(cols*random.random())
        
    if (zz==1):
        loc = rand_hedge(i, j, h_, cells, rows, cols)
        if loc:
            x, y = loc 
            return CellOrientation.HORIZONTAL, x, y 
        else:
            zz=2
            loc = rand_vedge(i, j, v_, cells, rows, cols)
            if loc:
                x, y = loc 
                return CellOrientation.VERTICAL, x, y 
    else :
        loc = rand_vedge(i, j, v_, cells, rows, cols)
        if loc:
            x, y = loc
            return CellOrientation.VERTICAL, x, y 
        else :
            zz=1
            loc = rand_hedge(i, j, h_, cells, rows, cols)
            if loc:
                x, y = loc 
                return CellOrientation.HORIZONTAL, x, y 
    return None

def all3s(h_, v_) :
    legal_actions_in_order = []
    d = sides3()
    while d:
        u,v = d
        takebox(u,v, h_, v_)
        legal_actions_in_order.append(u,v)
        d = sides3()
    return legal_actions_in_order

def sethedge(i,j):
    pass

def setvedge(i,j):
    pass

def takebox(i,j, h_, v_, rows, cols):
    if (h_[i][j]<1):
        # sethedge(i,j)
        action = action_id(rows,cols,CellOrientation.HORIZONTAL,i,j)
        return action

    elif (v_[i][j]<1): 
        # setvedge(i,j)
        action = action_id(rows,cols,CellOrientation.VERTICAL,i,j)
        return action

    elif (v_[i+1][j]<1): 
        # sethedge(i+1,j)
        action = action_id(rows,cols,CellOrientation.HORIZONTAL,i+1,j)
        return action

    else: 
        # setvedge(i,j+1)
        action = action_id(rows,cols,CellOrientation.VERTICAL,i,j+1)
        return action

def sac(i, j, rows, cols, h_, v_, points, cells):     # sacrifices two squares if there are still 3's
    count=0
    loop=False
    # count aantal boxes vanaf box(i,j)
    incount(0, i, j, rows, cols, count, loop, h_, v_, cells)
    
    # if chain is half open, use half haerted technique
    if not loop:
        takeallbut(i,j)
    
    # if last step, pak dan alle boxes. 
    if (count + points[0] + points[1] == rows*cols):
        legal_actions_in_order = all3s(h_, v_)
    
    else:
        # if chain closed: 
        if (loop):
            # why consider only -2 of the boxes if the chain is closed. 
            # kmoet eens incount runnen op een game state om die volledig te begrijpen ig. 
            # analoog met deze functie.
            count=count-2

        legal_actions_in_order = []
        outcount(0, i, j, count, h_, v_, rows, cols, legal_actions_in_order)
        i=rows
        j=cols

def incount(k, i, j, rows, cols, count, loop, h_, v_, cells):
    count+=1              
    if (k!=1 and v_[i][j]<1) :
        if (j>0):  

			#      *----*---*
			# 	   |		|
			# 	   *----*---*
			#             
            if (cells[i][j-1]>2): 
                count+=1
                loop=True

			#      *----*---*
			# 	   			|
			# 	   *----*---*

			#      *----*---*
			#  	   |		|
			#  	   *	*---*
			#  
			#      * 	*---*
			#  	   |		|
			#  	   *----*---*
                
            elif (cells[i][j-1]>1):
                incount(3,i,j-1,rows, cols, count, loop, h_, v_, cells)

    elif (k!=2 and h_[i][j]<1) :
        if (i>0):

            #      *----*
            #  	   |    |
            #      * 	*
            #  	   |    |
            #  	   *----*

            if (cells[i-1][j]>2):
                count+=1
                loop=True

            #      *----*
            #  	        |
            #      * 	*
            #  	   |    |
            #  	   *----*	

            #      *----*
            #  	   |     
            #      * 	*
            #  	   |    |
            #  	   *----*	

            #      * 	*
            #  	   |    | 
            #      * 	*
            #  	   |    |
            #  	   *----*
            	
            elif (cells[i-1][j]>1):
                incount(4,i-1,j,rows, cols, count, loop, h_, v_, cells)
		
    elif (k!=3 and v_[i][j+1]<1):
        if (j < cols-1):		

            #      *----*---*
			# 	   |		|
			# 	   *----*---*
   
            if (cells[i][j+1]>2):
                count+=1
                loop=True

			#      *----*---*
            #  	   |		|
            #  	   *----*	*
            
            #      *----*	*
            #  	   |		|
            #  	   *----*---*

            #      *----*---*
            #  	   |		
            #  	   *----*---*

            elif (cells[i][j+1]>1):
                incount(1,i,j+1,rows, cols, count, loop, h_, v_, cells)

    elif (k!=4 and h_[i+1][j]<1):
        if (i< rows-1):		

			#      *----*
			#  	   |    |
			#      * 	*
			#  	   |    |
			#  	   *----*
        
            if (cells[i+1][j] > 2):
                count+=1
                loop= True

            #      *----*
            #  	   |    |
            #      * 	*
            #  	        |
            #  	   *----*	

            #      *----*
            #  	   |    | 
            #      * 	*
            #  	   |    
            #  	   *----*	

            #      *----*
            #  	   |    | 
            #      * 	*
            #  	   |    |
            #  	   *	*	

            elif (cells[i+1][j] > 1):
                incount(2,i+1,j, rows, cols, count, loop, h_, v_, cells)

def outcount(k, i, j, count, h_, v_, rows, cols):
    if (count>0):
        if (k!=1 and v_[i][j]<1):
            if (count!=2): 
                # setvedge(i,j)
                action = action_id(rows, cols, CellOrientation.VERTICAL, i, j)
                # legal_actions_in_order.append(action)
                return action
            count-=1
            outcount(3,i,j-1, count, h_, v_, rows, cols)

        elif (k!=2 and h_[i][j]<1):
            if (count!=2): 
                # sethedge(i,j)
                action = action_id(rows, cols, CellOrientation.HORIZONTAL, i, j)
                # legal_actions_in_order.append(action)
                return action
            count-=1;
            outcount(4,i-1,j, count, h_, v_, rows, cols)

        elif (k!=3 and v_[i][j+1]<1):
            if (count!=2): 
                # setvedge(i,j+1)
                action = action_id(rows, cols, CellOrientation.VERTICAL, i, j+1)
                # legal_actions_in_order.append(action)
                return action
            count-=1;
            outcount(1,i,j+1, count, h_, v_, rows, cols)
            
        elif (k!=4 and h_[i+1][j]<1):
            if (count!=2):
                # sethedge(i+1,j)
                action = action_id(rows, cols, CellOrientation.HORIZONTAL, i+1, j)
                # legal_actions_in_order.append(action)
                return action
            count-=1;
            outcount(2,i+1,j, count, h_, v_, rows, cols)



def takeallbut(x, y, u, v, rows, cols, cells):
	while sides3not(x, y, u, v, rows, cols, cells):
		takebox(u,v)

def sides3not(x, y, u, v, rows, cols, cells):
    for i in range(0, rows):
        for j in range(0, cols):
            if (cells[i][j]==3):
                if (i!=x or j!=y):
                    u=i
                    v=j
                    return u, v
    return None

def setvedge(i,j):
    pass

def sethedge(i,j):
    pass



def singleton(rows, cols, cells, h_, v_) :     # Returns true and zz,x,y if edge(x,y) gives exactly 1 square away
    numb = None         
    for i in range(0,rows):
        for j in range(0,cols):
            if (cells[i][j]==2):
                numb=0
                if (h_[i][j]<1):
                    if (i<1 or cells[i-1][j]<2):
                        numb +=1
                zz=2
                if (v_[i][j]<1):
                    if (j<1 or cells[i][j-1]<2):
                        numb+=1
                    if (numb>1):
                        x=i
                        y=j
                        return CellOrientation.VERTICAL, x, y 
                if (v_[i][j+1]<1):
                    if (j+1==cols or cells[i][j+1]<2): 
                        numb+=1
                    if (numb>1):
                        x=i
                        y=j+1
                        return CellOrientation.VERTICAL, x, y
                zz=1
                if (h_[i+1][j]<1):
                    if (i+1==rows or cells[i+1][j]<2): 
                        numb+=1
                    if (numb>1):
                        x=i+1
                        y=j
                        return CellOrientation.HORIZONTAL, x, y
    return None

def doubleton(rows, cols, cells, v_, h_) :     #Returns true and zz,x,y if edge(x,y) gives away exactly 2 squares.
	zz=2               
	for i in range(0,rows):
		for j in range(0,cols-1):
			if (cells[i][j]==2 and cells[i][j+1]==2 and v_[i][j+1]<1):
				if (ldub(i,j) and rdub(i,j+1)):
					x=i
					y=j+1
					return CellOrientation.VERTICAL, x, y
	zz=1
	for j in range(0,cols):
		for i in range(0, rows-1):
			if (cells[i][j]==2 and cells[i+1][j]==2 and h_[i+1][j]<1):
				if (udub(i,j) and ddub(i+1,j)):
					x=i+1
					y=j
					return CellOrientation.HORIZONTAL, x, y
	return None


def ldub(i, j, rows, v_, h_, cells):
    """
    Given box(i,j)=2 and vedge(i,j+1)=0, returns true if the other free edge leads to a box<2
    """   
    if (v_[i][j]<1):      
        if (j<1 or cells[i][j-1]<2):
            return True
    elif (h_[i][j]<1):
        if (i<1 or cells[i-1][j]<2): 
            return True
    elif (i==rows-1 or cells[i+1][j]<2):
        return True
    return False

def rdub(i, j, rows, cols, v_, h_, cells):
    if (v_[i][j+1]<1):
        if (j+1==cols or cells[i][j+1]<2): 
            return True
    elif (h_[i][j]<1):
        if (i<1 or cells[i-1][j]<2): 
            return True
    elif (i+1==rows or cells[i+1][j]<2):
        return True
    return False
				
def udub(i, j, rows, cols, v_, h_, cells):
    if (h_[i][j]<1):
        if (i<1 or cells[i-1][j]<2):
            return True
    elif (v_[i][j]<1):
        if (j<1 or cells[i][j-1]<2): 
            return True
    elif (j==cols-1 or cells[i][j+1]<2):
        return True
    return False

def ddub(i, j, rows, cols, v_, h_, cells):
    if (h_[i+1][j]<1):
        if (i==rows-1 or cells[i+1][j]<2): 
            return True
    elif (v_[i][j]<1):
        if (j<1 or cells[i][j-1]<2): 
            return True
    elif (j==cols-1 or cells[i][j+1]<2):
        return True
    return False
