from pyeda.inter  import *
from functools    import reduce
from parser       import CTLtree

def negation(list_of_literals):
	return list(map(lambda a: ~a, list_of_literals))

def conjunction(list_of_literals):
	return reduce(lambda a,b: a & b, list_of_literals)

def disjunction(list_of_literals):
	return reduce(lambda a,b: a | b, list_of_literals)

def exists(bdd, bdd_vars):
	ans = bdd
	n = len(bdd_vars)
	for i in range(n):
		ans = ans.restrict({bdd_vars[i,1] : 0}) | ans.restrict({bdd_vars[i,1] : 1})
	return ans
