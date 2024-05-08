#  
#      *----*
#  	        |
#      *----*
def single_singleton(SA):
    SA.cells[0][0] = 3
    SA.cells[1][0] = 1
    SA.cells[0][1] = 1

    SA.h_[0][0] = 1
    SA.h_[1][0] = 1
    SA.v_[0][1] = 1

#  
#      *----*----*
#  	   |         |  
#      *----*----*
def single_doubleton(SA):
    SA.cells[0][0] = 3
    SA.cells[0][1] = 3
    SA.cells[1][0] = 1
    SA.cells[1][1] = 1
    SA.cells[0][2] = 1

    SA.h_[0][0] = 1
    SA.h_[0][1] = 1
    SA.h_[1][0] = 1
    SA.h_[1][1] = 1

    SA.v_[0][0] = 1
    SA.v_[0][2] = 1

#  
#      *----*
#  	   |    |
#      * 	*
#  	   |    |
#  	   *    *
def vertical_half_open_chain(SA):
    # ------------- 
    SA.h_[0][0] = 1

    SA.v_[0][0] = 1
    SA.v_[0][1] = 1
    SA.v_[1][0] = 1
    SA.v_[1][1] = 1

    SA.cells[0][0] = 3
    SA.cells[0][1] = 1
    SA.cells[1][0] = 2
    SA.cells[1][1] = 1

#      *----*---*
#  	   |		|
#  	   *----*   *
def horizontal_half_open_chain2(SA):
    # ------------- 
    SA.h_[0][0] = 1
    SA.h_[0][1] = 1
    SA.h_[1][0] = 1

    SA.v_[0][0] = 1
    SA.v_[0][2] = 1

    SA.cells[0][0] = 3
    SA.cells[0][1] = 2
    SA.cells[0][2] = 1
    SA.cells[1][0] = 1

#      *----*---*
#  	   |		
#  	   *----*---*
def horizontal_half_open_chain1(SA):
    # ------------- 
    SA.h_[0][0] = 1
    SA.h_[0][1] = 1
    SA.h_[1][0] = 1
    SA.h_[1][1] = 1

    SA.v_[0][0] = 1

    SA.cells[0][0] = 3
    SA.cells[0][1] = 2
    SA.cells[1][0] = 1
    SA.cells[1][1] = 1

#      *----*---*---*---*
#  	   |		        |
#  	   *----*---*---*---*
def horizontal_closed_chain(SA):
    # --------------
    SA.h_[0][0] = 1
    SA.h_[0][1] = 1
    SA.h_[0][2] = 1
    SA.h_[0][3] = 1
    SA.h_[0][4] = 1

    # --------------
    SA.h_[1][0] = 1
    SA.h_[1][1] = 1
    SA.h_[1][2] = 1
    SA.h_[1][3] = 1
    SA.h_[1][4] = 1

    # --------------
    SA.v_[0][0] = 1
    SA.v_[0][4] = 1

    # --------------
    SA.cells[0][0] = 3
    SA.cells[0][1] = 2
    SA.cells[0][2] = 2
    SA.cells[0][3] = 3
    SA.cells[0][4] = 1

    SA.cells[1][0] = 1
    SA.cells[1][1] = 1
    SA.cells[1][2] = 1
    SA.cells[1][3] = 1


# hetvolgende maar transposed:
#      *----*---*---*---*
#  	   |		        |
#  	   *----*---*---*---*
def vertical_closed_chain(SA):
    # --------------
    SA.v_[0][0] = 1
    SA.v_[1][0] = 1
    SA.v_[2][0] = 1
    SA.v_[3][0] = 1

    # --------------
    SA.v_[0][1] = 1
    SA.v_[1][1] = 1
    SA.v_[2][1] = 1
    SA.v_[3][1] = 1

    # --------------
    SA.h_[0][0] = 1
    SA.h_[4][0] = 1

    # --------------
    SA.cells[0][0] = 3
    SA.cells[1][0] = 2
    SA.cells[2][0] = 2
    SA.cells[3][0] = 3
    SA.cells[4][0] = 1

    SA.cells[0][1] = 1
    SA.cells[1][1] = 1
    SA.cells[2][1] = 1
    SA.cells[3][1] = 1

# Solving Dots-And-Boxes
# Joseph K. Barker and Richard E Korf
# Figure 2: Examples of chains
def example_paper(SA):
    # --------------
    SA.h_[0][2] = 1
    SA.h_[0][3] = 1
    SA.h_[0][4] = 1
    SA.h_[0][5] = 1

    SA.h_[1][2] = 1
    SA.h_[1][3] = 1
    SA.h_[1][4] = 1

    SA.h_[3][5] = 1

    # --------------
    SA.v_[0][2] = 1
    SA.v_[1][5] = 1
    SA.v_[2][5] = 1

    SA.v_[0][6] = 1
    SA.v_[1][6] = 1
    SA.v_[2][6] = 1

    # --------------
    SA.h_[0][0] = 1

    SA.h_[2][1] = 1
    SA.h_[2][2] = 1
    SA.h_[2][3] = 1
    

    SA.h_[3][0] = 1
    SA.h_[3][1] = 1
    SA.h_[3][2] = 1
    SA.h_[3][3] = 1
    
    # --------------
    SA.v_[0][0] = 1
    SA.v_[1][0] = 1
    SA.v_[2][0] = 1
    
    SA.v_[0][1] = 1
    SA.v_[1][1] = 1

    # --------------

    SA.cells[0][0] = 3
    SA.cells[0][1] = 2
    SA.cells[0][2] = 3
    SA.cells[0][3] = 2
    SA.cells[0][4] = 2
    SA.cells[0][5] = 2
    
    SA.cells[1][0] = 2
    SA.cells[1][1] = 2
    SA.cells[1][2] = 2
    SA.cells[1][3] = 2
    SA.cells[1][4] = 2
    SA.cells[1][5] = 2

    SA.cells[2][0] = 2
    SA.cells[2][1] = 2
    SA.cells[2][2] = 2
    SA.cells[2][3] = 2
    SA.cells[2][4] = 1
    SA.cells[2][5] = 3
