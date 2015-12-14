# Classe CTLtree com a estrutura em árvore de fórmulas CTL

# A variável "kind" é o a operação da fórmula, podendo ser "+", "*", "-", 
# "AU","EU","AG","EG","AX","EX","AF","EF", "xN" (onde N é um natural), "0", ou "1"
# No caso de "kind" ser uma operação, "childs" é uma lista ordenada com as subárvores 
# correspondentes as operandos, por exemplo +(f1)(f2) se torna uma CTLtree com kind = "+"
# e childs= [CTLtree(f1),CTLtree(f2)]

class CTLtree():
	def __init__(self,str):
		kind, childs = CTLtree.parse(str)
		self.kind = kind
		self.childs = childs

#função que mostra o começo de cada subárvore na fórmulas, mas pouco visual
#	def __str__(self):
#		answer = "CTL_Tree: " + self.kind
#		for c in self.childs:
#			answer += "(" + str(c)+ ")"
#		return answer
			
#função que devolve a fórmula no modo string comum
	def __str__(self):
		answer = self.kind
		if len(self.childs)==2:
			answer += "(" + str(self.childs[0])+ ")(" + str(self.childs[1])+ ")"
		elif len(self.childs)==1:
			answer += str(self.childs[0])
		return answer

	def bemFormada(formula):
		parenteses = 0
		for c in formula:
			if c == '(':
				parenteses +=1
			if c == ')':
				parenteses -=1
			if parenteses <0:
				return False
		return parenteses == 0

	def separa(formula):
		parenteses = 0
		for i in range(len(formula)):
			if formula[i] == '(':
				parenteses +=1
			if formula[i] == ')':
				parenteses -=1
			if parenteses == 0:
				return i+1
		return -1

	
# Esse é a função que recebe uma fórmula CTL e converte na estrutura de árvore
	def parse(formula):
#		print(formula)
		if not CTLtree.bemFormada(formula):
			print("Formula mal formada para parse:",formula)
		formula = formula.strip()
		c = formula[0]
		l=1
		if c == "A" or c == "E":
			c += formula[1]
			l=2	

		if c == "+" or c == "*" or c == "AU" or c == "EU":
			kind = c
			if formula[l] != "(":
				print("Operador Binario sem parenteses (adjacente)")
			quebra = CTLtree.separa(formula[l:])

#			print(formula, l, quebra)
			c1 = CTLtree(formula[l+1:l+quebra-1])
			c2 = CTLtree(formula[l+quebra+1:-1])
			return kind,[c1,c2]

		if c == "-" or c == "EX" or c == "AX" or c == "EF" or c == "AF" or c == "EG" or c =="AG":
			kind = c
			c1 = CTLtree(formula[l:])
			return kind,[c1]

		if c == "0" or c == "1":
			return c,[]

		return formula,[]

#Função exemplo de teste para a classe CTLtree
def test():
	print("Testando parser CTL:")
	print("Arvore CTL para a expressão:1     " + str(CTLtree("1")))
	print("Arvore CTL para a expressão:0     " + str(CTLtree("0")))
	print("Arvore CTL para a expressão:x1     " + str(CTLtree("x1")))
	print("Arvore CTL para a expressão:+(x1)(x2)     " + str(CTLtree("+(x1)(x2)")))
	print("Arvore CTL para a expressão:*(x1)(x2)     " + str(CTLtree("*(x1)(x2)")))
	print("Arvore CTL para a expressão:-x1     " + str(CTLtree("-x1")))
	print("Arvore CTL para a expressão:EX x1     " + str(CTLtree("EX x1")))
	print("Arvore CTL para a expressão:AX x1     " + str(CTLtree("AX x1")))
	print("Arvore CTL para a expressão:EF x2     " + str(CTLtree("EF x2")))
	print("Arvore CTL para a expressão:AF x2     " + str(CTLtree("AF x2")))
	print("Arvore CTL para a expressão:EG x3     " + str(CTLtree("EG x3")))
	print("Arvore CTL para a expressão:AG x3     " + str(CTLtree("AG x3")))
	print("Arvore CTL para a expressão:EU(x4)(x5)     " + str(CTLtree("EU(x4)(x5)")))
	print("Arvore CTL para a expressão:AU(x4)(x5)     " + str(CTLtree("AU(x4)(x5)")))
	
	print("Arvore CTL para a expressão:AU(AU(EX 1)(x1))(EU(x2)(0))     " + str(CTLtree("AU(AU(EX 1)(x1))(EU(x2)(0))")))
	print("Arvore CTL para a expressão:+(AX EG x1)( - +(x1)(AG x2) )     " + str(CTLtree("+(AX EG x1)( - +(x1)(AG x2) )")))

if __name__=='__main__':
	test()