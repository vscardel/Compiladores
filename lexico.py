import re
import sys

class EndOfBuff(Exception):
	pass

InputPointer = -1
literal = ''
identifier = ''
number = ''
linha,coluna = 1,0

keywords = [
	'ATEH','BIT','DE','ENQUANTO','ESCREVA','FIM','FUNCAO','INICIO',
	'INTEIRO','LEIA','NULO','PARA','PARE','REAL','RECEBA','SE','SENAO',
	'VAR','VET'
]

n = '[0-9]'
l = '[a-zA-Z]'

letra = re.compile(l)
numero = re.compile(n)

listaTokens = []


def read_input():

	buff = ''
	erro = 0

	while True:
		try:
			s = input()

			for char in s:
				if (ord(char) not in range(32,127) 
				and ord(char) not in range(9,11)):
					erro = 1
					raise EOFError

			buff += s + '\n'
		except EOFError:
			break

	buff = buff[:-1]

	if erro:
		return 0
	else:
		return buff

def getNextChar():
	global InputPointer,buff,coluna,ERRO
	InputPointer = InputPointer + 1
	if InputPointer == len(buff): 
		if literal:
			if literal[len(literal)-1] == '"':
				LITERAL = literal[:-1]
				listaTokens.append(('LITERAL',LITERAL))
			else:
				print(linha,coluna)
				ERRO = 1
		elif identifier:
			if identifier in keywords:
				listaTokens.append((identifier,identifier))
			else:
				listaTokens.append(('ID',identifier))
		elif number:
				listaTokens.append(('NUM',number))
		raise EndOfBuff
	else:
		coluna = coluna + 1
		return buff[InputPointer]


def retract():
	global InputPointer,coluna
	coluna = coluna - 1
	InputPointer = InputPointer - 1

def checa_linha(char):
	global linha,coluna
	if ord(char) == 10:
		linha = linha + 1
		coluna = 0


buff = read_input()

