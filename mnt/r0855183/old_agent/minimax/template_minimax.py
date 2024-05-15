import os
import sys
import pyspiel
from absl import app

package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_directory)

from dotsandboxes_agent.transposition_table import Transposition_Table, TNaive_Table

def _minimax(state, maximizing_player_id, cache:Transposition_Table):
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

    val = cache.get(state)
    if val != None:
        return val

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
    cache.set(state, minimax_value)

    return minimax_value


def minimax_naive_search(game,
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

    tt = TNaive_Table()
    v = _minimax(
        state.clone(),
        maximizing_player_id=maximizing_player_id,
        cache=tt)
    return tt, v


def main(_):
    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    game_string = "dots_and_boxes(num_rows=7,num_cols=7)"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)

    value = minimax_naive_search(game)

    if value == 0:
        print("It's a draw")
    else:
        winning_player = 1 if value == 1 else 2
        print(f"Player {winning_player} wins.")


if __name__ == "__main__":
    app.run(main)
