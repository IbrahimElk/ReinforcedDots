import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset from CSV into a DataFrame
df = pd.read_csv("agent_vs_mcts.csv")
# df = pd.read_csv("agent_vs_random.csv")
# df = pd.read_csv("agent_vs_first_edge.csv")
# df = pd.read_csv("agent_vs_agent.csv")

# for example , for one df: 
agent1_obtained_negative1 = df[(df['agent_p1'] == "my_agent") & (df['return_p1'] == -1)]
agent1_obtained_positive1 = df[(df['agent_p1'] == "my_agent") & (df['return_p1'] ==  1)]
agent2_obtained_negative1 = df[(df['agent_p2'] == "my_agent") & (df['return_p2'] == -1)]
agent2_obtained_positive1 = df[(df['agent_p2'] == "my_agent") & (df['return_p2'] ==  1)]

agent1_count_neg = len(agent1_obtained_negative1)
agent2_count_neg = len(agent2_obtained_negative1)
agent1_count_pos = len(agent1_obtained_positive1)
agent2_count_pos = len(agent2_obtained_positive1)

ec_count_won = agent2_count_pos + agent1_count_pos
ec_count_lost = agent2_count_neg + agent1_count_neg

print("Number of times my_agent agent won : ", ec_count_won)
print("Number of times my_agent agent lost : ", ec_count_lost)

agent1_obtained_negative1 = df[(df['agent_p1'] == "baseline") & (df['return_p1'] == -1)]
agent1_obtained_positive1 = df[(df['agent_p1'] == "baseline") & (df['return_p1'] ==  1)]
agent2_obtained_negative1 = df[(df['agent_p2'] == "baseline") & (df['return_p2'] == -1)]
agent2_obtained_positive1 = df[(df['agent_p2'] == "baseline") & (df['return_p2'] ==  1)]

agent1_count_neg = len(agent1_obtained_negative1)
agent2_count_neg = len(agent2_obtained_negative1)
agent1_count_pos = len(agent1_obtained_positive1)
agent2_count_pos = len(agent2_obtained_positive1)

ec_count_won = agent2_count_pos + agent1_count_pos
ec_count_lost = agent2_count_neg + agent1_count_neg

print("Number of times first_open_edge agent won : ", ec_count_won)
print("Number of times first_open_edge agent lost : ", ec_count_lost)
