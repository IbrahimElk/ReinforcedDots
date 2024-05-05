import os
import sys
import pyspiel
import numpy as np
package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_directory)

from flag import Flag
from transposition_table import TTable
from cell_orientation import CellOrientation
from intelligent_chains import safe3s, sides3, sides3not, incount, outcount, sides01, takebox, sac, singleton, doubleton

# FIXME: draw game tree to see if it makes sense. 
# TODO: output of evaluation function, should it consider the output space of the terminal states? 

# TODO: tis niet in principe nodig om value en action terug te returnen, enkel in minimax.
# we kunnen ook gwn de action terug geven, en dan bij "make any move", dan is eerste moment dat je minimax doet.

def action_id(num_rows_:int, num_cols_:int, orientation_:CellOrientation, row_:int, col_:int):
  action = 0
  maxh  = (num_rows_ + 1) * num_cols_
  if (orientation_ == CellOrientation.HORIZONTAL):
    action = row_ * num_cols_ + col_
  else :
    action = maxh + row_ * (num_cols_ + 1) + col_
  return action

def eval_function(state, maximizing_player_id): 
    params = state.get_game().get_parameters()
    num_rows = params['num_rows']
    num_cols = params['num_cols']
    num_dots = ((1 + num_rows) * (1 + num_cols))
    
    state_info = state.observation_tensor()    
    np_state_info = np.array(state_info)
    
    # {cellstates= (empty, player1, player2), num_cells , part_of_cell(horizontal, vertical, which_player_won) = 3},
    state_matrix = np_state_info.reshape(3, num_dots, 3)
   
    player = state.current_player()
    points_empty = sum(state_matrix[0,:,2])
    points_player = sum(state_matrix[player+1,:,2])

    # normalize the points to [-1 , 1] region?  
    total_amnt_boxes = num_rows * num_cols

    if player == maximizing_player_id:
        return points_player/total_amnt_boxes
    else :
        return (total_amnt_boxes - (points_empty + points_player))/total_amnt_boxes