if buff:
	state,ERRO,flag_virgula = 0,0,0

	while True:

		try:
			if state == 0:
				char = getNextChar()
				if char == '.':
					listaTokens.append(('PONT','.'))
					state = 0
				elif char == ';':
					listaTokens.append(('PONT_V',';'))
					state = 0
				elif char == ':':
					listaTokens.append(('D_PONT',':'))
					state = 0
				elif char == '+':
					listaTokens.append(('ADIC','+'))
					state = 0
				elif char == '-':
					listaTokens.append(('SUB','-'))
					state = 0
				elif char == '*':
					if InputPointer == len(buff)-1:
						listaTokens.append(('MUL','*'))
					state = 6
				elif char == '/':
					listaTokens.append(('DIV','/'))
					state = 0
				elif char == '%':
					listaTokens.append(('MOD','%'))
					state = 0
				elif char == '(':
					listaTokens.append(('LPAR','('))
					state = 0
				elif char == ')':
					listaTokens.append(('RPAR',')'))
					state = 0
				elif char == '[':
					listaTokens.append(('RBRAK','['))
					state = 0
				elif char == ']':
					listaTokens.append(('LBRAK',']'))
					state = 0
				elif char == '&':
					listaTokens.append(('AND','&'))
					state = 0
				elif char == '|':
					listaTokens.append(('OR','|'))
					state = 0
				elif char == '!':
					listaTokens.append(('NOT','!'))
					state = 0
				elif char == '=':
					listaTokens.append(('EQUAL','='))
					state = 0
				elif char == '>':
					if InputPointer == len(buff)-1:
						listaTokens.append(('GT','>'))
					state = 17
				elif char == '<':
					if InputPointer == len(buff)-1:
						listaTokens.append(('LT','<'))
					state = 18
				elif char == '"':
					if InputPointer == len(buff)-1:
						print(linha,coluna)
						ERRO = 1
					state = 19
				elif letra.match(char):
					state = 20
					identifier = identifier + char
				elif numero.match(char):
					state = 21
					number = number + char
				elif ord(char) in [9,10,32]:
					state = 22
					checa_linha(char)
				else:
					print(linha,coluna)
					ERRO = 1
			
			elif state == 6:
				char = getNextChar()
				if char == '*':
					listaTokens.append(('POT','**'))
					state = 0
				elif char in [9,10,32]:
					checa_linha(char)
					listaTokens.append(('MUL','*'))
					state = 22
				else:
					listaTokens.append(('MUL','*'))
					retract()
					state = 0
			elif state == 17:
				char = getNextChar()
				if char == '=':
					listaTokens.append(('GE','>='))
					state = 0
				elif char in [9,10,32]:
					state = 22
					checa_linha()
				else:
					listaTokens.append(('GR','>'))
					retract()
					state = 0
			elif state == 18: #LESS
				char = getNextChar()
				if char == '-':
					listaTokens.append(('ATR','<-'))
					state = 0
				elif char == '=':
					listaTokens.append(('LE','<='))
					state = 0
				elif char == '>':
					listaTokens.append(('DIFF','<>'))
					state = 0
				elif char in [9,10,32]:
					state = 22
					checa_linha(char)
				else:
					listaTokens.append(('LT','<'))
					retract()
					state = 0
			elif state == 19:	#LITERAL
				if len(literal) > 512:
						retract()
						print(linha,coluna)
						ERRO = 1
						literal = ''
						state = 0
				else:
					char = getNextChar()
					if char == '"':
						listaTokens.append(('LITERAL',literal))
						literal = ''
						state = 0
					elif (ord(char) in range(32,127)) or (ord(char) in [9,10,32]):
						if ord(char) == 10:
							checa_linha(char)
						literal = literal + char 
						state = 19

			elif state == 20:	#ID
				if len(identifier) > 512:
					retract()
					ERRO = 1
					print(linha,coluna)
					identifier = ''
					state = 0
				else:
					char = getNextChar()
					if letra.match(char):
						identifier = identifier + char
						state = 20
					elif numero.match(char):
						identifier = identifier + char
						state = 20
					elif ord(char) in [9,10,32]:
						if identifier in keywords:
							listaTokens.append((identifier,identifier))
						else:
							listaTokens.append(('ID',identifier))
						identifier = ''
						state = 22
						checa_linha(char)
					else:
						retract()
						if identifier in keywords:
							listaTokens.append((identifier,identifier))
						else:
							listaTokens.append(('ID',identifier))
						identifier = ''
						state = 0
			elif state == 21:	#NUMERO
				if len(number) > 512:
					retract()
					print(linha,coluna)
					ERRO = 1
					number = ''
					state = 0
					flag_virgula = 0
				else:
					char = getNextChar()
					if numero.match(char):
						number = number + char
						state = 21
					elif char == ',':
						if not flag_virgula:
							flag_virgula = 1
							number = number + char
							state = 21
						else:
							retract()
							print(linha,coluna)
							ERRO = 1
							number = ''
							flag_virgula = 0
							state = 0
					elif char in [9,10,32]:
						number = number[:-1]
						listaTokens.append(('NUM',number))
						number = ''
						state = 22
						checa_linha(char)
						flag_virgula = 0
					elif letra.match(char):
						retract()
						ERRO = 1
						print(linha,coluna)
						number = ''
						state = 0
						flag_virgula = 0
					else:
						retract()
						listaTokens.append(('NUM',number))
						number = ''
						state = 0
						flag_virgula = 0
			elif state == 22:	#ESPACO EM BRANCO
				char = getNextChar()
				if ord(char) in [9,10,32]:
					if ord(char) == 10:
						checa_linha(char)
					state = 22
				else:
					retract()
					state = 0

		except EndOfBuff:
			break

	if not ERRO:
		print('OK')
else:
	print('ARQUIVO INVALIDO')