import os
import json
import random 
import pyspiel
import numpy as np

from open_spiel.python import rl_environment
from open_spiel.python import rl_tools, rl_agent
from open_spiel.python.algorithms.tabular_qlearner import QLearner
from open_spiel.python.algorithms.boltzmann_tabular_qlearner import BoltzmannQLearner
from lenient_boltzmann_tabular_qlearner import LenientBoltzmannQLearner

def train_agents(player1: rl_agent.AbstractAgent, 
                 player2: rl_agent.AbstractAgent,
                 game = "matrix_bos", 
                 training_episodes = 25000):
    points = []
    if game == "matrix_sub": 
        game = pyspiel.create_matrix_game("subsidy_game", "Subsidy Game", ["S1","S2"], ["S1","S2"], [[12,0], [11,10]], [[12,11], [0,10]])
    
    env = rl_environment.Environment(game)    
    
    for cur_episode in range(training_episodes):
        # if cur_episode % int(1000) == 0:
            # win_rates = eval_against_random_bots(env, [wife, husband], random_agents, 1000)
            # pass
        time_step = env.reset()
        while not time_step.last():
            player1_output = player1.step(time_step)
            player2_output = player2.step(time_step)
            time_step = env.step([player1_output.action, player2_output.action])
        
        # if cur_episode % int(5e2) == 0:
        #     print("Starting episode : ", cur_episode)

        # de eerste 100 episodes opslaan.
        # cur_episode % 500 == 0 or
        # or cur_episode <= 1000
        # cur_episode % 100 == 0 or  
        if cur_episode <= 200 :
            points.append((list(player1_output.probs),list(player2_output.probs)))

            # points.append((list(player1_output.probs),list(player2_output.probs)))

        player1.step(time_step)
        player2.step(time_step)
    return points

def get_all_red_lines(
        method:str,
        num_lines:int=5,
        Kappa:int = 15,
        game = "matrix_bos"):

    lijst = []
    num_actions = get_num_actions(game)
    if num_actions == 2: 
        intial_q_values = [
            [{0: 0, 1: 0},{0: 0, 1: 0}],
            [{0: -1, 1: 0},{0: 1, 1: 0}], 
            [{0: 0, 1: -0.25}, {0: 0, 1: 0.75}], 
            [{0: 1, 1: 0.5},{0: 0, 1: 0}]]
    else : 
        intial_q_values = [
            [{0: 0, 1: 0, 2: 0},      {0: 0, 1: 0, 2: 0}],
            [{0: -1, 1: 0, 2: 1},     {0: 1, 1: 0, 2: 0}], 
            [{0: 0, 1: -0.25, 2: -1},  {0: 0, 1: 0.75, 2: 0}], 
            [{0: 1, 1: 0.5, 2: 0},    {0: 0, 1: 0, 2: 0.5}]]

    amt_distinct_start_probs = len(intial_q_values)
    for i in range(amt_distinct_start_probs):
        # multiple_hists_per_learner = []
        # for _ in range(num_lines):
        [agent1, agent2] = get_correct_agents(method, intial_q_values[i], num_actions, Kappa)
        history_of_probs = train_agents(agent1, agent2, game=game, training_episodes=25000)
        # multiple_hists_per_learner.append(history_of_probs)
        
        # mean_hstr = mean_elementwise(multiple_hists_per_learner)
        lijst.append(history_of_probs)
    return lijst

def mean_elementwise(nested_lst):
    nested_list = np.array(nested_lst)
    mean_values = np.mean(nested_list, axis=0)
    # mean_values = np.expand_dims(mean_values, axis=0)
    return mean_values.tolist()

def get_num_actions(game:str):
    if game == "matrix_sub": 
        game = pyspiel.create_matrix_game("subsidy_game", "Subsidy Game", ["S1","S2"], ["S1","S2"], [[12,0], [11,10]], [[12,11], [0,10]])
    
    env = rl_environment.Environment(game)    
    num_actions = env.action_spec()["num_actions"]
    return num_actions

def get_correct_agents(method:str, qvalues, num_actions, kappa):
    num_players = 2
    agents = []
    match method:
        case "Q":
            step_size = 0.01
            agents =[
                QLearner(player_id=idx, 
                        num_actions=num_actions, 
                        epsilon_schedule=rl_tools.LinearSchedule(0.3,0.05, 1000),
                        step_size=step_size
                        )
                for idx in range(num_players)
            ]
        case "B" : 
            step_size = 0.001
            agents =[
                BoltzmannQLearner(player_id=idx, 
                                num_actions=num_actions,
                                step_size = step_size,
                                temperature_schedule=rl_tools.LinearSchedule(0.3, 0.01, 50000))
                for idx in range(num_players)
            ]
        case "LB" : 
            step_size = 0.001
            agents =[
                LenientBoltzmannQLearner(player_id=idx, 
                                num_actions=num_actions,
                                temperature_schedule=rl_tools.LinearSchedule(0.3, 0.01, 50000),
                                kappa=kappa)
                for idx in range(num_players)
            ]
        case _: 
            raise ValueError("Invalid method name provided")

    for i in range(len(agents)):
        agents[i]._q_values['[0.0]']  = qvalues[i]
            
    return agents
    
