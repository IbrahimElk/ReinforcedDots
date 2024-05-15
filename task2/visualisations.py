import os
import json
import random 

from open_spiel.python.egt import dynamics
from open_spiel.python.egt import utils
from open_spiel.python import rl_environment
import open_spiel.python.egt.visualization as vis
import numpy as np

from matplotlib import projections
import matplotlib.pyplot as plt

import pyspiel
from open_spiel.python import rl_tools, rl_agent
from open_spiel.python.algorithms.tabular_qlearner import QLearner
from open_spiel.python.algorithms.boltzmann_tabular_qlearner import BoltzmannQLearner
from lenient_boltzmann_tabular_qlearner import LenientBoltzmannQLearner


colordict = {
    1: 'red',
    2: 'blue',
    3: 'green',
    4: 'orange',
    5: 'purple',
    6: 'cyan',
    7: 'magenta',
    8: 'yellow',
    9: 'brown',
    10: 'lime',
    11: 'pink',
    12: 'teal',
    13: 'lavender',
    14: 'beige',
    15: 'maroon',
}

save_path = '035'
global_filename = save_path + '.json'

def main():
    """
    Generates the requiered visualisations for the 4 requested matrix games
    """
    game_sub = pyspiel.create_matrix_game("subsidy_game", "Subsidy Game", ["S1","S2"], ["S1","S2"],
                                            [[12,0],[11,10]], [[12,11],[0,10]])
    game_brps = pyspiel.create_matrix_game("brock_paper_scissors", "Biased Rock, Paper, Scissors",["R","P","S"],["R","P","S"],
                                          [[0,-0.05,0.25],[0.05,0,-0.5],[-0.25,0.5,0]],[[0,0.05,-0.25],[-0.05,0,0.5],[0.25,-0.5,0]])
    game_bos = pyspiel.create_matrix_game("battle_of_the_sexes", "Battle of the Sexes", 
                                          ["O","M"],["O","M"], [[3,0],[0,2]],[[2,0],[0,3]])
    game_pd = pyspiel.create_matrix_game("prisoners_dilemma", "Prisoners Dilemma", 
                                         ["C","D"],["C","D"], [[-1,-4],[0,-3]],[[-1,0],[-4,-3]])

    #games = [game_sub,game_bos,game_brps,game_pd]
    gamedict = {'matrix_bos':game_bos, 'matrix_brps':game_brps, 'matrix_pd':game_pd, 'matrix_sub':game_sub,'matrix_rps':game_brps}
    algorithmdict = {"Q":"e-greedy","LB":"lenient boltzmann","B":"boltzmann"}

    plot_replicator_dynamics_2x2(game_sub)
    plot_replicator_dynamics_rps(game_brps)
    plot_replicator_dynamics_2x2(game_bos)
    plot_replicator_dynamics_2x2(game_pd)
    
    current_directory_path = os.getcwd()
    data_path = os.path.join(current_directory_path,'',global_filename)
    f = open(data_path,encoding='utf-8')
    data = json.load(f)

    # [[actie 1 prob,actie 2 prob], [actie 1 prob,actie 2 prob]]
    # enkel actie 1 prob van beide spelers nodig

    for game in data:
        print(gamedict[game].get_type().long_name)
        
        for alg in data[game]:            
            parameterlist = []
            
            if algorithmdict[alg] == "e-greedy":
                parameters = []
                parameters.append(data[game][alg][0]["data"])
                # parameters.append(data[game][alg][1]["data"])
                # parameters.append(data[game][alg][2]["data"])
                
                parameterlist.append(['epsilon = ' + str(data[game][alg][0]["epsilon"])])
                # parameterlist.append(['epsilon = ' + str(data[game][alg][1]["epsilon"])])
                # parameterlist.append(['epsilon = ' + str(data[game][alg][2]["epsilon"])])


            elif algorithmdict[alg] == "boltzmann":
                parameters = []
                parameters.append(data[game][alg][0]["data"])
                # parameters.append(data[game][alg][1]["data"])
                # parameters.append(data[game][alg][2]["data"])

                parameterlist.append(['temperature = ' + str(data[game][alg][0]["temperature"])])
                # parameterlist.append(['temperature = ' + str(data[game][alg][1]["temperature"])])
                # parameterlist.append(['temperature = ' + str(data[game][alg][2]["temperature"])])


            elif algorithmdict[alg] == "lenient boltzmann":
                parameters = []

                # kappa 5
                # print(data[game][alg][0]["kappa"])
                # print(data[game][alg][1]["kappa"])
                # print(data[game][alg][2]["kappa"])
                # parameters.append(data[game][alg][0]["data"])
                # parameters.append(data[game][alg][1]["data"])
                # parameters.append(data[game][alg][2]["data"])
                
                # kappa 10
                print(data[game][alg][0]["kappa"])
                print(data[game][alg][1]["kappa"])
                # print(data[game][alg][5]["kappa"])
                parameters.append(data[game][alg][0]["data"])
                parameters.append(data[game][alg][1]["data"])
                # parameters.append(data[game][alg][5]["data"])

                
                il = []
                il.append('kappa = ' + str(data[game][alg][0]["kappa"]))
                il.append('temperature = ' + str(data[game][alg][0]["temperature"]))
                parameterlist.append(il)
                il = []
                il.append('kappa = ' + str(data[game][alg][1]["kappa"]))
                il.append('temperature = ' + str(data[game][alg][1]["temperature"]))
                parameterlist.append(il)
                # il = []
                # il.append('kappa = ' + str(data[game][alg][5]["kappa"]))
                # il.append('temperature = ' + str(data[game][alg][5]["temperature"]))
                # parameterlist.append(il)

            else:
                raise ValueError("Unknown algorithm name")
            
            
            # Decide which plot function to use.
            if "Rock, Paper, Scissors" not in gamedict[game].get_type().long_name:
                ctr = 0
                for trajectorylist in parameters:
                    plot_trajectory_2x2(gamedict[game],
                                        algorithmdict[alg],
                                        trajectorylist,
                                        parameterlist[ctr])
                    ctr += 1

            else:
                ctr = 0
                for trajectorylist in parameters:
                    plot_trajectory_rps(gamedict[game],algorithmdict[alg],trajectorylist,parameterlist[ctr])
                    ctr += 1

    f.close()
        
   
