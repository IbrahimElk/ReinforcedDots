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
            time_step = env.step([player1_output.action,player2_output.action])
        
        if cur_episode % int(1e4) == 0:
            print("Starting episode : ", cur_episode)

        # de eerste 100 episodes opslaan.
        if cur_episode % 10 == 0 :
            points.append((list(player1_output.probs),list(player2_output.probs)))

        player1.step(time_step)
        player2.step(time_step)
    return points

def get_all_red_lines(
        method:str,
        amt_distinct_start_probs:int,
        num_lines:int=5,
        temperature:float=0.2,
        Kappa:int = 15,
        game = "matrix_bos"):

    lijst = []
    num_actions = get_num_actions(game)
    for _ in range(amt_distinct_start_probs):
        
        random_probs = [random.random() for _ in range(num_actions)]
        total = sum(random_probs)
        normalized_probs = [x/total for x in random_probs]

        multiple_hists_per_learner = []
        for _ in range(num_lines):
            print(normalized_probs)
            [agent1, agent2] = get_correct_agents(method, normalized_probs, num_actions, temperature, Kappa)
            history_of_probs = train_agents(agent1, agent2, game=game, training_episodes=1000)
            multiple_hists_per_learner.append(history_of_probs)
        
        mean_hstr = mean_elementwise(multiple_hists_per_learner)
        startingposition = {
            "starting_probs: " : normalized_probs,
            "line: " : mean_hstr
        }
        lijst.append(startingposition)
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

def get_correct_agents(method:str, init_probs, num_actions, temperature, kappa):
    num_players = 2
    agents = []
    match method:
        case "Q":
            agents =[
                QLearner(player_id=idx, 
                        num_actions=num_actions, 
                        epsilon_schedule=rl_tools.ConstantSchedule(temperature),
                        init_probs=init_probs)
                for idx in range(num_players)
            ]
        case "B" : 
            agents =[
                BoltzmannQLearner(player_id=idx, 
                                num_actions=num_actions,
                                temperature_schedule=rl_tools.ConstantSchedule(temperature),
                                init_probs=init_probs)
                for idx in range(num_players)
            ]
        case "LB" : 
            agents =[
                LenientBoltzmannQLearner(player_id=idx, 
                                num_actions=num_actions,
                                temperature_schedule=rl_tools.ConstantSchedule(temperature),
                                kappa=kappa,
                                init_probs=init_probs)
                for idx in range(num_players)
            ]
        case _: 
            raise ValueError("Invalid method name provided")
    return agents

def record_results(game_name, dict_q_learning):
    dict_q_learning[game_name] = {"Q": [], "B": [], "LB":[]}
    starting_amnt_probs = 5

    # STANDAARD Q LEARNING:
    epsilon_values = [0.2, 0.5, 0.7]
    for epsilon in epsilon_values:
        lijst   = get_all_red_lines(method="Q",
                                    num_lines=5,
                                    amt_distinct_start_probs=starting_amnt_probs, 
                                    temperature=epsilon, 
                                    Kappa=1, # heeft geen invloed, is enkel van invloed voor lenient boltzmann agent.
                                    game=game_name)
        
        # TODO: multiple starting positions, all with num_lines = 5 to take the average. 
        dict_q_learning[game_name]["Q"].append({"epsilon": epsilon, 
                                                "num_lines": 5, 
                                                "data": lijst})
    # # TRADITIONAL BOLtZMANN Q LEARNING
    for temperature in [0.2, 1, 5]: # FIXME: dit interval gekozen, maar nergens opt intenret een aanrader voor interval waarden...
        lijst   = get_all_red_lines(method="B",
                            num_lines=5,
                            amt_distinct_start_probs=starting_amnt_probs, 
                            temperature=temperature, 
                            Kappa=1, 
                            game=game_name)
        
        dict_q_learning[game_name]["B"].append({"temperature": temperature, 
                                                "num_lines": 5, 
                                                "data": lijst})

    # LENIENT BOLtZMANN Q LEARNING
    for Kappa in [5, 10]:
        for temperature in [0.2, 1, 5]:
            lijst = get_all_red_lines(method="LB",
                                num_lines=5, 
                                amt_distinct_start_probs=starting_amnt_probs,
                                temperature=temperature, 
                                Kappa=Kappa, 
                                game=game_name)
            dict_q_learning[game_name]["LB"].append({"kappa": Kappa,
                                                     "temperature": temperature, 
                                                     "num_lines": 5, 
                                                     "data": lijst})

def main():
    game_name = ["matrix_bos", "matrix_sub", "matrix_pd", "matrix_brps"]
    dict_q_learning = {}
    for game in game_name:
        record_results(game, dict_q_learning)

    filename = "data.json"
    directory_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(directory_path, filename)

    with open(json_file_path, "w") as file:
        json.dump(dict_q_learning, file)

    print(f"dict written to {filename}")



if __name__ == "__main__":
    main()