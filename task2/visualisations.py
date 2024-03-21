import os
import json

from open_spiel.python.egt import dynamics
from open_spiel.python.egt import utils
from open_spiel.python import rl_environment
import open_spiel.python.egt.visualization as vis

from matplotlib import projections
import matplotlib.pyplot as plt

import pyspiel
from open_spiel.python import rl_tools, rl_agent
from open_spiel.python.algorithms.tabular_qlearner import QLearner
from open_spiel.python.algorithms.boltzmann_tabular_qlearner import BoltzmannQLearner


def main():
    """
    Generates the requiered visualisations for the 4 requested matrix games
    """
    game_sub = pyspiel.create_matrix_game("subsidy_game", "Subsidy Game", ["S1","S2"], ["S1","S2"],
                                            [[12,0],[11,10]], [[12,11],[0,10]])
    game_brps = pyspiel.create_matrix_game("rock_paper_scissors", "Biased Rock, Paper, Scissors",["R","P","S"],["R","P","S"],
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
    data_path = os.path.join(current_directory_path,'task2','data.json')
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
                parameters.append(data[game][alg][1]["data"])
                parameters.append(data[game][alg][2]["data"])
                
                parameterlist.append(['epsilon = ' + str(data[game][alg][0]["epsilon"])])
                parameterlist.append(['epsilon = ' + str(data[game][alg][1]["epsilon"])])
                parameterlist.append(['epsilon = ' + str(data[game][alg][2]["epsilon"])])


            elif algorithmdict[alg] == "boltzmann":
                parameters = []
                parameters.append(data[game][alg][0]["data"])
                parameters.append(data[game][alg][1]["data"])
                parameters.append(data[game][alg][2]["data"])

                parameterlist.append(['temperature = ' + str(data[game][alg][0]["temperature"])])
                parameterlist.append(['temperature = ' + str(data[game][alg][1]["temperature"])])
                parameterlist.append(['temperature = ' + str(data[game][alg][2]["temperature"])])


            elif algorithmdict[alg] == "lenient boltzmann":
                parameters = []
                parameters.append(data[game][alg][0]["data"])
                parameters.append(data[game][alg][4]["data"])
                parameters.append(data[game][alg][8]["data"])

                il = []
                il.append('kappa = ' + str(data[game][alg][0]["kappa"]))
                il.append('temperature = ' + str(data[game][alg][0]["temperature"]))
                parameterlist.append(il)
                il = []
                il.append('kappa = ' + str(data[game][alg][4]["kappa"]))
                il.append('temperature = ' + str(data[game][alg][4]["temperature"]))
                parameterlist.append(il)
                il = []
                il.append('kappa = ' + str(data[game][alg][8]["kappa"]))
                il.append('temperature = ' + str(data[game][alg][8]["temperature"]))
                parameterlist.append(il)



            else:
                raise ValueError("Unknown algorithm name")
            
            
            # Decide which plot function to use.
            if "Rock, Paper, Scissors" not in gamedict[game].get_type().long_name:
                    ctr = 0
                    for trajectorylist in parameters:
                        plot_trajectory_2x2(gamedict[game],algorithmdict[alg],trajectorylist,parameterlist[ctr])
                        ctr += 1

            else:
                plot_trajectory_rps(gamedict[game],algorithmdict[alg],trajectorylist,parameterlist)

    f.close()
        
   
def plot_replicator_dynamics_rps(game):
    """
    Plots the replicator dynamics for a given rock, paper, scissor matrix game.
    """
    current_directory_path = os.getcwd()
    subfolder_path = os.path.join(current_directory_path,'task2','images')
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
    subfolder_path = os.path.join(current_directory_path,'task2','images')
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
    trajectorylist = trajectorylist[0][2:]
    
    current_directory_path = os.getcwd()
    subfolder_path = os.path.join(current_directory_path,'task2','images')
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    projections.register_projection(vis.Dynamics2x2Axes)
    payoff_tensor = utils.game_payoffs_array(game)
    repdyn = dynamics.MultiPopulationDynamics(payoff_tensor,dynamics.replicator)

    # Plot replicator dynamics as a vector field.
    fig = plt.figure(figsize=(4,4))
    subplt = fig.add_subplot(111,projection="2x2")
    subplt.quiver(repdyn,color='blue')

    # Plot trajectories
    trajectorynr = 0
    colordict = {1:'red',2:'black',3:'green'}

    for trajectory in trajectorylist:
        trajectorynr += 1
        x = []
        y = []

        for prob_hist in trajectory:
            x.append(prob_hist[0][0])
            y.append(prob_hist[1][0])
        
        subplt.plot(x,y,'-',alpha=0.5,color=colordict[trajectorynr])
        subplt.plot(x[0],y[0],'o',alpha=1,color=colordict[trajectorynr])
        subplt.plot(x[-1],y[-1],'s',alpha=1,color=colordict[trajectorynr])
   
    subplt.set_title(f"Trajectory plot: {game.get_type().long_name} using {alg} ({stringify_list(parameterlist)}).")
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
    subfolder_path = os.path.join(current_directory_path,'task2','images')
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    projections.register_projection(vis.Dynamics3x3Axes)
    payoff_tensor = utils.game_payoffs_array(game)
    repdyn = dynamics.SinglePopulationDynamics(payoff_tensor,dynamics.replicator)

    # Plot replicator dynamics as a vector field.
    fig = plt.figure(figsize=(4,4))
    subplt = fig.add_subplot(111,projection="3x3")
    subplt.quiver(repdyn,color='blue')

    # Plot trajectories
    for trajectory in trajectorylist:
        for prob_hist in trajectory:
            x = [hist[0][0] for hist in prob_hist]
            y = [hist[1][0] for hist in prob_hist]
            subplt.plot(x,y,color='black')
   
    subplt.set_title(f"Trajectory plot: {game.get_type().long_name} using {alg}.")
    subplt.set_labels(["Rock", "Paper", "Scissors"])
    filepath = os.path.join(subfolder_path,"traj_plot_" + game.get_type().short_name +"_"+ alg + ".png")
    plt.savefig(filepath)
    plt.show()


def train_agents(
                 player1:rl_agent.AbstractAgent, 
                 player2:rl_agent.AbstractAgent,
                 game = "matrix_bos", 
                 training_episodes = 10**5):
    points = []
    env = rl_environment.Environment(game)    
    for cur_episode in range(training_episodes):
        time_step = env.reset()
        while not time_step.last():
            wife_output = player1.step(time_step)
            husband_output = player2.step(time_step)
            time_step = env.step([wife_output.action,husband_output.action])
        
        if cur_episode % int(1e4) == 0:
            print("Starting episode : ", cur_episode)

        if cur_episode % int(1e2) == 0:
            # print("Starting episode : ", cur_episode)
            # TODO: from trial and error bleek dat 10**5 datapunten te veel is
            # dus nu, enkel 10 punten per training (per lijn).
            points.append((wife_output.probs,husband_output.probs))

        player1.step(time_step)
        player2.step(time_step)

    print("wife_output.action,husband_output.action")
    print(wife_output.action,husband_output.action)
    print("(wife_output.probs,husband_output.probs)")
    print((wife_output.probs,husband_output.probs))
    return points

def get_all_red_lines(
        method:str,
        num_lines:int=5,
        temperature:float=0.2,
        Kappa:int = 15,
        game = "matrix_bos"):

    num_players = 2
    if game == "subsidy_game": 
        game = pyspiel.create_matrix_game("subsidy_game", "Subsidy Game", ["S1","S2"], ["S1","S2"], [[12,0], [11,10]], [[12,11], [0,10]])
    env = rl_environment.Environment(game)    
    num_actions = env.action_spec()["num_actions"]
    [agent1, agent2] = get_correct_agents(method, num_players, num_actions, temperature, Kappa)

    multiple_lines_per_learner = []
    for i in range(num_lines):
        red_line = train_agents(agent1,agent2,game=game, training_episodes=10**5)
        multiple_lines_per_learner.append(red_line)

    print("=============================================================================")
    return multiple_lines_per_learner, 

def get_correct_agents(method:str, num_players, num_actions, temperature, kappa):
    agents = []
    match method:
        case "Q":
            agents =[
                QLearner(player_id=idx, 
                        num_actions=num_actions, 
                        epsilon_schedule=rl_tools.ConstantSchedule(temperature))
                for idx in range(num_players)
            ]
        case "B" : 
            agents =[
                BoltzmannQLearner(player_id=idx, 
                                num_actions=num_actions,
                                temperature_schedule=rl_tools.ConstantSchedule(temperature))
                for idx in range(num_players)
            ]
        # case "LB" : 
        #     agents =[
        #         LenientBoltzmannQLearner(player_id=idx, 
        #                         num_actions=num_actions,
        #                         temperature_schedule=rl_tools.ConstantSchedule(temperature),
        #                         Kappa=kappa)
        #         for idx in range(num_players)
        #     ]
        case _: 
            raise ValueError("Invalid method name provided")
    return agents

def record_results(game_name, dict_q_learning):
    dict_q_learning[game_name] = {"Q": [], "B": [], "LB":[]}

    # STANDAARD Q LEARNING:
    epsilon_values = [round(i * 0.1, 1) for i in range(10)]
    for epsilon in epsilon_values:
        lijst   = get_all_red_lines(method="Q",
                            num_lines=5, 
                            temperature=epsilon, 
                            Kappa=1, # heeft geen invloed, is enkel van invloed voor lenient boltzmann agent.
                            game=game_name)
        
        dict_q_learning[game_name]["Q"].append({"epsilon": epsilon, 
                                                "num_lines": 5, 
                                                "data": lijst})

    # # TRADITIONAL BOLtZMANN Q LEARNING
    for temperature in range(0,100,10): # FIXME: dit interval gekozen, maar nergens opt intenret een aanrader voor interval waarden...
        lijst   = get_all_red_lines(method="B",
                            num_lines=5, 
                            temperature=temperature, 
                            Kappa=1, 
                            game=game_name)
        
        if game_name not in dict_q_learning:
            dict_q_learning[game_name] = {"B": []}
        dict_q_learning[game_name]["B"].append({"temperature": temperature, 
                                                "num_lines": 5, 
                                                "data": lijst})

    # # LENIENT BOLtZMANN Q LEARNING
    # for Kappa in range(10,100,10):
    #     for temperature in range(0,100,10):
    #         lijst = get_all_red_lines(method="LB",
    #                             num_lines=5, 
    #                             temperature=epsilon, 
    #                             Kappa=Kappa, 
    #                             game=game_name)
    #         # print(rewards_lijst) # nested lijst van rewards

def main2():
    game_name = ["matrix_bos", "matrix_rps", "matrix_pd", "matrix_brps"]
    dict_q_learning = {}
    for game in game_name:
        record_results(game, dict_q_learning)

    filename = f"data.json"
    with open(filename, "w") as file:
        json.dump(dict_q_learning, file)

    print(f"dict written to {filename}")

def stringify_list(lst:list):
    """
    Converts a list of strings to a single string.
    """
    result = ""
    for i in lst:
        result += str(i) + " "
    
    return result

main()
# main2()   