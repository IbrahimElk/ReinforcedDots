from open_spiel.python import rl_agent,rl_tools, rl_environment
from open_spiel.python.algorithms import tabular_qlearner
import collections
import numpy as np
import pyspiel

class LenientBoltzmannQLearner(tabular_qlearner.QLearner):
	def __init__(self,
		player_id,
		num_actions,
		step_size=0.1,
		discount_factor=1.0,
		temperature_schedule=rl_tools.ConstantSchedule(.5),
		centralized=False,
		kappa=10):	  

		super().__init__(
			player_id,
			num_actions,
			step_size=step_size,
			discount_factor=discount_factor,
			epsilon_schedule=temperature_schedule,
			centralized=centralized)
		
		self._history = collections.defaultdict(list)
		self._prev_action = None
		self._kappa = kappa

	def _softmax(self, info_state, legal_actions, temperature):
		"""Action selection based on boltzmann probability interpretation of Q-values.

		For more details, see equation (2) page 2 in
		https://arxiv.org/pdf/1109.1528.pdf

		Args:
			info_state: hashable representation of the information state.
			legal_actions: list of actions at `info_state`.
			temperature: temperature used for softmax.

		Returns:
			A valid soft-max selected action and valid action probabilities.
		"""
		
		probs = np.zeros(self._num_actions)
		if temperature > 0.0:
			probs += [
				np.exp((1 / temperature) * self._q_values[info_state][i])
				for i in range(self._num_actions)
			]
			probs /= np.sum(probs)
		else:
			# Temperature = 0 causes normal greedy action selection
			greedy_q = max([self._q_values[info_state][a] for a in legal_actions])
			greedy_actions = [
				a for a in legal_actions if self._q_values[info_state][a] == greedy_q
			]

			probs[greedy_actions] += 1 / len(greedy_actions)

		action = np.random.choice(range(self._num_actions), p=probs)
		return action, probs

	def _get_action_probs(self, info_state, legal_actions, epsilon):
		"""Returns a selected action and the probabilities of legal actions."""
		return self._softmax(info_state, legal_actions, temperature=epsilon)

		
	def step(self, time_step, is_evaluation=False):
		"""Returns the action to be taken and updates the Q-values if needed.

    	Args:
		time_step: an instance of rl_environment.TimeStep.
		is_evaluation: bool, whether this is a training or evaluation call.

		Returns:
		A `rl_agent.StepOutput` containing the action probs and chosen action.
		"""
		if self._centralized:
			info_state = str(time_step.observations["info_state"])
		else:
			info_state = str(time_step.observations["info_state"][self._player_id])
		legal_actions = time_step.observations["legal_actions"][self._player_id]
		# Prevent undefined errors if this agent never plays until terminal step
		action, probs = None, None

		# Act step: don't act at terminal states.
		if not time_step.last():
			epsilon = 0.0 if is_evaluation else self._epsilon
			action, probs = self._get_action_probs(info_state, legal_actions, epsilon)

    	# Learn step: don't learn during evaluation or at first agent steps.
		if self._prev_info_state and not is_evaluation:
			target = time_step.rewards[self._player_id]

# --------------------------------------------------------------------------------------------- 
# begin 
			history_rewards_length = len(self._history[self._prev_action])
			if history_rewards_length < self._kappa: 
				self._history[self._prev_action].append(target)
			else: 
				target = max(self._history[self._prev_action])

				# delete previous rewards from the buffer 
				self._history[self._prev_action] = []

				if not time_step.last():  # Q values are zero for terminal.
					# een deel van de Q FORMULA:
					# Q(s,a) = Q(s,a) + α * (r + γ * max(Q(s',a')) - Q(s,a))
					# HIER: γ * max(Q(s',a'))
					target += self._discount_factor * max([self._q_values[info_state][a] for a in legal_actions])

				prev_q_value = self._q_values[self._prev_info_state][self._prev_action]
					# γ * max(Q(s',a')) - Q(s,a)
				self._last_loss_value = target - prev_q_value
					# Q(s,a) + α * (r + γ * max(Q(s',a')) - Q(s,a))
				self._q_values[self._prev_info_state][self._prev_action] += (self._step_size * self._last_loss_value)
					
					# Decay epsilon, if necessary.
					# α lager laten worden voor convergentie denk iK. 
				self._epsilon = self._epsilon_schedule.step()
					
			if time_step.last():  # prepare for the next episode.
				self._prev_info_state = None
				return
# einde
# --------------------------------------------------------------------------------------------- 
						
		# Don't mess up with the state during evaluation.
		if not is_evaluation:
			self._prev_info_state = info_state
			self._prev_action = action
		return rl_agent.StepOutput(action=action, probs=probs)
	

if __name__ == "__main__":
	# NADEEL VAN LENIENCY, DUURT LANG... moet telkens kappa steps wachten voordat de q values zullen veranderne. 
	# kan mogelijk verlaagt worden door linearschedule te hebben van kappa ipv constant. 


	# A simpler approach is to have the agent collect κ rewards for
	# a single action before it updates the value of this action based on the highest of those κ rewards [8]. This
	# results in a fixed degree of leniency, expressed by the value of κ
	num_players = 2
	game = pyspiel.create_matrix_game("subsidy_game", "Subsidy Game", ["S1","S2"], ["S1","S2"], [[12,0], [11,10]], [[12,11], [0,10]])
	
	env = rl_environment.Environment(game)
	num_actions = env.action_spec()["num_actions"]
	Kappa = 15 
	wife    = LenientBoltzmannQLearner(	player_id=0,
										num_actions=num_actions,    
										temperature_schedule=rl_tools.ConstantSchedule(1),
										kappa=Kappa)
	husband = LenientBoltzmannQLearner(	player_id=1, 
										num_actions=num_actions,    
										temperature_schedule=rl_tools.ConstantSchedule(1),
										kappa=Kappa)

	# 1. Train the agents
	training_episodes = 25000
	# FIXME: wrm is het zo slecht als met willekeurige kappa ????
	# het is zo dat bepaalde acties enkel rewards "12" bevatten en dus de max zou die nemen....

	# aight blijkbaar als temperature 1 is, dan groter kans op 12???
	# FIXME: mss de agent laten runnen voor meerere keren voor verschillende waarden van temperature ? 
	# (kappa, is denk ik genoeg , puur op intuitie.)

	for cur_episode in range(training_episodes):
			if cur_episode % int(1e4) == 0:
				print("Starting episode: ", cur_episode)
			time_step = env.reset()
			while not time_step.last():
					wife_output = wife.step(time_step)
					husband_output = husband.step(time_step)
					time_step = env.step([wife_output.action,husband_output.action])

			wife.step(time_step)
			husband.step(time_step)

	print("")
	print(env.get_state)
	print(time_step.rewards)