def record_results(game_name, dict_q_learning):
    dict_q_learning[game_name] = {"Q": [], "B": [], "LB":[]}

    # STANDAARD Q LEARNING:
    # epsilon_values = [0.2, 0.5, 0.7]
    # for epsilon in epsilon_values:
    lijst   = get_all_red_lines(method="Q",
                                Kappa=1, # heeft geen invloed, is enkel van invloed voor lenient boltzmann agent.
                                game=game_name)
    
    # TODO: multiple starting positions, all with num_lines = 5 to take the average. 
    dict_q_learning[game_name]["Q"].append({"epsilon": -1, 
                                            "data": lijst})
    # # TRADITIONAL BOLtZMANN Q LEARNING
    # for temperature in [0.2, 0.5, 0.7]: # FIXME: dit interval gekozen, maar nergens opt intenret een aanrader voor interval waarden...
    lijst   = get_all_red_lines(method="B",
                        Kappa=1, 
                        game=game_name)
    
    dict_q_learning[game_name]["B"].append({"temperature": -1, 
                                            "data": lijst})

    # LENIENT BOLtZMANN Q LEARNING
    for Kappa in [5, 10]:
        lijst = get_all_red_lines(method="LB",
                            Kappa=Kappa, 
                            game=game_name)
        dict_q_learning[game_name]["LB"].append({"kappa": Kappa,
                                                 "temperature": -1, 
                                                 "data": lijst})

def main():
    game_name = ["matrix_bos" , "matrix_sub", "matrix_pd" , "matrix_brps"]
    dict_q_learning = {}
    for game in game_name:
        record_results(game, dict_q_learning)

    # O1   -> (1, 0.05,25000) + (1, 0.01, 30000) + (1, 0.01, 25000)           + step sizes (both) + points iedre 100 + eerste 100
    # O2   -> (0.75, 0.05,25000) + (0.75, 0.01, 30000) + (0.75, 0.01, 25000)  + step sizes (both) + points iedre 100 + eerste 100
    # O3   -> (0.5, 0.05,25000)  + (0.5, 0.01, 30000)  + (0.5,  0.01, 25000)  + step sizes (both) + points iedre 100 + eerste 100
    # O4   -> (0.25, 0.05,25000) + (0.25, 0.01, 30000) + (0.25, 0.01, 25000)  + step sizes (both) + points iedre 100 + eerste 100
    # O5   -> (0.1, 0.05,25000) + (0.1, 0.01, 30000) + (0.1, 0.01, 25000)     + step sizes (both) + points iedre 100 + eerste 100

    # O6   -> (1, 0.05,25000) + (1, 0.01, 30000) + (1, 0.01, 25000)           + no step sizes (both) + points iedre 100 + eerste 100
    # O7   -> (0.75, 0.05,25000) + (0.75, 0.01, 30000) + (0.75, 0.01, 25000)  + no step sizes (both) + points iedre 100 + eerste 100
    # O8   -> (0.5, 0.05,25000)  + (0.5, 0.01, 30000)  + (0.5,  0.01, 25000)  + no step sizes (both) + points iedre 100 + eerste 100
    # O9   -> (0.25, 0.05,25000) + (0.25, 0.01, 30000) + (0.25, 0.01, 25000)  + no step sizes (both) + points iedre 100 + eerste 100
    # 010  -> (0.1, 0.05,25000) + (0.1, 0.01, 30000) + (0.1, 0.01, 25000)     + no step sizes (both) + points iedre 100 + eerste 100

    # 011  -> (1, 0.05,25000) + (1, 0.01, 30000) + (1, 0.01, 25000)           + no step sizes (both) + points iedre 100 + geen eerste 100
    # 012  -> (0.75, 0.05,25000) + (0.75, 0.01, 30000) + (0.75, 0.01, 25000)  + no step sizes (both) + points iedre 100 + geen eerste 100
    # 013  -> (0.5, 0.05,25000)  + (0.5, 0.01, 30000)  + (0.5,  0.01, 25000)  + no step sizes (both) + points iedre 100 + geen eerste 100
    # 014  -> (0.25, 0.05,25000) + (0.25, 0.01, 30000) + (0.25, 0.01, 25000)  + no step sizes (both) + points iedre 100 + geen eerste 100
    # 015  -> (0.1, 0.05,25000) + (0.1, 0.01, 30000) + (0.1, 0.01, 25000)     + no step sizes (both) + points iedre 100 + geen eerste 100
    
    # 016  -> (1, 0.05,25000) + (1, 0.01, 30000) + (1, 0.01, 25000)           + no step sizes (both) + geen points iedre 100 + eerste 100
    # 017  -> (0.75, 0.05,25000) + (0.75, 0.01, 30000) + (0.75, 0.01, 25000)  + no step sizes (both) + geen points iedre 100 + eerste 100
    # 018  -> (0.5, 0.05,25000)  + (0.5, 0.01, 30000)  + (0.5,  0.01, 25000)  + no step sizes (both) + geen points iedre 100 + eerste 100
    # 019  -> (0.25, 0.05,25000) + (0.25, 0.01, 30000) + (0.25, 0.01, 25000)  + no step sizes (both) + geen points iedre 100 + eerste 100
    # 020  -> (0.1, 0.05,25000) + (0.1, 0.01, 30000) + (0.1, 0.01, 25000)     + no step sizes (both) + geen points iedre 100 + eerste 100


    # 21 rl_tools.LinearSchedule(0.3,0.05,num_train_episodes)
    filename = "022.json"
    directory_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(directory_path, filename)

    with open(json_file_path, "w") as file:
        json.dump(dict_q_learning, file)

    print(f"dict written to {filename}")



if __name__ == "__main__":
    main()