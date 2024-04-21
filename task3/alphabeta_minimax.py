import pyspiel
from transposition_table import TTable
from minimax.chains_minimax import chain_heuristic

# TODO: output of evaluation function should it consider the output space of the terminal states? 
# I don't think so.

def _alpha_beta(state, depth, alpha, beta, value_function,
                maximizing_player_id, cache:TTable):

    if state.is_terminal():
        return state.player_return(maximizing_player_id), None

    if depth == 0:
        return value_function(state), None

    # transpostion table
    val = cache.get(state)
    if val != None:
        return val

    player = state.current_player()
    best_action = -1
    if player == maximizing_player_id:
        value = -float("inf")
        for action in state.legal_actions():
            child_state = state.clone()
            child_state.apply_action(action)
            child_value, _ = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id)
            if child_value > value:
                value = child_value
                best_action = action
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut-off
        
        # transpostion table
        cache.set(state, value)

        return value, best_action
    else:
        value = float("inf")
        for action in state.legal_actions():
            child_state = state.clone()
            child_state.apply_action(action)
            child_value, _ = _alpha_beta(child_state, depth - 1, alpha, beta,
                                        value_function, maximizing_player_id)
            if child_value < value:
                value = child_value
                best_action = action
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cut-off
        
        # transpostion table
        cache.set(state, value)

        return value, best_action

def minimax_alphabeta_search(game,
                        state=None,
                        value_function=None,
                        maximum_depth=30,
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
    transposition_table = TTable()

    return _alpha_beta(
        state.clone(),
        maximum_depth,
        alpha=-float("inf"),
        beta=float("inf"),
        value_function=chain_heuristic,
        maximizing_player_id=maximizing_player_id,
        cache=transposition_table)