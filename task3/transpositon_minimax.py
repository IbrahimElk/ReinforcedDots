import pyspiel
import hashlib
import numpy as np
from absl import app


def _minimax(state, maximizing_player_id, cache):
    """
    Implements a min-max algorithm

    Arguments:
      state: The current state node of the game.
      maximizing_player_id: The id of the MAX player. The other player is assumed
        to be MIN.

    Returns:
      The optimal value of the sub-game starting in state
    """

    if state.is_terminal():
        return state.player_return(maximizing_player_id)

    hashed_key = hash_state(state)
    if in_cache(hashed_key, cache):
        return cashed_value(hashed_key, cache)

    player = state.current_player()
    if player == maximizing_player_id:
        selection = max
    else:
        selection = min

    values_children = []
    for action in state.legal_actions():
        child_state = state.child(action)
        value = _minimax(child_state, maximizing_player_id, cache)
        values_children.append(value)
    
    minimax_value = selection(values_children)
    store_cache(hashed_key, minimax_value, cache)

    return minimax_value

def in_cache(hashed_state, cache):
    return hashed_state in cache

def hash_state(state):
    hash_hex = state.dbn_string()
    # params = state.get_game().get_parameters()
    # num_rows = params['num_rows']
    # num_cols = params['num_cols']
    # state_info = state.observation_tensor()
    # num_cells = ((1 + num_rows) * (1 + num_cols))
    
    # np_state_info = np.array(state_info)
    # state_matrix = np_state_info.reshape(3, num_cells, 3)
    # filtered_state_matrix = np.stack([state_matrix[:,:,0], state_matrix[:,:,1]], axis=-1)
    # filtered_state_matrix = filtered_state_matrix.astype(int)
    # merged_array = np.bitwise_or(filtered_state_matrix[1], filtered_state_matrix[2])

    # arr_bytes = merged_array.tobytes()
    # hash_object = hashlib.sha256(arr_bytes)
    # hash_hex = hash_object.hexdigest()
    return hash_hex

def cashed_value(hashed_key, cache):
    return cache[hashed_key]

def store_cache(hashed_state, minimaxvalue, cache):
    cache[hashed_state] = minimaxvalue

def minimax_search(game,
                   num_rows:int,
                   num_cols:int,
                   state=None,
                   maximizing_player_id=None,
                   state_to_key=lambda state: state):
    """Solves deterministic, 2-players, perfect-information 0-sum game.

    For small games only! Please use keyword arguments for optional arguments.

    Arguments:
      game: The game to analyze, as returned by `load_game`.
      state: The state to run from.  If none is specified, then the initial state is assumed.
      maximizing_player_id: The id of the MAX player. The other player is assumed
        to be MIN. The default (None) will suppose the player at the root to be
        the MAX player.

    Returns:
      The value of the game for the maximizing player when both player play optimally.
    """
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
    tranpostion_table = {}
    v = _minimax(
        state.clone(),
        maximizing_player_id=maximizing_player_id, 
        cache=tranpostion_table)
    return v


def main(_):
    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    num_rows = 7
    num_cols = 7
    game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)
    
    value = minimax_search(game, num_rows, num_cols)

    if value == 0:
        print("It's a draw")
    else:
        winning_player = 1 if value == 1 else 2
        print(f"Player {winning_player} wins.")
 

if __name__ == "__main__":
    app.run(main)

# DOC: 

# def in_cache(state, cache, num_rows, num_cols):
#     # hashed_state -> [lower_bound, upper_bound] #lowerbound of minimax value.
#     # state will be the configuration of the edges, but it should also be that 
#     # state who are symmetries of each other, to result in the same lower and 
#     # upperbound of the minimax value, as they encode the same state.
    
#     # Also, the underlying game object in open_spiel encodes the game via 3 vectors, 
#     # _v, _h and _p. See seperate PDF, We don't need _p as per the paper "Solving Dots-And-Boxes".

#     # Also, the vectors _v and _h contain entries of types '0', '1' or '2'. We will merge the 
#     # values '1' and '2' together to the value '1'. As any notion of players is not of importance.
#     # Once again, refer to the paper.
    
#     # we must make sure that symmestries of the state, result in the same hash, how do wo do this? 
    
    
#     hashed_state = hash_state(state, num_rows, num_cols)
#     return hashed_state in cache

# def hash_state(state, num_rows, num_cols):
#     # state.observation_tensor() returns a 3-d tensor.
#     # see respective dots_and_boxes.cc file
#     # 
#     #   TensorView<3> view(values,
#     #                      {/*cellstates=*/3, num_cells_,
#     #                       /*part of cell (h, v, p)=*/3},
#     #                      true);

#     # cellstate = empty , player1 , player2 
#     # num_cells = aantal (x,y) punten in dots and boxes waaruit edjes vertrekt. 
#     #           | zie aparte pdf file in doc folder.
#     # part of cell = defines if the edge is horizontal, vertical or p 
#     #              | p => player points, defines if it results in player i's point towards a box.)
    
#     # we zijn ekel geinteresseerd in player1 + player2 dimensies, waarvan alle num_cells en waarvan 
#     # enkel horizontal of vertical van belang is. 

#     state_info = state.observation_tensor()
#     num_cells = ((1 + num_rows) * (1 + num_cols))
#     # print(len(state_info), 3*num_cells*3)
    
#     # info: 
#     # empty player = indices van 0 -> 3 * num_cells
#     # first player = indices van 3 * num_cells -> 2 * 3 * num_cells
#     # thrid player = indices van 2 * 3 * num_cells -> 3 * 3 * num_cells

#     # we hebben niet elke 3 * num_cells nodig. 
#     # enkel 2 * num_cells
    
#     np_state_info = np.array(state_info)
#     state_matrix = np_state_info.reshape(3, num_cells, 3)

#     # (3, 9, 3)
#     # [[[1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]
#     #   [1. 1. 1.]]

#     #  [[0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]]

#     #  [[0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]
#     #   [0. 0. 0.]]]

#     # [ 1  1  1] => [horinzontal vertical dezeplayerheeftdezeboxofniet]
#     # derde index niet nodig. 
#     # [[1 1 1] ... ] => 16 cells of 9 cells voor aantal xy punten in x keer y dots and boxes game.
#     # [[ [1 1 1] ... ] ... ] => voor elk player, waarbij de eerste de null player is. 

#     # print(state_matrix.shape)
#     # print(state_matrix)

#     filtered_state_matrix = np.stack([state_matrix[:,:,0], state_matrix[:,:,1]], axis=-1)

#     # print(filtered_state_matrix.shape)
#     # print(filtered_state_matrix)

#     arr_bytes = filtered_state_matrix.tobytes()
#     hash_object = hashlib.sha256(arr_bytes)
#     hash_hex = hash_object.hexdigest()
#     return hash_hex


# # Original array
    # original_array = np.array([
    #                         [[1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1],
    #                             [1, 1]],
                            
    #                         [[0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0]],
                            
    #                         [[0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0],
    #                             [0, 0]]])

    # # Merge the last two lists of the first dimension using binary OR operation
    # merged_array = np.bitwise_or(original_array[1], original_array[2])

    # print(merged_array)
