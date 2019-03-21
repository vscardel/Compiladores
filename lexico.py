import sys
import re

erro = []
tokens = []

keywords = ['ATEH','BIT','DE','ENQUANTO','ESCREVA','FIM','FUNCAO','INICIO',
			'INTEIRO','LEIA','NULO','PARA','PARE','REAL','RECEBA','SE','SENAO','VAR',
			'VET','.',':',';','<','+','*','/','-','**','%','[',']','>','<=','>=','=',
			'<>','"','&','|','!','(',')','<-']



linha,finish,flag_id,flag_num = 1,0,0,0

l = '[a-zA-Z]'
n = '[0-9]'

letra = re.compile(l)
numero = re.compile(n)

def eh_letra(char):
	return re.match(letra,char)

def eh_numero(char):
	return re.match(numero,char)

def gera_msg_erro(linha,coluna):
	msg_erro = str(linha) + ' ' + str(coluna + 1)
	erro.append(msg_erro)

def checa_tam_id():
	global flag_id,tam_max_id

	if tam_max_id > 250:
		gera_msg_erro(linha,coluna)
		flag_id = 0
		tam_max_id = 0

def checa_tam_num():
	global flag_num,tam_max_num

	if tam_max_num > 250:
		gera_msg_erro(linha,coluna)
		flag_num = 0
		tam_max_num = 0



while True:

	try:

		if finish:	#sai do loop se foi encontrado algum char invalido
			break

		line = sys.stdin.readline()

		tam_max_id,tam_max_num = 0,0	#tamango max do id comeca como 0
		buff = ''	#buffer para guardar token atual

		for coluna,char in enumerate(line):	

			if ord(char) in range(32,127) or ord(char) in [9,10]:	#caracteres imprimiveis

				if eh_letra(char):	#trata letras

					if flag_num == 1:
						gera_msg_erro(linha,coluna)
						flag_num = 0

					if flag_id == 0:
						flag_id = 1
						tam_max_id = tam_max_id + 1

					elif flag_id == 1:
						tam_max_id = tam_max_id + 1
						checa_tam_id()

				elif eh_numero(char):	#trata numeros

					if flag_id == 0:

						if flag_num == 0:
							flag_num = 1
							tam_max_num = tam_max_num + 1

						elif flag_num == 1:
							tam_max_num = tam_max_num + 1
							checa_tam_num()

					elif flag_id == 1:
						tam_max_id = tam_max_id + 1
						checa_tam_id()

				else: #trata outros caracteres (lembrar de tratar a ',' para numeros)
					pass	
			else:
				print('ARQUIVO INVALIDO')
				finish = 1
				break
									
		linha = linha + 1

		print(erro)

	except EOFError:
		break
