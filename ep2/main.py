from pyeda.inter  import *
from parser       import CTLtree
from functools    import reduce
from logic_helper import *
import re

# Lê entrada e remove espaços em branco
n      = int(input())
edges  = re.sub('[\s+]', '', input())
labels = re.sub('[\s+]', '', input())
tree   = CTLtree(input())
tgt    = re.sub('[\s+]', '', input())

# Lista ordenada das variaveis que ocorreram na entrada
variables = list(set(re.sub('[\[\]\(\)"]', '', labels).split(",")))
variables.sort()
# Transicoes de estados
edges  = edges[2:-2].split("),(")
# Conjunto de labels que sao verdadeiras em cada estado
labels = labels[2:-2].split("),(")
labels = list(map(lambda label: set(label[1:-1].split('","')), labels))
# Descricao do estado objetivo
tgt    = set(tgt[2:-2].split('","'))

x = bddvars('x', len(variables), 2)

# Lista de estados s e suas versoes s'
S  = []
pS = []
for label in labels:
    symbols = []
    prime_symbols = []
    for i in range(len(variables)):
        if(variables[i] in label):
            symbols.append(x[i,0])
            prime_symbols.append(x[i,1])
        else:
            symbols.append(~x[i,0])
            prime_symbols.append(~x[i,1])
    S.append(conjunction(symbols))
    pS.append(conjunction(prime_symbols))

# Representacao do modelo
model = []
for edge in edges:
    u, v = map(int, edge.split(","))
    model.append(S[u] & pS[v])
model = disjunction(model)

def sat_ex(tree):
	ans = set()
	B   = disjunction(list(map(lambda i: pS[i], sat(tree))))
	pre = exists(B & model, x)
	for i in range(n):
		if (S[i] & ~pre).is_zero():
			ans.add(i)
	return ans

def sat_af(tree):
	last = set(range(n))
	ans = sat(tree)
	while last != ans:
		last = set(ans)
		B   = disjunction(list(map(lambda i: ~pS[i], last)))
		pre = exists(B & model, x)
		for i in range(n):
			if not (S[i] & ~pre).is_zero():
				ans.add(i)
	return ans

def sat_eu(tree0, tree1):
	aux  = sat(tree0)
	last = set(range(n))
	ans  = sat(tree1)
	while last != ans:
		last = set(ans)
		B    = disjunction(list(map(lambda i: pS[i], last)))
		pre  = exists(B & model, x)
		for i in range(n):
			if(S[i] & ~pre).is_zero():
				ans.add(i)
	return ans

def sat(tree):
	ans = set()
	if tree.kind == "1": ans = set(range(n))
	elif tree.kind[0] == "x":
		sol = disjunction(S) & x[variables.index(tree.kind),0]
		for i in range(n):
			if (S[i] & ~sol).is_zero():
				ans.add(i)
	elif tree.kind == "-":  ans = set(range(n))-sat(tree.childs[0])
	elif tree.kind == "+":  ans = sat(tree.childs[0]) | sat(tree.childs[1])
	elif tree.kind == "*":  ans = sat(tree.childs[0]) & sat(tree.childs[1])
	elif tree.kind == "EX": ans = sat_ex(tree.childs[0])
	elif tree.kind == "EU": ans = sat_eu(tree.childs[0], tree.childs[1])
	elif tree.kind == "AF": ans = sat_af(tree.childs[0])
	return ans

ans = list(map(lambda i: labels[i], sat(tree)))
print(ans)
print(tgt in ans)
