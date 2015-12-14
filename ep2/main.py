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
tgt    = int(input())

# Lista ordenada das variaveis que ocorreram na entrada
variables = list(set(re.sub('[\[\]\(\)"]', '', labels).split(",")))
variables.sort()
# Transicoes de estados
edges  = edges[2:-2].split("),(")
# Conjunto de labels que sao verdadeiras em cada estado
labels = labels[2:-2].split("),(")
labels = list(map(lambda label: set(label[1:-1].split('","')), labels))

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
print(sat(S, tree))
