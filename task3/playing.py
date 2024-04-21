from absl import app
from absl import flags
import numpy as np

from minimax.transpositon_minimax import minimax_transposition_search, Transposition_Table
from minimax.symmetry_minimax import minimax_symmetry_search
from minimax.chains_minimax import minimax_chains_search
from minimax.template_minimax import minimax_naive_search
from alphabeta_minimax import minimax_alphabeta_search

from open_spiel.python.bots import human
from open_spiel.python.bots import uniform_random
import pyspiel

seed  = 12761381  # The seed to use for the RNG

def LoadAgent(agent_type, player_id, rng):
  """Return a bot based on the agent type."""
  if agent_type == "random":
    return uniform_random.UniformRandomBot(player_id, rng)
  elif agent_type == "human":
    return human.HumanBot()
  else:
    raise RuntimeError("Unrecognized agent type: {}".format(agent_type))

def training(player0:str, player1:str):
    rng = np.random.RandomState(seed)
    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    num_rows = 2
    num_cols = 2
    game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)

    agents = [
        LoadAgent(player0, 0, rng),
        LoadAgent(player1, 1, rng),
    ]

    state = game.new_initial_state()

    # Print the initial state
    print("INITIAL STATE")
    print(str(state))

    while not state.is_terminal():
        current_player = state.current_player()
        # Decision node: sample action for the single current player
        legal_actions = state.legal_actions()
        for action in legal_actions:
            print(
                "Legal action: {} ({})".format(
                    state.action_to_string(current_player, action), action
                )
            )
        # if human, asks in terminal which move and returns the action. 
        # if random, based on state, gives random action
        action = agents[current_player].step(state)
        action_string = state.action_to_string(current_player, action)
        print("Player ", current_player, ", chose action: ", action_string)
        state.apply_action(action)

        print("")
        print("NEXT STATE:")
        print(str(state))
        if not state.is_terminal():
            print(str(state.observation_tensor()))

    # Game is now done. Print utilities for each player
    returns = state.returns()
    for pid in range(game.num_players()):
        print("Utility for player {} is {}".format(pid, returns[pid]))



if __name__ == "__main__":
   p1 = "human"
   p2 = "random"
   training(p1,p2)




