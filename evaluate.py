# Copied from https://github.com/avalds/QisCoin/blob/master/evaluation.py
# Code after: https://colab.research.google.com/drive/1KoAQ1C_BNtGV3sVvZCnNZaER9rstmy0s#scrollTo=ygl_gVmV_QP7

import numpy as np

def evaluate_model(model, env, num_steps=1000, verbose = False):
	episode_rewards = [0.0]
	obs = env.reset()
	for i in range(num_steps):
		action, _ = model.predict(obs)
		#Need to take the first element in action, as sometimes it is a vector of length n.
		if(np.shape(action) != ()):
			action = action[0]
			if(verbose): print(action)
		obs, reward, done, _ = env.step(action)
		episode_rewards[-1] += reward
		if done:
			obs = env.reset()
			episode_rewards.append(0.0)
			if(verbose): print("vicory")

	mean_reward = round(np.mean(episode_rewards), 3)
	return mean_reward, len(episode_rewards)-1

def evaluate_random(env, num_steps=1000):
	episode_rewards = [0.0]
	obs = env.reset()
	for i in range(num_steps):
		obs, reward, done, _ = env.step(env.action_space.sample())
		episode_rewards[-1] += reward
		if done:
			obs = env.reset()
			episode_rewards.append(0.0)

	mean_reward = round(np.mean(episode_rewards), 3)
	return mean_reward, len(episode_rewards)-1
