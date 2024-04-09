"""
Chains are sequences of one or more capturable boxes ("corridors").

2 kinds of chains exist:
    1. half-open chains: only one end of chain is capturable. (= corridor with 3 edges filled in)
    2. closed chains: both ends of chain are capturable.      (= corridor with 4 edges filled in)

Most moves on a state with chains are suboptimal, using this knowledge can reduce the branching 
factor of the game tree.

Half-open chains, only 2 moves are part of a optimal strategy:
    1.  Capture every available box in that chain and make an additional move.
    2.  Capture all but 2 boxes in that chain and fill in the end of the chain.
        This creates a hard-hearted handout.

Closed chains, only 2 moves is part of a optimal strategy:
    1.  Capture every available box in that chain and make an additional move.
    2.  Capture all but 4 boxes in that chain and fill in the edge that separates it in 
        2 hard-hearted handouts.

More than 1 chain available:
    1. Fill all but 1 available chains, and follow the above mentioned strategies for the remaining
        chain. If possible choose half-open chain as the last one. (Sacrifices only 2 instead of 4)
"""
