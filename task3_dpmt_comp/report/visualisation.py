import os
import json
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# GOAL:
# Use these the three optimizations (transposition table, symmetry and chains)
# and compare with the provided template algorithm. For various game board
# sizes, plot both the execution times and the number of keys.
# -----------------------------------------------------------------------------

def parseJSON():
    current_dir = os.path.dirname(__file__)
    json_filename = os.path.join(current_dir, 'data.json')

    with open(json_filename, "r") as json_file:
        data = json.load(json_file)
    return data

def construct_plot(x, y, 
                   categorical,
                   title:str,
                   ylabel:str,
                   xlabel:str,
                   legend:str,
                   logy=True):
    
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x, y=y, hue=categorical)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.title(title, fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    if logy:
        plt.yscale('log')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend(title=legend, fontsize=14, title_fontsize=14)
    plt.tight_layout()
    return plt

def save_plot(plt, filename:str):
    current_dir = os.path.dirname(__file__)

    save_dir_png = 'plots/png/'
    save_dir_eps = 'plots/eps/'
    
    folder_path_png = os.path.join(current_dir, save_dir_png)
    folder_path_eps = os.path.join(current_dir, save_dir_eps)

    os.makedirs(folder_path_png, exist_ok=True)
    os.makedirs(folder_path_eps, exist_ok=True)

    save_path_png = os.path.join(folder_path_png, filename)
    save_path_eps = os.path.join(folder_path_eps, filename)

    plt.savefig(save_path_png + ".png" , format='png')
    plt.savefig(save_path_eps + ".eps" , format='eps')

def plot_time(data):
    games = []
    algorithms = []
    times = []

    for game, stats in data["data"].items():
        for algorithm, stat in stats.items():
            games.append(game)
            algorithms.append(algorithm)
            times.append(stat["time"] * 1000)

    plt = construct_plot(games, 
                   times, 
                   algorithms,
                   title="Time Taken for Minimax Search",
                   ylabel="Time (ms)",
                   xlabel="Game Sizes",
                   legend="Algorithms",
                   logy=True)
    save_plot(plt, "plot_time")

def plot_nbkeys(data):
    games = []
    algorithms = []
    nb_keys = []

    for game, stats in data["data"].items():
        for algorithm, stat in stats.items():
            games.append(game)
            algorithms.append(algorithm)
            nb_keys.append(stat["nb_keys"])


    plt = construct_plot(games, 
                   nb_keys, 
                   algorithms,
                   title="Number of Keys in Cache for Minimax Search",
                   ylabel="Number of Keys in Cache",
                   xlabel="Game Sizes",
                   legend="Algorithms",
                   logy=False)
    save_plot(plt, "number_keys")

def plot_htskeys(data):
    games = []
    algorithms = []
    nb_hits = []

    for game, stats in data["data"].items():
        for algorithm, stat in stats.items():
            games.append(game)
            algorithms.append(algorithm)
            nb_hits.append(stat["nb_hits"])

    plt = construct_plot(games, 
                   nb_hits, 
                   algorithms,
                   title="Number of Hits of Cache for Minimax Search",
                   ylabel="Number of Hits of Cache",
                   xlabel="Game Sizes",
                   legend="Algorithms",
                   logy=True)
    save_plot(plt, "number_hits")

def plot_msdkeys(data):
    games = []
    algorithms = []
    nb_misses = []

    for game, stats in data["data"].items():
        for algorithm, stat in stats.items():
            games.append(game)
            algorithms.append(algorithm)
            nb_misses.append(stat["nb_misses"])

    plt = construct_plot(games, 
                   nb_misses, 
                   algorithms,
                   title="Number of Misses of Cache for Minimax Search",
                   ylabel="Number of Misses of Cache",
                   xlabel="Game Sizes",
                   legend="Algorithms",
                   logy=True)
    save_plot(plt, "number_misses")


def plot_keys(data):
    for game, stats in data["data"].items():
        algorithms = []
        nb_keys = []
        nb_hits = []
        nb_misses = []

        for algorithm, stat in stats.items():
            # if algorithm == "minimax_template_search":
            #     break

            algorithms.append(algorithm)
            nb_keys.append(stat["nb_keys"])
            nb_hits.append(stat["nb_hits"])
            nb_misses.append(stat["nb_misses"])
        
        sns.set_style("whitegrid")
        plt.figure(figsize=(12, 6))

        bar_width = 0.2
        index = np.arange(len(algorithms))
        plt.bar(x=index-bar_width, height=nb_keys,     width=bar_width, label='nb_keys')
        plt.bar(x=index,           height=nb_hits,     width=bar_width, label='nb_hits')
        plt.bar(x=index+bar_width, height=nb_misses,   width=bar_width, label='nb_misses')

        plt.xlabel('Algorithms', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.yscale('log')

        plt.xticks(index, algorithms, fontsize=12, rotation=45, ha='right')
        plt.title(f'Number of Keys, Hits, and Misses for Minimax Search in Game Size {game}', fontsize=16)

        plt.legend(fontsize=12)
        plt.tight_layout()
        # plt.show()
        save_plot(plt, "number_keys_hits_misses")

def main():
    parsed_data = parseJSON()
    plot_time(parsed_data)
    plot_nbkeys(parsed_data)
    plot_htskeys(parsed_data)
    plot_msdkeys(parsed_data)
    plot_keys(parsed_data)

if __name__ == "__main__":
    main()