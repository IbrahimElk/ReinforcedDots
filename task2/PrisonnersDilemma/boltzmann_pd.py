import logging
from absl import app
import numpy as np

from open_spiel.python import rl_tools
from open_spiel.python import rl_environment
from open_spiel.python.algorithms import random_agent
from open_spiel.python.algorithms.boltzmann_tabular_qlearner import BoltzmannQLearner

def eval_against_random_bots(env, trained_agents, random_agents, num_episodes):
  """Evaluates `trained_agents` against `random_agents` for `num_episodes`."""
  wins = np.zeros(2)
  random_wins = np.zeros(2)
  for player_pos in range(2):
    if player_pos == 0:
      cur_agents = [trained_agents[0], random_agents[1]]
    else:
      cur_agents = [random_agents[0], trained_agents[1]]
    for _ in range(num_episodes):
      time_step = env.reset()
      while not time_step.last():
        traiend_agent_output = cur_agents[player_pos].step(time_step, is_evaluation=True)
        random_agent_output = cur_agents[1-player_pos].step(time_step, is_evaluation=True)
        time_step = env.step([traiend_agent_output.action,random_agent_output.action])

      # de speler die start met de eerste step, is de speler 0 en is degene waarbij .rewards[0] overeenkomt.  
      # dus, wanneer player_pos = 1 is, dan start random agent met de eerste step, en dus is de rewards voor trained_agent , .rewards[1]
      if time_step.rewards[player_pos] > 0:
        wins[player_pos] += 1
      # zelf toegevoegd.
      else: 
        random_wins[player_pos] += 1
  print("trained agent win rate when starting: " , wins[0] / num_episodes,         " & trained agent win rate when second: " , wins[1] / num_episodes)
  print("random  agent win rate when starting: " , random_wins[0] / num_episodes,  " & random  agent win rate when second: " , random_wins[1] / num_episodes)
  return wins / num_episodes


def main(_):
    game = "matrix_pd"
    num_players = 2

    env = rl_environment.Environment(game)
    num_actions = env.action_spec()["num_actions"]
    
    wife    = BoltzmannQLearner(player_id=0, 
                                num_actions=num_actions,    
                                temperature_schedule=rl_tools.LinearSchedule(.3, 0.01, 1000))
    husband = BoltzmannQLearner(player_id=1, 
                                num_actions=num_actions,    
                                temperature_schedule=rl_tools.LinearSchedule(.3, 0.01, 1000))
    # random agents for evaluation
    random_agents = [
        random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
        for idx in range(num_players)
    ]

    # 1. Train the agents
    training_episodes = 10**5
    for cur_episode in range(training_episodes):
        if cur_episode % int(1e4) == 0:
            win_rates = eval_against_random_bots(env, [wife, husband], random_agents, 1000)
            logging.info("Starting episode %s, win_rates %s", cur_episode, win_rates)
        time_step = env.reset()
        while not time_step.last():
            wife_output = wife.step(time_step)
            husband_output = husband.step(time_step)
            
            time_step = env.step([wife_output.action,husband_output.action])

        wife.step(time_step)
        husband.step(time_step)

    print("")
    print(env.get_state)
    print(time_step.rewards)

    return

if __name__ == "__main__":
  app.run(main)