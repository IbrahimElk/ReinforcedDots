"""
Tabular Q-Learner on Battle Of The Sexes.

Two Q-Learning agents are trained by playing against each other.
e-greedy , with epsilon = 0.2

After about 10**5 training episodes, the agents do NOT reach a good policy:
Win rate against random opponents is around 51% for player 0 and 50% for player 1.
"""

import logging
import sys
from absl import app
from absl import flags
import numpy as np

from open_spiel.python import rl_tools
from open_spiel.python import rl_environment
from open_spiel.python.algorithms import random_agent
from open_spiel.python.algorithms import tabular_qlearner

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
    game = "matrix_bos"
    num_players = 2

    env = rl_environment.Environment(game)
    num_actions = env.action_spec()["num_actions"]
    
    # als epsilon, quite laag is, bv. 0.2, dan zal het na een eindige aantal iteraties 
    # convergeren naar één van de twee Nash equilibirum pure strategien. 
    # bij self-play, dan idd goed, maar tegen random agents idd slecht zoals verwacht. (makes sense)
    wife    = tabular_qlearner.QLearner(player_id=0, 
                                num_actions=num_actions,    
                                epsilon_schedule=rl_tools.ConstantSchedule(0.2))
    husband = tabular_qlearner.QLearner(player_id=1, 
                                num_actions=num_actions,    
                                epsilon_schedule=rl_tools.ConstantSchedule(0.2))
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
        # print(wife._q_values.items())
        # print(husband._q_values.items())

    print("")
    print(env.get_state)
    print(time_step.rewards)

    #FIXME: HET ZOU LOGISCH ZIJN ALS WIN KANSEN 50% is, want je weet niet welke acties de andere agent doet, dus 
    # als je LW kiest, dan afh van de andere agent , kun je helemaal niets van reward ontvangen of maximaal. 
    # dus je kunt niet evalueren hoe goed je doet based only on the q values of your own actions. 
    return

if __name__ == "__main__":
  app.run(main)