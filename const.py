import generate_actions

# Datatypes: integer values, array of datatypes, prob of datatypes, number of datatypes
t_int = 0
t_string = 1
t_datetime = 2
types = [t_int,t_string,t_datetime]
types_prob = [0.65,0.25,0.1]
n_types = 3

# Actions
actions = generate_actions.generate_actions()
