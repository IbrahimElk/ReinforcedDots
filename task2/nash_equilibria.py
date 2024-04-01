import pyspiel
import numpy as np
from open_spiel.python import policy
from open_spiel.python.mfg.algorithms import nash_conv
import nashpy as nash

# Subsidy Game
subsidy_game = nash.Game([[12, 0], [11, 10]], [[12, 11], [0, 10]])
subsidy_equilibria = subsidy_game.support_enumeration()
print("Nash Equilibria for Subsidy Game:")
for eq in subsidy_equilibria:
    print(eq)

# Biased Rock, Paper, Scissors
biased_rps_game = nash.Game([[0, -0.05, 0.25], [0.05, 0, -0.5], [-0.25, 0.5, 0]],
                            [[0, 0.05, -0.25], [-0.05, 0, 0.5], [0.25, -0.5, 0]])
biased_rps_equilibria = biased_rps_game.support_enumeration()
print("\nNash Equilibria for Biased Rock, Paper, Scissors:")
for eq in biased_rps_equilibria:
    print(eq)

# Battle of the Sexes
battle_of_sexes_game = nash.Game([[3, 0], [0, 2]], [[2, 0], [0, 3]])
battle_of_sexes_equilibria = battle_of_sexes_game.support_enumeration()
print("\nNash Equilibria for Battle of the Sexes:")
for eq in battle_of_sexes_equilibria:
    print(eq)

# Prisoner's Dilemma
prisoners_dilemma_game = nash.Game([[-1, -4], [0, -3]], [[-1, 0], [-4, -3]])
prisoners_dilemma_equilibria = prisoners_dilemma_game.support_enumeration()
print("\nNash Equilibria for Prisoner's Dilemma:")
for eq in prisoners_dilemma_equilibria:
    print(eq)