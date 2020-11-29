import numpy as np
import mockSQLenv as srv
import const
import sys

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
		print(2**self.num_expl_actions, self.num_expl_actions)
		self.Q = np.ones((2**self.num_esc_expl_actions, self.num_actions))

		self.verbose = verbose

	def set_learning_options(self,exploration=0.2,learningrate=0.1,discount=0.9):
		self.expl = exploration
		self.lr = learningrate
		self.discount = discount

	def _select_action(self):
		if (np.random.random() < self.expl):
			np.random.randint(0,self.num_actions)
		else:
			return np.argmax(self.Q[self.state,:])


	def step(self):
		self.steps = self.steps + 1

		action = self._select_action()

		state_resp, reward, termination, debug_msg = self.env.step(action)

		self._analyze_response(action, state_resp, reward)
		self.terminated = termination
		if(self.verbose): print(s)

		return




	def _analyze_response(self, action, response, reward):
		expl1 = 1 	# SOMETHING
		expl2 = 2 	# SOMETHING, but maybe should be nothing
		flag  = 3 	#FLAG
		expl3 = 4 	#SOMETHING
		wrong1 = 0 	#NOTHING
		wrong2 = -1 #NOTHING

		#The agent recieves SOMETHING as the response
		if(response==exp1 or response == expl2):
			self.state = 2*(action // 17) + (action % 17)
			self._update_Q(self.state, self.state, action, reward)
		#SOMETHING
		elif(response == expl3):
			self._update_Q(self.state, self.state, action, reward)

		elif(response==wrong1 or response == wrong2):
			self._update_Q(self.state, self.state, action, reward)

		elif(command==flag):
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


	def run_episode(self):
		_,_,self.terminated,s = self.env.reset()
		if(self.verbose): print(s)

		while not(self.terminated):
			self.step()


if __name__ == "__main__":
	a = Agent(const.actions)
