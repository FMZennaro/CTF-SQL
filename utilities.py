from itertools import chain, combinations

def powerset(iterable):
	#based on: https://stackoverflow.com/questions/18035595/powersets-in-python-using-itertools
	"powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
	s = list(iterable)
	return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))


def getdictshape(d):
	return (len(d.keys()), d[()].shape)


if __name__ == "__main__":
	x = powerset([0,1,2,3,4,5])
	print(x)
	print(len(x))
