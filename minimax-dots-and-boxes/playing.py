import os 
import sys
import numpy as np

package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_directory)

from open_spiel.python.bots import human
from open_spiel.python.bots import uniform_random

from dotsandboxes_agent_ec.dotsandboxes_agent import get_agent_for_tournament
from dotsandboxes_agent_emd.dotsandboxes_agent import get_agent_for_tournament

# from baselines.firstopen import get_agent_for_tournament
# from baselines.random import get_agent_for_tournament

import pyspiel

seed  = 12761381  # The seed to use for the RNG

def LoadAgent(agent_type, player_id, rng):
  """Return a bot based on the agent type."""
  if agent_type == "random":
    return uniform_random.UniformRandomBot(player_id, rng)
  elif agent_type == "human":
    return human.HumanBot()
  elif agent_type == "minimax":
     return get_agent_for_tournament(player_id)
  else:
    raise RuntimeError("Unrecognized agent type: {}".format(agent_type))

def training(player0:str, player1:str):
    rng = np.random.RandomState(seed)
    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    num_rows = 5
    num_cols = 5
    game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)

    agents = [
        LoadAgent(player0, 0, rng),
        LoadAgent(player1, 1, rng),
    ]

    state = game.new_initial_state()

    while not state.is_terminal():
        current_player = state.current_player()
        action = agents[current_player].step(state)
        agents[1-current_player].inform_action(state, current_player, action)
        action_string = state.action_to_string(current_player, action)
        print("Player ", current_player, ", chose action: ", action_string)
        state.apply_action(action)

    # Game is now done. Print utilities for each player
    returns = state.returns()
    for pid in range(game.num_players()):
        print("Utility for player {} is {}".format(pid, returns[pid]))


if __name__ == "__main__":
    p1 = "random"
    p2 = "minimax"
    # p3 = "minimax2"
    #  p = "random"
    training(p2,p1)

    # if current_player == 1 dan das P2 oftewel p1 = minimax. 
    # if current_player == 0 dan das P1 oftewel
    print("player0 corresponds to the first player that makes a move on the board.")
    print(f"player0 is {p1} and player1 is {p2}")

    print("P2 on the board corresponds to player1")
    print("P1 on the board corresponds to player0")



