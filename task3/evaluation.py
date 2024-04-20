# from absl import app
# from absl import flags
# import numpy as np
import time 
import os 
import json 

from transpositon_minimax import minimax_transposition_search, Transposition_Table
from symmetry_minimax import minimax_symmetry_search
from chains_minimax import minimax_chains_search
from template_minimax import minimax_naive_search
from mixed_minimax import minimax_mixed_search

# from open_spiel.python.bots import human
# from open_spiel.python.bots import uniform_random
import pyspiel

import platform
import psutil

# -----------------------------------------------------------------------------
# GOAL:
# Use these the three optimizations (transposition table, symmetry and chains)
# and compare with the provided template algorithm. For various game board
# sizes, plot both the execution times and the number of keys.
# -----------------------------------------------------------------------------

# function signature for the minimax argument, should be the same for all!
# def minimax_transposition_search(game,
#                    state=None,
#                    maximizing_player_id=None) -> tuple(int, Transposition_Table)
def scrape_minimax(minimax, game, state):
    print(f"Utilising {minimax.__name__} algorithm")

    t0 = time.time()
    tt, mmvalue = minimax(game, state) # de state wordt niet verandert door minimax, door state.clone(),
    t1 = time.time()

    cache = tt.get_cache()
    nb_keys = len(cache.keys())
    nb_hits = tt.get_hits()
    nb_misses = tt.get_misses()

    results = {
        "time" :            t1-t0,
        "minimax_value" :   mmvalue, # for maximizing player, player 0. 
        "nb_keys":          nb_keys,
        "nb_hits":          nb_hits,
        "nb_misses":        nb_misses,
    }
    return results

def record_results(game, dict_results:dict):
    optims = [minimax_transposition_search, 
            #   minimax_symmetry_search, 
            #   minimax_chains_search, 
              minimax_naive_search, 
            #   minimax_mixed_search
              ]
    
    for optim in optims:
        state = game.new_initial_state()
        dict_results[optim.__name__] = scrape_minimax(optim, game, state)

def initialise_report():
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()

    hardware_info = {
        "system_information" : {
            "System" :      uname.system,
            "Node Name":    uname.node,
            "Release":      uname.release,
            "Version":      uname.version,
            "Machine":      uname.machine,
            "Processor":    uname.processor
        },
        "CPU_info" : {
            "Physical cores" :  psutil.cpu_count(logical=False),
            "Total cores":      psutil.cpu_count(logical=True),
            "Max Frequency":    f"{cpufreq.max:.2f}Mhz",
            "Min Frequency":    f"{cpufreq.min:.2f}Mhz"
        }
        
        # "memory_info" : {
            # todo
        # }

        # "gpu_info" niet nodig nu
    }

    result = {
        "data" : {}, 
        "meta" : {
            "hardware_info" : hardware_info
        }             
    }
    return result



def main():
    min_rows_cols = 1
    max_rows_cols = 2 # start klein en ga naar max 7
    ran = range(min_rows_cols, max_rows_cols + 1)
    # zou het anders performen als de game (3,5) of (5,3) groot is? 
    # ib: ik denk het niet, maar eens testen.
    gameboard_sizes = [(x,y) for x in ran for y in ran] 
    
    gameboard_sizes = [(1,1),(1,2),(2,1)] # ,(1,3),(3,1),(3,2),(2,3)]

    report = initialise_report()
   
    # counter = 0
    for game_size in gameboard_sizes:
        games_list = pyspiel.registered_names()
        assert "dots_and_boxes" in games_list
        num_rows = game_size[0]
        num_cols = game_size[1]
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
        
        print("Creating game: {}".format(game_string))
        game = pyspiel.load_game(game_string)

        game_config = f"({num_rows},{num_cols})"
        report["data"][game_config] = {}
        record_results(game, report["data"][game_config])
        # counter+=1

    # dirname = "data"
    # current_dir = os.path.dirname(__file__)
    # json_dir_path = os.path.join(current_dir, dirname)
    # os.makedirs(json_dir_path, exist_ok=True)

    # filename = "data.json"
    # json_file_path = os.path.join(json_dir_path, filename)
    # with open(json_file_path, "w") as file:
    #     json.dump(report, file)

    # print(f"dict written to {filename}")

if __name__ == "__main__":
    main()
























# FLAGS = flags.FLAGS

# flags.DEFINE_integer("seed", 12761381, "The seed to use for the RNG.")

# # Supported types of players: "random", "human"
# flags.DEFINE_string("player0", "random", "Type of the agent for player 0.")
# flags.DEFINE_string("player1", "random", "Type of the agent for player 1.")


# def LoadAgent(agent_type, player_id, rng):
#   """Return a bot based on the agent type."""
#   if agent_type == "random":
#     return uniform_random.UniformRandomBot(player_id, rng)
#   elif agent_type == "human":
#     return human.HumanBot()
#   else:
#     raise RuntimeError("Unrecognized agent type: {}".format(agent_type))


# def training(_):
#     rng = np.random.RandomState(FLAGS.seed)
#     games_list = pyspiel.registered_names()
#     assert "dots_and_boxes" in games_list
#     num_rows = 2
#     num_cols = 2
#     game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

#     print("Creating game: {}".format(game_string))
#     game = pyspiel.load_game(game_string)

#     agents = [
#         LoadAgent(FLAGS.player0, 0, rng),
#         LoadAgent(FLAGS.player1, 1, rng),
#     ]

#     state = game.new_initial_state()

#     # Print the initial state
#     print("INITIAL STATE")
#     print(str(state))

#     while not state.is_terminal():
#         current_player = state.current_player()
#         # Decision node: sample action for the single current player
#         legal_actions = state.legal_actions()
#         for action in legal_actions:
#             print(
#                 "Legal action: {} ({})".format(
#                     state.action_to_string(current_player, action), action
#                 )
#             )
#         action = agents[current_player].step(state)
#         action_string = state.action_to_string(current_player, action)
#         print("Player ", current_player, ", chose action: ", action_string)
#         state.apply_action(action)

#         print("")
#         print("NEXT STATE:")
#         print(str(state))
#         if not state.is_terminal():
#             print(str(state.observation_tensor()))

#     # Game is now done. Print utilities for each player
#     returns = state.returns()
#     for pid in range(game.num_players()):
#         print("Utility for player {} is {}".format(pid, returns[pid]))
