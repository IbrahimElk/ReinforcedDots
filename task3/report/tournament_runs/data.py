import pandas as pd

# Load the dataset from CSV into a DataFrame
df = pd.read_csv("ec_0_en_emd_1_file4_multiplicative.csv")

# Filter the dataframe based on the conditions
agent1_obtained_negative1 = df[(df['agent_p1'] == 0) & (df['return_p1'] == -1)]
agent1_obtained_positive1 = df[(df['agent_p1'] == 0) & (df['return_p1'] ==  1)]

agent2_obtained_negative1 = df[(df['agent_p2'] == 0) & (df['return_p2'] == -1)]
agent2_obtained_positive1 = df[(df['agent_p2'] == 0) & (df['return_p2'] ==  1)]

# Count the occurrences
agent1_count_neg = len(agent1_obtained_negative1)
agent2_count_neg = len(agent2_obtained_negative1)

agent1_count_pos = len(agent1_obtained_positive1)
agent2_count_pos = len(agent2_obtained_positive1)

ec_count_won = agent2_count_pos + agent1_count_pos
ec_count_lost = agent2_count_neg + agent1_count_neg

print("Number of times eval_function_chain agent won : ", ec_count_won)
print("Number of times eval_function_chain agent lost : ", ec_count_lost)

# Filter the dataframe based on the conditions
agent1_obtained_negative1 = df[(df['agent_p1'] == 1) & (df['return_p1'] == -1)]
agent1_obtained_positive1 = df[(df['agent_p1'] == 1) & (df['return_p1'] ==  1)]

agent2_obtained_negative1 = df[(df['agent_p2'] == 1) & (df['return_p2'] == -1)]
agent2_obtained_positive1 = df[(df['agent_p2'] == 1) & (df['return_p2'] ==  1)]

# Count the occurrences
agent1_count_neg = len(agent1_obtained_negative1)
agent2_count_neg = len(agent2_obtained_negative1)

agent1_count_pos = len(agent1_obtained_positive1)
agent2_count_pos = len(agent2_obtained_positive1)

emd_count_won = agent2_count_pos + agent1_count_pos
emd_count_lost = agent2_count_neg + agent1_count_neg

print("Number of times eval_function_maximum_difference agent won : ", emd_count_won)
print("Number of times eval_function_maximum_difference agent lost : ", emd_count_lost)

# TODO: 
# dit met heuristiek + 1 voor chains, dus niet veel effect, probeer andere methode
# mss multiplicatieve effect, of grotere additieve effect van -50 en 50 bv. 

# FIXME: 
# zorg voor dat eval_function_chain onder de 200ms zit, want wordt nu niet aan voldaan!.

# ec_0_en_emd_1
# Number of times eval_function_chain agent won :  70
# Number of times eval_function_chain agent lost :  130
# Number of times eval_function_maximum_difference agent won :  130
# Number of times eval_function_maximum_difference agent lost :  70


# ec_0_en_emd_1_file3
# (venv) ➜  tournament_runs (task3/chains) python3 data.py                                                                                                          ✭ ✱
# Number of times eval_function_chain agent won :  57
# Number of times eval_function_chain agent lost :  143
# Number of times eval_function_maximum_difference agent won :  143
# Number of times eval_function_maximum_difference agent lost :  57


# ec_0_en_emd_1_file4 (multiplicative) 
# (venv) ➜  tournament_runs (task3/chains) python3 data.py                                                                                                          ✭ ✱
# Number of times eval_function_chain agent won :  72
# Number of times eval_function_chain agent lost :  128
# Number of times eval_function_maximum_difference agent won :  128
# Number of times eval_function_maximum_difference agent lost :  72
# (venv) ➜  tournament_runs (task3/chains)                             