def get_dbn_action(state, flag:Flag, depth, alpha, beta, value_function,
                maximizing_player_id, cache:TTable):

    if state.is_terminal():
        return state.player_return(maximizing_player_id), None
    
    # FIXME: zie MCTS, eval functie verandert, de huidige eval functie is a bad one. 
    # en mag niet gebruikt worden opt einde. 
    if depth == 0:
        return value_function(state, maximizing_player_id), None

    # FIXME: moet de val aangepast worden voor max of min speler, ik denk het niet
    # zie ook paper: "Solving Dots-And-Boxes" , maar niet zeker. 
    data = cache.get(state)
    if data != None:
        val , action = data 
        return val, action

    rows    = None
    cols    = None
    cells   = None
    v_      = None
    h_      = None
    points  = None

    # 1. is there a safe box ?
    next_action = safe3s(rows, cols, cells, v_, h_) 
    if next_action : 
        # first run actions that capture boxes. (safe boxes)
        # which of those possible actions is more preferrable ?
        
        # FIXME: hoe value geven aan deze actie? minimax of eval functie, kpeis gwn eval fucntie? of gwn +oo, idk ? 
        # child_value, action = take_action(state, depth, alpha, beta, value_function, maximizing_player_id, cache, action)
        child_state = state.clone()
        child_state.apply_action(action)
        child_value = value_function(child_state)

        return child_value, action
    
    if flag.getChainFill():
        # sides3(): check if you can still capture boxes. (unsafe boxes)
        d = sides3()
        if sides3():
            u, v = d
            actionid = takebox(u,v, h_, v_, rows, cols)

            # FIXME:  analoog als hierboven, hoe value berekene? 
            child_state = state.clone()
            child_state.apply_action(action)
            child_value = value_function(child_state)

            return child_value, actionid
       
        else : 
            # sides01(): returns a safe *random* edge that you can capture. 
            orien, x, y = sides01()

            # FIXME: hier ipv value_function gebruiken, gebruik ik minimax om value te vinden
            value, best_action = take_action(state, depth, alpha, beta, value_function,
                maximizing_player_id, cache, orien, x, y)
            
            flag.setChainFill(False)

            return value, best_action

    # FIXME: tis geen elifs..., maja werkt als elifs wegens return statements. 
    if flag.getHalfhaerted(): 
        if flag.getHalfOpen():
            d = sides3not(x, y, u, v, rows, cols, cells)
            if d:
                u, v = d
                action = takebox(u, v, h_, v_, rows, cols)

                # FIXME:  analoog als hierboven, hoe value berekene? 
                child_state = state.clone()
                child_state.apply_action(action)
                child_value = value_function(child_state)

                return child_value, actionid
            else: 
                flag.setHalfOpen(False)
        # als half open false is, 
        # dus oftewel , al meerdere keren gedaan dat of helemaal niet uitgevoed, boeit niet
        # in elk geval, deze if statement moet uitgevoerd worden.   
        if flag.getEnd():            
            d = sides3(rows, cols, cells)
            if d:
                u,v = d
                action = takebox(u, v, h_, v_, rows, cols)

                # FIXME:  analoog als hierboven, hoe value berekene? 
                child_state = state.clone()
                child_state.apply_action(action)
                child_value = value_function(child_state)

                return child_value, actionid
            else :
                flag.setEnd(False)
        
        if flag.getOut(): 
            count = flag.getCount()
            i,j = flag.getCell()
            outcount(0, i, j, count, h_, v_, rows, cols)

            action = outcount(0, i, j, count, h_, v_, rows, cols)
            flag.setCount(count)

            # FIXME:  analoog als hierboven, hoe value berekene? 
            child_state = state.clone()
            child_state.apply_action(action)
            child_value = value_function(child_state)

            return child_value, actionid

    # --------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------
    
    unsafe_box = sides3()
    safe_edge = sides01()
    single = singleton()
    double = doubleton()

    if unsafe_box:
        if safe_edge:
            flag.setChainFill(True)
            u, v = unsafe_box
            actionid = takebox(u,v, h_, v_, rows, cols)

            # FIXME:  analoog als hierboven, hoe value berekene? 
            child_state = state.clone()
            child_state.apply_action(action)
            child_value = value_function(child_state)

            return child_value, actionid

        else:
            flag.setHalfhaerted(True)
            u, v = unsafe_box

            count=0
            loop=False
            # count aantal boxes vanaf box(i,j)
            incount(0, u, v, rows, cols, count, loop, h_, v_, cells)

            flag.setCount(count)
            # if chain is half open, use half haerted technique
            if not loop:
                flag.setHalfOpen(True)

                d = sides3not(x, y, u, v, rows, cols, cells)
                if d:
                    u, v = d
                    action = takebox(u, v, h_, v_, rows, cols)

                    # FIXME:  analoog als hierboven, hoe value berekene? 
                    child_state = state.clone()
                    child_state.apply_action(action)
                    child_value = value_function(child_state)

                    return child_value, actionid
                
            # if last step, pak dan alle boxes. 
            if (count + points[0] + points[1] == rows*cols):
                flag.setEnd(True)
                
                d = sides3(rows, cols, cells)
                while d:
                    u,v = d
                    action = takebox(u, v, h_, v_)

                    # FIXME:  analoog als hierboven, hoe value berekene? 
                    child_state = state.clone()
                    child_state.apply_action(action)
                    child_value = value_function(child_state)

                    return child_value, actionid
                
            else:
                # if chain closed: 
                flag.setOut(True)

                if (loop):
                    count=count-2
                
                flag.setCell(u,v)
                # check of dat het u en v is die ik moe meegeven. 
                action = outcount(0, u, v, count, h_, v_, rows, cols)
                flag.setCount(count)

                # FIXME:  analoog als hierboven, hoe value berekene? 
                child_state = state.clone()
                child_state.apply_action(action)
                child_value = value_function(child_state)

                return child_value, actionid
    
    elif safe_edge: 
        orien, x, y = safe_edge
                        
        action = action_id(rows,cols,CellOrientation.HORIZONTAL,x,y)
    
        # FIXME:  analoog als hierboven, hoe value berekene? 
        child_state = state.clone()
        child_state.apply_action(action)
        child_value = value_function(child_state)

        return child_value, actionid
    
    elif single:
        orien, x, y = single
        action = action_id(rows,cols,CellOrientation.HORIZONTAL,x,y)
    
        # FIXME:  analoog als hierboven, hoe value berekene? 
        child_state = state.clone()
        child_state.apply_action(action)
        child_value = value_function(child_state)

        return child_value, actionid

    elif double:
        orien, x, y = double
        action = action_id(rows,cols,CellOrientation.HORIZONTAL,x,y)
    
        # FIXME:  analoog als hierboven, hoe value berekene? 
        child_state = state.clone()
        child_state.apply_action(action)
        child_value = value_function(child_state)

        return child_value, actionid
    else: 
        # make any move. 
        val, action = _alpha_beta(state, depth, alpha, beta, value_function)
        return val, action

