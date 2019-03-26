import re
import sys

InputPointer = -1

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
	global InputPointer,buff

	if InputPointer == len(buff):
		if not flagError:
			return 1
	else:
		InputPointer = InputPointer + 1
		return buff[InputPointer]


def retract():
	global InputPointer
	InputPointer = InputPointer - 1

buff = read_input()

if buff:
	state = 0

	while True:

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
				state = 5:
			elif char == '*':
				state = 6
			elif char == '/':
				state = 7:
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
			elif numero.match(char):
				state = 21
			elif ord(char) in [9,10,32]:
				state = 22
		elif state == 1:
			listaTokens.append('PONT','.')
			state = 0
		elif state == 2:
			listaTokens.append('PONT_V',';')
			state = 0
		elif state == 3:
			listaTokens.append('D_PONT',':')
			state = 0
		elif state == 4:
			listaTokens.append('ADIC','+')
			state = 0
		elif state == 5:
			listaTokens.append('SUB','-')
			state = 0
		elif state == 6:
			char = getNextChar()
			if char == '*':
				listaTokens.append('POT','**')
				state = 0
			elif char in [9,10,32]:
				listaTokens.append('MUL','*')
				state = 22
			else:
				retract()
				print('linha','coluna')
				state = 0
else:
	print('ARQUIVO INVALIDO')