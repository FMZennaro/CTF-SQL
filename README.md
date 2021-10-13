# CTF-SQL
Modelling SQL Injection Using Reinforcement Learning

### Requirements
The following code requires *numpy, scipy, matplotlib* and [OpenAI gym](https://github.com/openai/gym); [stable-baselines3](https://stable-baselines3.readthedocs.io/en/master/) (together with [pytorch](https://pytorch.org/)) is used to train reinforcement learning agents.

**Warning:** Simulation1 and Simulation2 rely at the moment on synthetic SQL server simulators. Simulation1 uses the module *mockSQLenv.py*. Simulation2 uses the OpenAI gym environment [gym-CTF-SQL](https://github.com/avalds/gym-CTF-SQL) (check the gym repository for installing and running the environment)

### Content
The project *CTF-SQL* contains the simulations running reinforcement agent on a CTF challenge containing a simple SQL injection vulnerability. Every *SimulationX* file contains a simulation, including training and analysis.
- *Simulation1* runs a tabular Q-learning agent;
- *Simulation2* runs a deep Q-learning agent (with different batch settings).
Details about the setup and the interpretation may be found in [1].

### References

\[1\] Erdodi, L., Sommervoll, A.A. and Zennaro, F.M., 2020. Simulating SQL Injection Vulnerability Exploitation Using Q-Learning Reinforcement Learning Agents. arXiv preprint.