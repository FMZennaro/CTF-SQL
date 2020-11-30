import numpy as np
import mockSQLenv as srv
import const
import sys
import utilities as ut

"""
agent.py is based on FMZennaro's agent on https://github.com/FMZennaro/CTF-RL/blob/master/Simulation1/agent.py
"""



class Agent():
	def __init__(self, actions, verbose=True):
		self.actions = actions
		#All the exploratory actions
		self.expl_actions = list(filter(lambda x: "flag" not in x, self.actions))
		#All the escape exploratory actions
		self.esc_expl_actions = list(filter(lambda x: "union" not in x, self.actions))


		self.num_actions = len(actions)
		self.num_expl_actions = len(self.expl_actions)
		self.num_esc_expl_actions = len(self.esc_expl_actions)

		"""
		We let the first index be the state and the second index be the action
		"""
		#print(2**self.num_expl_actions, self.num_expl_actions)
		self.Q = np.ones((2**self.num_esc_expl_actions, self.num_actions))

		self.verbose = verbose
		self.set_learning_options()
		self.used_actions = []
		self.used_esc_expl_actions_with_response = set([])
		self.powerset = None

	def set_learning_options(self,exploration=0.2,learningrate=0.1,discount=0.9):
		self.expl = exploration
		self.lr = learningrate
		self.discount = discount

	def _select_action(self):
		if (np.random.random() < self.expl):
			return np.random.randint(0,self.num_actions)
		else:
			return np.argmax(self.Q[self.state,:])


	def step(self):
		self.steps = self.steps + 1

		action = self._select_action()
		self.used_actions.append(action)

		state_resp, reward, termination, debug_msg = self.env.step(action)

		self._analyze_response(action, state_resp, reward)
		self.terminated = termination
		if(self.verbose): print(debug_msg)

		return


	def _calculate_next_state(self):
		if(self.powerset is None):
			self.powerset = ut.powerset(list(range(self.num_esc_expl_actions)))

		x = list(self.used_esc_expl_actions_with_response)
		x.sort()
		x = tuple(x)
		new_state = self.powerset.index(x)

		return new_state


	def _analyze_response(self, action, response, reward):
		expl1 = 1 	# SOMETHING
		expl2 = 2 	# SOMETHING, but maybe should be nothing
		flag  = 3 	#FLAG
		expl3 = 4 	#NOTHING
		wrong1 = 0 	#NOTHING
		wrong2 = -1 #NOTHING

		escape_action = False

		action_str = const.actions[action]
		if(action_str in self.esc_expl_actions):
			escape_action = True
			#We add 1 since we start in state 0 and it makes more sense to go up from there
			action_index = self.esc_expl_actions.index(action_str)

		#The agent recieves SOMETHING as the response
		if(response==expl1 or response == expl2):
			self.used_esc_expl_actions_with_response.add(action_index)
			self.state = self._calculate_next_state()
			self._update_Q(self.state, self.state, action, reward)
		#SOMETHING
		elif(response == expl3):
			self._update_Q(self.state, self.state, action, reward)

		elif(response==wrong1 or response == wrong2):
			self._update_Q(self.state, self.state, action, reward)

		elif(response==flag):
			self._update_Q(self.state,self.state,action,reward)
		else:
			print("ILLEGAL RESPONSE")
			sys.exit()

	def _update_Q(self, oldstate, newstate, action, reward):
		best_action_newstate = np.argmax(self.Q[newstate,:])
		self.Q[oldstate,action] = self.Q[oldstate,action] + self.lr * (reward + self.discount*self.Q[newstate, best_action_newstate] - self.Q[oldstate, action])

	def reset(self,env):
		self.env = env
		self.terminated = False
		self.state = 0
		self.steps = 0
		self.used_esc_expl_actions_with_response = set([])
		self.used_actions = []


	def run_episode(self):
		_,_,self.terminated,s = self.env.reset()
		if(self.verbose): print(s)

		while not(self.terminated):
			self.step()


if __name__ == "__main__":
	a = Agent(const.actions)
	env = srv.mockSQLenv()
	a.reset(env)
	a.run_episode()
	#a.step()
