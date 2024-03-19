from open_spiel.python import rl_tools,rl_agent
from open_spiel.python.algorithms.boltzmann_tabular_qlearner import BoltzmannQLearner

import numpy as np

class LenientBoltzmannQLearner(BoltzmannQLearner):
    '''
    Subclass of BoltzmannQLearner that uses a lenient policy.
    '''
    
    # Use the same constructor as the parent class.
    def __init__(self, 
                 player_id, 
                 num_actions, 
                 step_size=0.1, 
                 discount_factor=1, 
                 temperature_schedule=rl_tools.ConstantSchedule(.5),
                 history_before_q=15, 
                 centralized=False):
        
        self._erm = {i:np.array([]) for i in range(num_actions)}
        self._history_before_q = history_before_q
        
        super().__init__(player_id, num_actions, step_size=step_size, discount_factor=discount_factor, temperature_schedule=temperature_schedule, centralized=centralized)

    # Override the function step() from the QLearner class by making a few changes in the provided implementation.
    def step(self, time_step, is_evaluation=False):
        if self._centralized:
            info_state = str(time_step.observations["info_state"])
        else:
            info_state = str(time_step.observations["info_state"][self._player_id])
        legal_actions = time_step.observations["legal_actions"][self._player_id]

        # Prevent undefined errors if this agent never plays until terminal step
        action,probs = None, None


        # Act step: don't act at terminal states.
        if not time_step.last():
            epsilon = 0.0 if is_evaluation else self._epsilon
            action, probs = self._get_action_probs(info_state, legal_actions, epsilon)

        # Learn step: don't learn during evaluation or at first agent steps.
        if self._prev_info_state and not is_evaluation:
            target = time_step.rewards[self._player_id]

            #######
            # APPLIED CHANGES: Put most recent reward in the experience replay memory (ERM).
            # The lenient policy is only executed when the ERM is large enough, in that case the maximum reward in the ERM is
            # used as the target instead of the average reward in normal Boltzmann Q-learning.
            #######
            self._erm[self._prev_action] = np.append(self._erm[self._prev_action], target)
            for action in self._erm:
                if self._erm[action].size >= self._history_before_q:

                    target = self._erm[action].max(initial=-np.inf)

                    prev_q_value = self._q_values[self._prev_info_state][action]
                    self._last_loss_value = target - prev_q_value
                    self._q_values[self._prev_info_state][action] += (self._step_size * self._last_loss_value)

                    self._erm[action] = np.array([])
            #######
            # END OF APPLIED CHANGES
            #######
                    
            
            if time_step.last():  # prepare for the next episode.
                self._prev_info_state = None
                return

        # Don't mess up with the state during evaluation.
        if not is_evaluation:
            self._prev_info_state = info_state
            self._prev_action = action
        
        return rl_agent.StepOutput(action=action, probs=probs)