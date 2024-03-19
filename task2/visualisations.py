from open_spiel.python.egt import dynamics
from open_spiel.python.egt import utils
from open_spiel.python import rl_environment
import open_spiel.python.egt.visualization as vis

from matplotlib import projections
import matplotlib.pyplot as plt

import pyspiel
import os

def main():
    """
    Generates the requiered visualisations for the 4 requested matrix games
    """
    game_sub = pyspiel.create_matrix_game("subsidy_game", "Subsidy Game", ["S1","S2"], ["S1","S2"],
                                      [[12,0],[11,10]], [[12,11],[0,10]])
    game_rps = pyspiel.load_matrix_game("matrix_rps")

    ## TODO add other matrix games above.

    plot_replicator_dynamics_2x2(game_sub)
    plot_replicator_dynamics_rps(game_rps)

    

def plot_replicator_dynamics_rps(game, history = None):
    current_directory_path = os.getcwd()
    subfolder_path = os.path.join(current_directory_path,'task2','images')
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    projections.register_projection(vis.Dynamics3x3Axes)
    payoff_tensor = utils.game_payoffs_array(game)
    dyn = dynamics.SinglePopulationDynamics(payoff_tensor,dynamics.replicator)

    fig = plt.figure(figsize=(4,4))
    rpdyn = fig.add_subplot(111, projection="3x3")
    rpdyn.quiver(dyn)
    rpdyn.set_labels(["Rock", "Paper", "Scissors"])
    rpdyn.set_title(f"{game.get_type().long_name} trajectory plot")
    filepath = os.path.join(subfolder_path,"traj_plot_" + game.get_type().short_name +".png")
    plt.savefig(filepath)
    plt.show()

def plot_replicator_dynamics_2x2(game,history=None):
    current_directory_path = os.getcwd()
    subfolder_path = os.path.join(current_directory_path,'task2','images')
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    projections.register_projection(vis.Dynamics2x2Axes)
    payoff_tensor = utils.game_payoffs_array(game)
    dyn = dynamics.MultiPopulationDynamics(payoff_tensor,dynamics.replicator)

    fig = plt.figure(figsize=(4,4))
    rpdyn = fig.add_subplot(111, projection="2x2")
    rpdyn.streamplot(dyn)
    rpdyn.set_xlabel(f"P(Player 1 chooses {game})")
    rpdyn.set_title(f"{game.get_type().long_name} trajectory plot")
    filepath = os.path.join(subfolder_path,"traj_plot_" + game.get_type().short_name +".png")
    plt.savefig(filepath)
    plt.show()


main()
