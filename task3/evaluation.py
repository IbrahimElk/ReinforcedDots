import time 

# FIXME:
# al de volgende assumes they have transposition table. 
# dus je vergelijkt de toevoeging van symmerien, chains optimisaties tegenover de baseline
# die enkel de transpostion table heeft. 
# (adners is er niets te vergelijken want naive methode kan amper 2x2 oplossen.)

from minimax.transpositon_minimax import minimax_transposition_search, Transposition_Table
from minimax.symmetry_minimax import minimax_symmetry_search
from minimax.chains_minimax import minimax_chains_search
from minimax.template_minimax import minimax_naive_search
from alphabeta_minimax import minimax_alphabeta_search

import pyspiel
import platform
import psutil

# Problem: timing only from initial state. 
# TODO: 
# get timing results for several empty boards (everage it out, and add std to barplot)
# and 5 problems from (Berlekamp 2000).
# 1) "110011000010100011000101"
# 2) "111000000000010011110111"
# 3) "111000000000010011110110"
# 4) "111011000100100001010101"
# 5) "011110011100101010011000"

# TODO:
# everythign together:
# see file alphabeta_minimax.py 

# TODO: 
# evaluate with self play and random agent ? 
# to see how good it actually is, to see if it understands the concepts of chains etc
# will be needed in the report!! 

# -----------------------------------------------------------------------------
# GOAL:
# Use these the three optimizations (transposition table, symmetry and chains)
# and compare with the provided template algorithm. For various game board
# sizes, plot both the execution times and the number of keys.
# -----------------------------------------------------------------------------

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
              minimax_alphabeta_search
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






















