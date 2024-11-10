import pyspiel

from open_spiel.python.algorithms import tabular_qlearner
from open_spiel.python import rl_environment


# Subsidy game is a non-zero-sum coordination matrix game.

# Initialize the environment
game = pyspiel.create_matrix_game("subsidy_game", "Subsidy Game", ["S1","S2"], ["S1","S2"], [[12,0], [11,10]], [[12,11], [0,10]])
env = rl_environment.Environment(game)
num_players = env.num_players
num_actions = env.action_spec()["num_actions"]
EPISODES = 25000

# Create the agents
agents =[
    tabular_qlearner.QLearner(player_id=idx, num_actions=num_actions)
    for idx in range(num_players)
]

# Train the Q-learning agents in self-play, commented parts are for graphical visualization of the learning process
#state_hist = []

for cur_episode in range(EPISODES):
    if cur_episode % 1000 == 0:
        print(f'Episodes: {cur_episode}')
    time_step = env.reset()
    while not time_step.last():
        agent_outputs = [agent.step(time_step) for agent in agents]
        #state_hist.append([agent_output.probs for agent_output in agent_outputs])
        time_step = env.step([agent_output.action for agent_output in agent_outputs])
    for agent in agents:
        agent.step(time_step)

print("Training done!")


# Evaluation of the agents
time_step = env.reset()
while not time_step.last():
    print("")
    print(env.get_state)
    agent_actions = [agent.step(time_step, is_evaluation=True).action for agent in agents]
    print(agent_actions)

    actions = []
    agent = 0
    for action in agent_actions:
        actions.append(env.get_state.action_to_string(agent, action))
        agent += 1
    
    actionstr = str(actions)

    print(f'Players chose {actionstr}')
    time_step = env.step([agent_output.action for agent_output in agent_outputs])

print("")
print(env.get_state)
print(time_step.rewards)

