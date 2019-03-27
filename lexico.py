import re
import sys

class EndOfBuff(Exception):
	pass

InputPointer = -1
literal = ''
identifier = ''
number = ''
linha,coluna = 1,1

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
	global InputPointer,buff,coluna
	InputPointer = InputPointer + 1
	if InputPointer == len(buff):
		raise EndOfBuff
	else:
		coluna = coluna + 1
		return buff[InputPointer]


def retract():
	global InputPointer,coluna
	coluna = coluna - 1
	InputPointer = InputPointer - 1

buff = read_input()

if buff:
	state,ERRO = 0,0

	while True:

		try:
			if state == 0:
				char = getNextChar()
				if char == '.':
					state = 1
				elif char == ';':
					state = 2
				elif char == ':':
					state = 3
				elif char == '+':
					state = 4
				elif char == '-':
					state = 5
				elif char == '*':
					state = 6
				elif char == '/':
					state = 7
				elif char == '%':
					state = 8
				elif char == '(':
					state = 9
				elif char == ')':
					state = 10
				elif char == '[':
					state = 11
				elif char == ']':
					state = 12
				elif char == '&':
					state = 13
				elif char == '|':
					state = 14
				elif char == '!':
					state = 15
				elif char == '=':
					state = 16
				elif char == '>':
					state = 17
				elif char == '<':
					state = 18
				elif char == '"':
					state = 19
				elif letra.match(char):
					state = 20
					identifier = identifier + char
				elif numero.match(char):
					state = 21
					number = number + char
				elif ord(char) in [9,10,32]:
					state = 22
				else:
					print(linha,coluna-1)
					ERRO = 1
			elif state == 1:
				listaTokens.append(('PONT','.'))
				state = 0
			elif state == 2:
				listaTokens.append(('PONT_V',';'))
				state = 0
			elif state == 3:
				listaTokens.append(('D_PONT',':'))
				state = 0
			elif state == 4:
				listaTokens.append(('ADIC','+'))
				state = 0
			elif state == 5:
				listaTokens.append(('SUB','-'))
				state = 0
			elif state == 6:
				char = getNextChar()
				if char == '*':
					listaTokens.append(('POT','**'))
					state = 0
				elif char in [9,10,32]:
					listaTokens.append(('MUL','*'))
					state = 22
				else:
					listaTokens.append(('MUL','*'))
					retract()
					state = 0
			elif state == 7:
				listaTokens.append(('DIV','/'))
				state = 0
			elif state == 8:
				listaTokens.append(('MOD','%'))
				state = 0
			elif state == 9:
				listaTokens.append(('LPAR','('))
				state = 0
			elif state == 10:
				listaTokens.append(('RPAR',')'))
				state = 0
			elif state == 11:
				listaTokens.append(('RBRAK','['))
				state = 0
			elif state == 12:
				listaTokens.append(('LBRAK',']'))
				state = 0
			elif state == 13:
				listaTokens.append(('AND','&'))
				state = 0
			elif state == 14:
				listaTokens.append(('OR','|'))
				state = 0
			elif state == 15:
				listaTokens.append(('NOT','!'))
				state = 0
			elif state == 16:
				listaTokens.append(('EQUAL','='))
				state = 0
			elif state == 17:
				char = getNextChar()
				if char == '=':
					listaTokens.append(('GE','>='))
					state = 0
				else:
					listaTokens.append(('GR','>'))
					retract()
					state = 0
			elif state == 18: #LESS
				char = getNextChar()
				if char == '-':
					listaTokens.append(('ATT','<-'))
					state = 0
				elif char == '=':
					listaTokens.append(('LE','<='))
					state = 0
				elif char == '>':
					listaTokens.append('DIFF','<>')
					state = 0
				elif char in [9,10,32]:
					state = 22
				else:
					listaTokens.append('LT','<')
					retract()
					state = 0
			elif state == 19:	#LITERAL
				char = getNextChar()
				if (ord(char) in range(32,127)) or (ord(char) in [9,10,32]):
					literal = literal + char 
					state = 19
				elif char == '"':
					listaTokens.append(('LITERAL',literal))
					literal = ''
					state = 0
				if len(literal) > 512:
					retract()
					ERRO = 1
					print(linha,coluna-1)
					literal = ''
					state = 0
			elif state == 20:	#ID
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
				else:
					retract()
					if identifier in keywords:
						listaTokens.append((identifier,identifier))
					else:
						listaTokens.append(('ID',identifier))
					identifier = ''
					state = 0
				if len(identifier) > 512:
					retract()
					ERRO = 1
					print(linha,coluna-1)
					literal = ''
					state = 0
			elif state == 21:	#NUMERO
				char = getNextChar()
				if numero.match(char):
					number = number + char
					state = 21
				elif char == ',':
					number = number + char
					state = 21
				elif char in [9,10,32]:
					number = number[:-1]
					listaTokens.append(('NUM',number))
					number = ''
					state = 22
				elif letra.match(char):
					retract()
					ERRO = 1
					print(linha,coluna-1)
					number = ''
					state = 0
				else:
					retract()
					listaTokens.append(('NUM',number))
					number = ''
					state = 0
				if len(number) > 512:
					retract()
					ERRO = 1
					print(linha,coluna-1)
					number = ''
					state = 0
			elif state == 22:	#ESPACO EM BRANCO
				char = getNextChar()
				if char in [9,10,32]:
					if char == 10:
						linha = linha + 1
						coluna = 0
					state = 22
				else:
					retract()
					state = 0

		except EndOfBuff:
			break

	if not ERRO:
		print('OK')
		print(listaTokens)
else:
	print('ARQUIVO INVALIDO')