def plot_replicator_dynamics_rps(game):
    """
    Plots the replicator dynamics for a given rock, paper, scissor matrix game.
    """
    current_directory_path = os.getcwd()
    subfolder_path = os.path.join(current_directory_path, save_path, 'figures_dyn')
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    projections.register_projection(vis.Dynamics3x3Axes)
    payoff_tensor = utils.game_payoffs_array(game)
    dyn = dynamics.SinglePopulationDynamics(payoff_tensor,dynamics.replicator)

    # Stream plot
    fig = plt.figure(figsize=(4,4))
    rpdyn = fig.add_subplot(111, projection="3x3")
    rpdyn.streamplot(dyn,density=0.75,color='black')
    
    # Quiver plot
    rpdyn.quiver(dyn,color='blue')
    
    
    rpdyn.set_labels(["Rock", "Paper", "Scissors"])
    rpdyn.set_title(f"Directional field plot: {game.get_type().long_name}")
    filepath = os.path.join(subfolder_path,"dir_field_plot_" + game.get_type().short_name +".png")
    plt.savefig(filepath)
    #plt.show()

def plot_replicator_dynamics_2x2(game):
    """
    Plots the replicator dynamics for a given 2x2 matrix game.
    """
    current_directory_path = os.getcwd()
    subfolder_path = os.path.join(current_directory_path,save_path, 'figures_dyn')
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    projections.register_projection(vis.Dynamics2x2Axes)
    payoff_tensor = utils.game_payoffs_array(game)
    dyn = dynamics.MultiPopulationDynamics(payoff_tensor,dynamics.replicator)

    # Stream plot
    fig = plt.figure(figsize=(4,4))
    rpdyn = fig.add_subplot(111, projection="2x2")
    rpdyn.streamplot(dyn,density=0.75,color='black')

    # Quiver plot
    rpdyn.quiver(dyn,color='blue')
    
    plt.xlim(-0.01,1.01)
    plt.ylim(-0.01,1.01)
    plt.xlabel(f"P({game.row_action_name(0)}) Agent 1")
    plt.ylabel(f"P({game.row_action_name(0)}) Agent 2")
    rpdyn.set_title(f"Directional field plot: {game.get_type().long_name}")
    filepath = os.path.join(subfolder_path,"dir_field_plot_" + game.get_type().short_name +".png")
    plt.savefig(filepath)
    #plt.show()