def _alpha_beta(state, depth, alpha, beta, value_function,
                maximizing_player_id, cache:TTable, possible_actions):
    
    player = state.current_player()
    best_action = -1
    if player == maximizing_player_id:
        value = -float("inf")
        for action in possible_actions:
            child_state = state.clone()
            child_state.apply_action(action)

            child_value, _  = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id, cache)
            if child_value > value:
                value = child_value
                best_action = action
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut-off
        
        # transpostion table
        cache.set(state, value, best_action)
        return value, best_action
    
    else:
        value = float("inf")
        for action in possible_actions:
            child_state = state.clone()
            child_state.apply_action(action)
            child_value, _  = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id, cache)
            if child_value < value:
                value = child_value
                best_action = action
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cut-off
        
        # transpostion table
        cache.set(state, value, best_action)
        return value, best_action

def minimax_alphabeta_search(game,
                            flag:Flag,
                            transposition_table:TTable,
                            state=None,
                            value_function=None,
                            maximum_depth=10,
                            maximizing_player_id=None):
    #TODO: value_function wordt gehardcoded hier naar de chain evaluation function.
    """ functie met alles der op en der aan (van optimisaties) """

    game_info = game.get_type()

    if game.num_players() != 2:
        raise ValueError("Game must be a 2-player game")
    if game_info.chance_mode != pyspiel.GameType.ChanceMode.DETERMINISTIC:
        raise ValueError("The game must be a Deterministic one, not {}".format(
        game.chance_mode))
    if game_info.information != pyspiel.GameType.Information.PERFECT_INFORMATION:
        raise ValueError(
        "The game must be a perfect information one, not {}".format(
            game.information))
    if game_info.dynamics != pyspiel.GameType.Dynamics.SEQUENTIAL:
        raise ValueError("The game must be turn-based, not {}".format(
        game.dynamics))
    if game_info.utility != pyspiel.GameType.Utility.ZERO_SUM:
        raise ValueError("The game must be 0-sum, not {}".format(game.utility))

    if state is None:
        state = game.new_initial_state()
    if maximizing_player_id is None:
        maximizing_player_id = state.current_player()
    
    # FIXME: no need for initial matrix to be stored in transposition table ?

    return prior_actions(
        state.clone(),
        flag,
        maximum_depth,
        alpha=-float("inf"),
        beta=float("inf"),
        value_function=eval_function,
        maximizing_player_id=maximizing_player_id,
        cache=transposition_table)

def main():
    flag    = Flag()
    tt      = TTable()
    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    num_rows = 1
    num_cols = 1
    game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)
    
    value, _ = minimax_alphabeta_search(game,flag,tt)
    if value == 0:
        print("It's a draw")
    else:
        winning_player = 1 if value == 1 else 2
        print(f"Player {winning_player} wins.")
 

if __name__ == "__main__":
    main()
