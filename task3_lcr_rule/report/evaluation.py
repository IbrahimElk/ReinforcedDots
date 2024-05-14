import time 
import os 
import sys

import pyspiel
import platform
import psutil

package_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")    # json_dir_path = os.path.join(current_dir, dirname)
sys.path.append(package_directory)

from dotsandboxes_agent1.minimax_search import minimax_search, minimax_chains_search
from dotsandboxes_agent1.alphabeta import minimax_alphabeta_search
from dotsandboxes_agent1.chains_strategy import StrategyAdvisor
from dotsandboxes_agent1.transposition_table import Transposition_Table, TEmpty_Table, TOptimised_Table
from dotsandboxes_agent1.evaluators import eval_maximize_difference

import json

# FIXME:
# al de volgende assumes they have transposition table. 
# dus je vergelijkt de toevoeging van symmerien, chains optimisaties tegenover de baseline
# die enkel de transpostion table heeft. 
# (adners is er niets te vergelijken want naive methode kan amper 2x2 oplossen.)

# -----------------------------------------------------------------------------
# GOAL:
# Use these the three optimizations (transposition table, symmetry and chains)
# and compare with the provided template algorithm. For various game board
# sizes, plot both the execution times and the number of keys.
# -----------------------------------------------------------------------------

def scrape_minimax(minimax, game, state, advisor, table, f):
    print(game)
    t0 = time.time()
    mmvalue, _ = minimax(game=game, transposition_table=table, strategy_advisor=advisor, state=state, value_function=f) # de state wordt niet verandert door minimax, door state.clone(),
    t1 = time.time()

    cache = table.get_cache()
    nb_keys = len(cache.keys())
    nb_hits = table.get_hits()
    nb_misses = table.get_misses()

    results = {
        "time" :            t1-t0,
        "minimax_value" :   mmvalue, # for maximizing player, player 0. 
        "nb_keys":          nb_keys,
        "nb_hits":          nb_hits,
        "nb_misses":        nb_misses,
    }
    return results

def record_results(game, dict_results:dict):
    optims = [(minimax_search, Transposition_Table(), None), 
              (minimax_search, TOptimised_Table(), None), 
              (minimax_chains_search, TEmpty_Table(), None), 
              (minimax_search, TEmpty_Table(), None), 
              (minimax_alphabeta_search, TOptimised_Table(), eval_maximize_difference)
              ]
    

    for optim, tt, f in optims:
        print(optim.__name__)
        state = game.new_initial_state()
        num_rows = state.get_game().get_parameters()['num_rows']
        num_cols = state.get_game().get_parameters()['num_cols']
        advisor = StrategyAdvisor(num_rows, num_cols)

        dict_results[optim.__name__] = scrape_minimax(optim, game, state, advisor, tt, f)

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

        # TODO:
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
    min_rows_cols = 3
    max_rows_cols = 3 # start klein en ga naar max 7
    ran = range(min_rows_cols, max_rows_cols + 1)
    # zou het anders performen als de game (3,5) of (5,3) groot is? 
    # ib: ik denk het niet, maar eens testen.
    gameboard_sizes = [(x,y) for x in ran for y in ran] 
    
    gameboard_sizes = [(1,1), (1,2), (2,2), (1,3)]

    report = initialise_report()
   
    # counter = 0
    for game_size in gameboard_sizes:
        games_list = pyspiel.registered_names()
        assert "dots_and_boxes" in games_list
        num_rows = game_size[0]
        num_cols = game_size[1]
        game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"
        
        print("Creating game: {}".format(game_string))
        game    = pyspiel.load_game(game_string)

        game_config = f"({num_rows},{num_cols})"
        report["data"][game_config] = {}

        record_results(game, report["data"][game_config])
        # counter+=1

    dirname = "data"
    current_dir = os.path.dirname(__file__)
    json_dir_path = os.path.join(current_dir, dirname)
    os.makedirs(json_dir_path, exist_ok=True)

    filename = "data_new.json"
    json_file_path = os.path.join(json_dir_path, filename)
    with open(json_file_path, "w") as file:
        print(report)
        json.dump(report, file)

    print(f"dict written to {filename}")

if __name__ == "__main__":
    main()






















