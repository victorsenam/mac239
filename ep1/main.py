## EP1 - MAC0329
# Nathan Benedetto Proença - 8941276
# Victor Sena Molero - 8941317


from pyeda.inter import *
from functools import reduce
from itertools import combinations

n, k = map(int, input().split())

x   = exprvars('grid', n, n)
sol =  bddvars('grid', n, n)
diagonals = []
clauses   = []

# calculando diagonais
for i in range(-n,n):
    main_diagonal = []
    for j in range(n):
        if( 0 <= i+j and i+j<n ):
            main_diagonal.append([i+j,j])
    if( len(main_diagonal) > 1):
        diagonals.append(main_diagonal)
for i in range(0,2*n):
    anti_diagonal = []
    for j in range(n):
        if( 0 <= i-j and i-j < n ):
            anti_diagonal.append([i-j,j])
    if( len(anti_diagonal) > 1 ):
        diagonals.append(anti_diagonal)

for i in range(n):
# no mínimo uma rainha em cada linha
    clauses.append(reduce(Or, [x[i][j] for j in range(n)]))
# no máximo uma rainha em cada linha
    for ii, ij in combinations(range(n),2):
        clauses.append(Or(Not(x[i][ii]), Not(x[i][ij])))

for j in range(n):
# no mínimo uma rainha em cada coluna
    clauses.append(reduce(Or, [x[i][j] for i in range(n)]))
# no máximo uma rainha em cada coluna
    for ii, ij in combinations(range(n),2):
        clauses.append(Or(Not(x[ii][j]), Not(x[ij][j])))

# no máximo uma rainha por diagonal
for diagonal in diagonals:
    for posi, posj in combinations(diagonal, 2):
        clauses.append(Or(Not(x[posi[0]][posi[1]]),Not(x[posj[0]][posj[1]])))

# rainhas já colocadas no tabuleiro
for i in range(k):
    ii, ij = map(int, input().split())
    clauses.append(x[ii][ij])

# gerando a CNF com todas as clauses já criadas
f = reduce(And, clauses)

# gerando o ROBDD com a CNF
tree = expr2bdd(f)

if tree.is_zero():
    print("UNSAT")
else:
    print("SAT")
    chosen_in = tree.satisfy_one()
    for i in range(n):
        line = ""
        for j in range(n):
            if ( chosen_in[sol[i,j]] ):
                line += ' Q '
            else:
                line += ' . '
        print(line)

