"""
Chains are sequences of one or more capturable boxes ("corridors").

2 kinds of chains exist:
    1. half-open chains: only one end of chain is capturable. (= corridor with 3 edges filled in)
    2. closed chains: both ends of chain are capturable.      (= corridor with 4 edges filled in)

Most moves on a state with chains are suboptimal, using this knowledge can reduce the branching 
factor of the game tree.

Half-open chains, only 2 moves are part of a optimal strategy:
    1.  Capture every available box in that chain and make an additional move.
    2.  Capture all but 2 boxes in that chain and fill in the end of the chain.
        This creates a hard-hearted handout.

Closed chains, only 2 moves is part of a optimal strategy:
    1.  Capture every available box in that chain and make an additional move.
    2.  Capture all but 4 boxes in that chain and fill in the edge that separates it in 
        2 hard-hearted handouts.

More than 1 chain available:
    1. Fill all but 1 available chains, and follow the above mentioned strategies for the remaining
        chain. If possible choose half-open chain as the last one. (Sacrifices only 2 instead of 4)
"""
import pyspiel
from absl import app


def _minimax(state, maximizing_player_id):
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

    player = state.current_player()
    if player == maximizing_player_id:
        selection = max
    else:
        selection = min
    values_children = [_minimax(state.child(action), maximizing_player_id) for action in state.legal_actions()]
    return selection(values_children)


def minimax_search(game,
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
    v = _minimax(
        state.clone(),
        maximizing_player_id=maximizing_player_id)
    return v


def main(_):
    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    game_string = "dots_and_boxes(num_rows=2,num_cols=2)"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)

    value = minimax_search(game)

    if value == 0:
        print("It's a draw")
    else:
        winning_player = 1 if value == 1 else 2
        print(f"Player {winning_player} wins.")


if __name__ == "__main__":
    app.run(main)