def plot_trajectory_2x2(game,alg:str,trajectorylist,parameterlist):
    """
    Plots possible trajectories for a given 2x2 matrix game using a , 
    by providing a list of trajectories containing the history of the 
    states achieved during the self-play.
    """

    # trajectorylist = trajectorylist[0]
    # print(trajectorylist)
    
    current_directory_path = os.getcwd()
    subfolder_path = os.path.join(current_directory_path,save_path, 'figures_trj')
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    projections.register_projection(vis.Dynamics2x2Axes)
    payoff_tensor = utils.game_payoffs_array(game)
    repdyn = dynamics.MultiPopulationDynamics(payoff_tensor,dynamics.replicator)

    # Plot replicator dynamics as a vector field.
    fig = plt.figure(figsize=(10,10))
    subplt = fig.add_subplot(111,projection="2x2")
    subplt.quiver(repdyn,color='black',alpha=0.2)

    # Plot trajectories
    trajectorynr = 0

    for trajectory in trajectorylist:
        x = []
        y = []

        for prob_hist in trajectory:
            x.append(prob_hist[0][0])
            y.append(prob_hist[1][0])
        
        trajectorynr += 1
        
        subplt.plot(x,y,'-',linewidth=4-trajectorynr,alpha=0.5,color=colordict[trajectorynr])
        subplt.plot(x[0],y[0],'o',alpha=1,color=colordict[trajectorynr])
        subplt.plot(x[-1],y[-1],'s',alpha=1,color=colordict[trajectorynr])


   
#    ({stringify_list(parameterlist)})
    subplt.set_title(f"Trajectory plot: {game.get_type().long_name} using {alg}.")
    plt.xlim(-0.01,1.01)
    plt.ylim(-0.01,1.01)
    plt.xlabel(f"P({game.row_action_name(0)}) Agent 1")
    plt.ylabel(f"P({game.row_action_name(0)}) Agent 2")
    filepath = os.path.join(subfolder_path,"traj_plot_" + game.get_type().short_name +"_"+ alg + stringify_list(parameterlist) + ".png")
    plt.savefig(filepath)
    #plt.show()

def plot_trajectory_rps(game,alg:str,trajectorylist,parameterlist):
    """
    Plots possible trajectories for the requested rock, paper, scissors game using a , 
    by providing a list of trajectories containing the history of the 
    states achieved during the self-play.
    """
    current_directory_path = os.getcwd()
    subfolder_path = os.path.join(current_directory_path, save_path,'figures_rps_trj')
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    projections.register_projection(vis.Dynamics3x3Axes)
    payoff_tensor = utils.game_payoffs_array(game)
    repdyn = dynamics.SinglePopulationDynamics(payoff_tensor,dynamics.replicator)

    # Plot replicator dynamics as a vector field.
    fig = plt.figure(figsize=(10,10))
    subplt = fig.add_subplot(111,projection="3x3")
    subplt.quiver(repdyn,color='black',alpha=0.2)

    # Plot trajectories
    trajectorynr = 0
    # colordict = {1:'red',2:'blue',3:'green'}

    for trajectory in trajectorylist:
        x = []

        for prob_hist in trajectory:
            x.append(prob_hist[0])
        
        trajectorynr += 1

        subplt.plot(x,linewidth=4-trajectorynr,alpha=0.5,color=colordict[trajectorynr])
        subplt.scatter([x[0]],marker='o',alpha=1,color=colordict[trajectorynr])
        subplt.scatter([x[-1]],marker='s',alpha=1,color=colordict[trajectorynr])
   

#    ({stringify_list(parameterlist)})
    subplt.set_title(f"Trajectory plot: {game.get_type().long_name} using {alg}.")
    subplt.set_labels(["Rock", "Paper", "Scissors"])
    filepath = os.path.join(subfolder_path,"traj_plot_" + game.get_type().short_name +"_"+ alg + stringify_list(parameterlist) + ".png")
    plt.savefig(filepath)
    # plt.show()

def stringify_list(lst:list):
    """
    Converts a list of strings to a single string.
    """
    result = ""
    for i in lst:
        result += str(i) + " "
    
    return result


if __name__ == "__main__":
    main()