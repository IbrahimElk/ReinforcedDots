import logging
from open_spiel.python import rl_environment
from open_spiel.python.algorithms import random_agent
from open_spiel.python.algorithms import tabular_qlearner
import numpy as np
from absl import app

def eval_against_random_bots(env, trained_agents, random_agents, num_episodes):
  """Evaluates `trained_agents` against `random_agents` for `num_episodes`."""
  wins = np.zeros(2)
  for player_pos in range(2):
    if player_pos == 0:
      cur_agents = [trained_agents[0], random_agents[1]]
    else:
      cur_agents = [random_agents[0], trained_agents[1]]
    for _ in range(num_episodes):
      time_step = env.reset()
      while not time_step.last():
        trained_agent_output = cur_agents[player_pos].step(time_step, is_evaluation=True)
        random_agent_output = cur_agents[1-player_pos].step(time_step, is_evaluation=True)
        time_step = env.step([trained_agent_output.action,random_agent_output.action])

      
      if time_step.rewards[player_pos] > 0:
        wins[player_pos] += 1

  return wins / num_episodes

def main(_):

    game = "matrix_brps"
    num_players = 2
    
    env = rl_environment.Environment(game)
    num_actions = env.action_spec()["num_actions"]

    player1 = tabular_qlearner.QLearner(player_id=0, num_actions=num_actions)
    player2 = tabular_qlearner.QLearner(player_id=1, num_actions=num_actions)

    random_agents = [
      random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
      for idx in range(num_players)
    ]

    episodes = 10**5
    for cur_episode in range(episodes):
        if cur_episode % int(1e4) == 0:
            win_rates = eval_against_random_bots(env, [player1, player2], random_agents, 1000)
            logging.info("Starting episode %s, win_rates %s", cur_episode, win_rates)
        time_step = env.reset()
        while not time_step.last():
            player1_output = player1.step(time_step)
            player2_output = player2.step(time_step)

            time_step = env.step([player1_output.action, player2_output.action])

        player1.step(time_step)
        player2.step(time_step)
    
    print("")
    print(env.get_state)
    print(time_step.rewards)

    return

if __name__ == "__main__":
  app.run(main)