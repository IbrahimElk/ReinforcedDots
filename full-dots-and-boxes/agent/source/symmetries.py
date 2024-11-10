"""
There are a number of trivial symmetries in Dots-And-Boxes
that reduce the problem space. The mirror image of a state is
also a legal game whose optimal strategy mirrors that of the
current state. All Dots-And-Boxes instances have horizon-
tal and vertical symmetry, and square boards have diagonal
symmetry.

Author : John Gao
April - 2024
"""
import numpy as np
import util as s

from deprecated import deprecated

# FIXME:(Ibrahim) there is a more performant way of implementing
# this symmetry algorithms. This is by directly working with the
# dots-and-boxes (DBN) notation which is a binary string and doing
# some bit manipulation.


def check_horizontal(state, num_rows:int, num_cols:int):
    """
    Checks the horizontal mirror symmetry of a Dots-and-Boxes game state.
    Args:
        state (pyspiel.State): The current game state.
        num_rows (int): The number of rows in the board.
        num_cols (int): The number of columns in the board.

    Returns:
        str: The new game state represented as a DBN string after the horizontal flip.
    """
    dbn = state.dbn_string()
    h_matrix, v_matrix = s.dbn_to_vectors(num_rows, num_cols, dbn)

    new_h_list = np.flipud(h_matrix)
    new_v_list = np.flipud(v_matrix)

    return s.vectors_to_dbn(num_rows, num_cols, new_h_list, new_v_list)

def check_vertical(state, num_rows, num_cols):
    """
    Checks the vertical mirror symmetry of a Dots-and-Boxes game state.

    Args:
        state (State): The current game state.
        num_rows (int): The number of rows in the board.
        num_cols (int): The number of columns in the board.

    Returns:
        str: The new game state represented as a DBN string after the vertical flip.
    """
    dbn = state.dbn_string()
    h_matrix, v_matrix = s.dbn_to_vectors(num_rows, num_cols, dbn)

    new_h_list = np.fliplr(h_matrix)
    new_v_list = np.fliplr(v_matrix)

    return s.vectors_to_dbn(num_rows, num_cols,new_h_list, new_v_list)

def check_hv(state, num_rows, num_cols):
    """
    Checks a combined horizontal and vertical mirror symmetry of a Dots-and-Boxes game state.
    (which is more performant than composing the check_vertical and check_horizontal)

    Args:
        state (State): The current game state.
        num_rows (int): The number of rows in the board.
        num_cols (int): The number of columns in the board.

    Returns:
        str: The new game state represented as a DBN string after the horizontal and vertical flips.
    """
    dbn = state.dbn_string()
    h_matrix, v_matrix = s.dbn_to_vectors(num_rows, num_cols, dbn)

    h_matrix = np.flipud(h_matrix)
    v_matrix = np.flipud(v_matrix)

    new_h_list = np.fliplr(h_matrix)
    new_v_list = np.fliplr(v_matrix)

    return s.vectors_to_dbn(num_rows, num_cols,new_h_list, new_v_list)

def check_vh(state, num_rows, num_cols):
    """
    Checks a combined vertical and horizontal mirror symmetry of a Dots-and-Boxes game state.
    (which is more performant than composing the check_vertical and check_horizontal)
    
    Args:
        state (State): The current game state.
        num_rows (int): The number of rows in the board.
        num_cols (int): The number of columns in the board.

    Returns:
        str: The new game state represented as a DBN string after the vertical and horizontal flips.
    """
    dbn = state.dbn_string()
    h_matrix, v_matrix = s.dbn_to_vectors(num_rows, num_cols, dbn)

    new_h_list = np.fliplr(h_matrix)
    new_v_list = np.fliplr(v_matrix)

    h_matrix = np.flipud(new_h_list)
    v_matrix = np.flipud(new_v_list)

    return s.vectors_to_dbn(num_rows, num_cols, h_matrix, v_matrix)

# only for square boards
def check_diag1(state, num_rows, num_cols):
    """
    Checks the diagonal symmetry (270 degrees rotation) of a Dots-and-Boxes game state.
    This symmetry is only applicable to square boards.

    Args:
        state (State): The current game state.
        num_rows (int): The number of rows in the board.
        num_cols (int): The number of columns in the board.

    Returns:
        str: The new game state represented as a DBN string after the 270-degree counterclockwise rotation.
    """
    dbn = state.dbn_string()
    h_matrix, v_matrix = s.dbn_to_vectors(num_rows, num_cols, dbn)
    
    new_h_list = np.rot90(v_matrix, 3)
    new_v_list = np.rot90(h_matrix, 3)
    
    return s.vectors_to_dbn(num_rows, num_cols, new_h_list, new_v_list)

def check_diag2(state, num_rows, num_cols):
    """
    Checks the diagonal symmetry (90 degrees rotation) of a Dots-and-Boxes game state.
    This symmetry is only applicable to square boards.

    Args:
        state (State): The current game state.
        num_rows (int): The number of rows in the board.
        num_cols (int): The number of columns in the board.

    Returns:
        str: The new game state represented as a DBN string after the 90-degree counterclockwise rotation.
    """    
    dbn = state.dbn_string()
    h_matrix, v_matrix = s.dbn_to_vectors(num_rows, num_cols, dbn)

    new_h_list = np.rot90(v_matrix, 1)
    new_v_list = np.rot90(h_matrix, 1)
    
    return s.vectors_to_dbn(num_rows, num_cols, new_h_list, new_v_list)

def check_h_diag1(state, num_rows, num_cols):
    """
    Checks the combination of horizontal flip and 270-degree diagonal rotation symmetry of a 
    Dots-and-Boxes game state. This symmetry is only applicable to square boards.

    Args:
        state (State): The current game state.
        num_rows (int): The number of rows in the board.
        num_cols (int): The number of columns in the board.

    Returns:
        str: The new game state represented as a DBN string after applying the transformations.
    """
    dbn = state.dbn_string()
    h_matrix, v_matrix = s.dbn_to_vectors(num_rows, num_cols, dbn)

    new_h_list = np.flipud(h_matrix)
    new_v_list = np.flipud(v_matrix)

    h_list = np.rot90(new_v_list, 3)
    v_list = np.rot90(new_h_list, 3)
    
    return s.vectors_to_dbn(num_rows, num_cols, h_list, v_list)

@deprecated
def _find_all_symmetries(state, num_rows, num_cols):
    s1 = check_horizontal(state, num_rows, num_cols)
    s2 = check_vertical(state, num_rows, num_cols)
    s3 = check_hv(state, num_rows, num_cols)
    s4 = check_vh(state, num_rows, num_cols)
    if num_rows == num_cols :
        s5 = check_diag1(state, num_rows, num_cols)
        s6 = check_diag2(state, num_rows, num_cols)
        s7 = check_diag2(state, num_rows, num_cols)
        return [s1, s2, s3, s4, s5 , s6, s7]
    else :
        return [s1, s2, s3, s4]
