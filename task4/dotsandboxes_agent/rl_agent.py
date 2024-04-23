# There will be a need to design or learn features 
# describing states and actions that correlate with the quality
# of state-action pairs

# You can use implementations from OpenSpiel
# (DQN, policy gradient, MCTS, etc.) or develop your own. 

# you will have to think about features that can accurately 
# represent the game state and that allow for
# learning models that generalize well.

# TODO: welke features keizen zodat het chains herkent ??

# ge wilt dat u representatie van een game state van dots and boxes 
# to be a one-to-one mapping. 

# Ge wilt niet dat je een bepaalde state van de game op meerdere mogelijke manieren
# mogelijk representateerbaar is. 

# De tensor that is provided by open_spiel is sparse, and may not have the correct meaning
# of neigbors. If you use a CNN network in task4, the choice of representation is
# VERY important. because the tensor by open_spiel may not encode the concept of neigbors 
# very well, which CNN assumes about the input space. (this due to indexing of tensor by open_spiel) 

# it is HIGHLY encouraged to try and deploy a random agent first and see if everything works. 
# Try to first use a simple network, and choose a good representation. 
# progressevily increase the complexity of the network and plot the loss error over training time. 
# If by increasing the complexity of the model doesn't improve the agent performance, 
# it is higly likely it is due to the representation chosen.


# FIXME: 
# stappenplan: 
# beginnen met 2x2 game boards
# een goeie represnetatie kiezen. (verschillende soorten vinden en ze allemaal uittesten)
# probeer het model complexitiet te vergroten , wordt het beter? (op diezeflde groote game 2x2)
# indien niet, change representatie. 

# alle 3 beginnen aan task4. 
# (we gaan anders gwn niet klaar geraken, daarna laatste week, 1 iemand verder aan verslag.)

# dus MCTS en minimax moet klaar tegen volgend week. (anders geraken we er niet...)
# vergelijk model met minimax en MCTS op 2x2. 

# john: MCTS implementeren en de code implementeren voor het verslag van task4
# Staf: Minimax chains laten herkennen en afwerken, en task2 verbeteren. 
# Ibrahim: RL kant van task4 beetje beginnen. 

# volgende week :
# iedereen beginnen aan RL kant. 