from pyeda.inter import *
from functools import reduce

def isVal (i, j, n):
    if (i < 0 or i >= n):
        return False
    if (j < 0 or j >= n):
        return False
    return True

# lendo entrada
n,k = map(int, input().split())

# inicializando variáveis de expressão
X = exprvars('x', n, n)

# vetor de clauses
clauses = []

# montando a CNF
for i in range(n):
    # no mínimo 1 rainha por linha
    clauses.append(reduce(Or, [X[i][j] for j in range(n)]))

    # no mínimo 1 rainha por coluna
    clauses.append(reduce(Or,[X[j][i] for j in range(n)]))

    # no máximo 1 rainha por linha
    for j in range(n):
        clauses.append(reduce(Or,[Not(X[i][k]) for k in range(n) if j != k]))

    # no máximo 1 rainha por coluna
    for j in range(n):
        clauses.append(reduce(Or,[Not(X[k][i]) for k in range(n) if j != k]))

    # no máximo 1 rainha por diagonal (paralela à principal)
    for j in range(n):
        clauses.append(reduce(Or, [Not(X[i+k][j+k]) for k in range(-n,n) if k != 0 and isVal(i+k, j+k, n)]))

    # no máximo 1 rainha por diagonal (paralela à secundária)
    for j in range(n):
        clauses.append(reduce(Or,[Not(X[i+k][j-k]) for k in range(0,2*n) if k != 0 and isVal(i+k, j-k, n)]))

f = reduce(And,clauses)
print (clauses)
print (f.is_cnf())

f = expr2bdd(f)

# insatisfatível
if f.is_zero():
    print ("UNSAT")
else:
    print ("SAT")
