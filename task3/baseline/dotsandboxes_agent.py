"""
A RANDOM dotsandboxes_agent.py

the file must be called dotsandboxes_agent.py in order to use the tournament.py file. 
"""
import os
import sys
import argparse
import logging
import random
import numpy as np
import pyspiel
from open_spiel.python.algorithms import evaluate_bots

logger = logging.getLogger('be.kuleuven.cs.dtai.dotsandboxes')

package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_directory)

from open_spiel.python.algorithms import evaluate_bots
from ..dotsandboxes_agent.alphabeta_minimax import minimax_alphabeta_search 
from ..dotsandboxes_agent.transposition_table import TTable

# probeer eerst zonder sac te implementeren , check hoe goed het is in tournament. 
# en implementeer ook singleton, is denk ik ook belangerijk. (doubleton iets minder, dus da kun je ook weg doen.)
# zorg voor minimax!
# symmetrieen cache moet nog optimisaliseert zijn etc. 
# zorg dat shit werkt en dan MCTS. en dan ist gedaan, mss jdk bellen voor mogelijk feedback, 
# ma da moet dus af zijn voor het weekend.

# mss check eens https://github.com/yimmon/dots-and-boxes/blob/master/src/algorithm/alphabeta/alphabeta.go ? 
# met hulp van chatgpt? 

class Agent(pyspiel.Bot):
    """Agent template"""

    def __init__(self, player_id):
        """Initialize an agent to play Dots and Boxes.

        Note: This agent should make use of a pre-trained policy to enter
        the tournament. Initializing the agent should thus take no more than
        a few seconds.
        """
        pyspiel.Bot.__init__(self)
        self.player_id = player_id
        self.cache = TTable()
        self._actions_safe3s = []
        self._actions_unsafe3s = {
            "unsafe_actions": [],
            "safe_edge": []
        }
        self._actions_unsafe3s = {
            "unsafe_actions": [],
            "safe_edge": []
        }
        self._actions_halfhaerted = {
            "unsafe_actions": [], # unsafe3 box + takesallbut actions (+ take_all_endgame_moves) + outcount

        }

    def restart_at(self, state):
        """Starting a new game in the given state.

        :param state: The initial state of the game.
        """

        params = state.get_game().get_parameters()
        
        rows = params['num_rows']
        cols = params['num_cols']
        
        self.rows = rows
        self.cols = cols
        self.h_ = [[0] * cols for _ in range(rows + 1)]
        self.v_ = [[0] * (cols + 1) for _ in range(rows)]
        self.cells = [[0] * cols for _ in range(rows)]
        self.score = [0, 0]

    def inform_action(self, state, player_id, action):
        """Let the bot know of the other agent's actions.

        :param state: The current state of the game.
        :param player_id: The ID of the player that executed an action.
        :param action: The action which the player executed.
        """
        pass
       
    def step(self, state):
        
        action = self.try_safe3s()
        if action:
            return action
        
        action = self.try_unsafe3s()
        if action:
            return action

        action = self.try_halfhaerted()
        if action:
            return action

        action = self.safe_edge()
        if action:
            return action

        # If no specific strategies apply, use minimax search
        return self.make_any_move()

    def try_safe3s(self):
        self._actions_safe3s = self.safe3s()

        if self._actions_safe3s:
            return self._actions_safe3s.pop(0)
        return None

    def try_unsafe3s(self):
        self._actions_unsafe3s = self.unsafe3s()

        unsafe_actions = self._actions_unsafe3s["unsafe_actions"]
        safe_edge = self._actions_unsafe3s["safe_edge"]

        if unsafe_actions and safe_edge:
            action = unsafe_actions.pop(0)
            self._actions_unsafe3s["safe_edge"] = []
            self._actions_unsafe3s["unsafe_actions"] = []
            return action
        return None

# function sac(i,j) {     //sacrifices two squares if there are still 3's
#   count=0;
# 	loop=false;
# 	incount(0,i,j);
# 	if (!loop) takeallbut(i,j);
# 	if (count+score[0]+score[1]==m*n) {
# 		takeall3s()
# 	} else {
# 		if (loop) {
# 			count=count-2;
# 		}
# 		outcount(0,i,j);
# 		i=m;
# 		j=n
# 	}
# }

    def try_halfhaerted(self):
        self._actions_unsafe3s = self._()

        # u, v = sides3()
        # count = incount(0,u,v)
        return None

    def safe_edge(self):

        return None

    def make_any_move(self):
        """Make any move using minimax search."""
        # TODO: Implement the make any move strategy (minimax search)
        return None



    # def func0(self):
    #     safe3s = self._actions_safe3s
    #     if safe3s: 
    #         return safe3s.pop(0)
    #     else : 
    #         return None
    
    # def func1(self):
    #     unsafe_actions = self._actions_unsafe3s["unsafe_actions"]
    #     safe_edge = self._actions_unsafe3s["safe_edge"]

    #     if unsafe_actions and safe_edge:
    #         if unsafe_actions:
    #             return unsafe_actions.pop(0)
    #         else : 
    #             action = safe_edge.pop(0)
    #             self._actions_unsafe3s["safe_edge"] = []
    #             self._actions_unsafe3s["unsafe_actions"] = []
    #             return action
                
    # # TODO:
    # def func2(self):
    #     self._actions_halfhaerted = []
    #     return None

    # def safe3():
    #     pass

    # def unsafe3s():
    #     pass

    # def halfhaerted():
    #     pass

    # def safe_edge():
    #     pass