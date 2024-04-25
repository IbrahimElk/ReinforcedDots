import pyspiel
import os
import sys

package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_directory)

from transpositon_minimax import _minimax
from dotsandboxes_agent.transposition_table import TSymmetric_Table

# the implementation of this function will go to transposition_table.py
# inside the hashstate function. 

def minimax_symmetry_search(game,
                   state=None,
                   maximizing_player_id=None):
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
    transposition_table = TSymmetric_Table()
    
    v = _minimax(
        state.clone(),
        maximizing_player_id=maximizing_player_id, 
        cache=transposition_table)
    return transposition_table, v