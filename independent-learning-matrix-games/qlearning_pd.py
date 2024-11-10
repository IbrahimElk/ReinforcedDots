"""
Tabular Q-Learner on Prisonner's Dilemma.

Two Q-Learning agents are trained by playing against each other.
e-greedy , with epsilon = 0.2

After about 10**5 training episodes, the agents do NOT reach a good policy:
Win rate against random opponents is around 100% for player 0 and 50% for player 1.

# FIXME DOC: ANALOOG AAN BOS GAME, REDENERING KAN HIER OOK TOEGEPAST WORDEN WAAROM HET ZO SLECHT DOET. 
"""


import logging
import sys
from absl import app
from absl import flags
import numpy as np
import pyspiel 

from open_spiel.python import rl_tools
from open_spiel.python import rl_environment
from open_spiel.python.algorithms import random_agent
from open_spiel.python.algorithms import tabular_qlearner
import open_spiel.python.egt.utils as utils

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
    game = pyspiel.load_game(game)
    env = rl_environment.Environment(game)
    num_actions = env.action_spec()["num_actions"]
    
    temperature = 0.2
    agents =[ tabular_qlearner.QLearner(player_id=idx, 
                        num_actions=num_actions, 
                        epsilon_schedule=rl_tools.ConstantSchedule(temperature))
                for idx in range(num_players)]

    intial_q_values = [
        [{0: 0, 1: 0},{0: 0, 1: 0}],
        [{0: -1, 1: 0},{0: 1, 1: 0}], 
        [{0: 0, 1: -0.25}, {0: 0, 1: 0.75}], 
        [{0: 1, 1: 0.5},{0: 0, 1: 0}]]
    
    for i in range(num_players):
      agents[i]._q_values['[0.0]']  = intial_q_values[0][i]

    # random agents for evaluation
    random_agents = [
        random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
        for idx in range(num_players)
    ]

    # 1. Train the agents
    training_episodes = 25000
    for cur_episode in range(training_episodes):
        # if cur_episode % int(1e4) == 0:
        #     win_rates = eval_against_random_bots(env, [prisoner1, prisoner2], random_agents, 1000)
        #     logging.info("Starting episode %s, win_rates %s", cur_episode, win_rates)
        time_step = env.reset()
        while not time_step.last():
            prisoner1_output = agents[0].step(time_step)
            prisoner2_output = agents[1].step(time_step)
            
            time_step = env.step([prisoner1_output.action,prisoner2_output.action])

        agents[0].step(time_step)
        agents[1].step(time_step)

    print("")
    print(env.get_state)
    print(time_step.rewards)

    return

if __name__ == "__main__":
  app.run(main)