# Copied from https://github.com/avalds/QisCoin/blob/master/evaluation.py
# Code after: https://colab.research.google.com/drive/1KoAQ1C_BNtGV3sVvZCnNZaER9rstmy0s#scrollTo=ygl_gVmV_QP7

import numpy as np

def evaluate_model_nondeter(model, env, num_steps=1000):
	episode_rewards = [0.0]
	obs = env.reset()
	for i in range(num_steps):
		action, _states = model.predict(obs)
		if(isinstance(action, np.ndarray)):
			#print("action",action, type(action))
			#print("yo", action[0])
			obs, reward, done, _ = env.step(action[0])
		else:
			obs, reward, done, _ = env.step(action)

		episode_rewards[-1] += reward
		if done:
			obs = env.reset()
			episode_rewards.append(0.0)

	mean_reward = round(np.mean(episode_rewards), 3)
	median_reward = np.median(episode_rewards)
	return mean_reward, len(episode_rewards)-1, median_reward

def evaluate_model_deterministic(model, env, num_steps):
	episode_rewards = [0.0]
	obs = env.reset()
	for i in range(num_steps):
		action, _states = model.predict(obs, deterministic = True)
		obs, reward, done, _ = env.step(action)

		episode_rewards[-1] += reward
		if done:
			obs = env.reset()
			episode_rewards.append(0.0)

	mean_reward = round(np.mean(episode_rewards), 3)
	median_reward = np.median(episode_rewards)
	return mean_reward, len(episode_rewards)-1, median_reward

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

def plot_evaluation(model, env, num_steps):
	import matplotlib.pyplot as plt
	episode_rewards = [0.0]
	obs = env.reset()
	for i in range(num_steps):
		action, _states = model.predict(obs)
		if(isinstance(action, np.ndarray)):
			#print("action",action, type(action))
			#print("yo", action[0])
			obs, reward, done, _ = env.step(action[0])
		else:
			obs, reward, done, _ = env.step(action)

		episode_rewards[-1] += reward
		if done:
			obs = env.reset()
			episode_rewards.append(0.0)

	print(episode_rewards)
	plt.plot(episode_rewards)
