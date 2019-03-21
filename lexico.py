import sys
import re

erro = []

keywords = ['ATEH','BIT','DE','ENQUANTO','ESCREVA','FIM','FUNCAO','INICIO',
			'INTEIRO','LEIA','NULO','PARA','PARE','REAL','RECEBA','SE','SENAO','VAR',
			'VET','.',':',';','<','+','*','/','-','**','%','[',']','>','<=','>=','=',
			'<>','"','&','|','!','(',')','<-']



l = '[a-zA-Z]'
n = '[0-9]'

letra = re.compile(l)
numero = re.compile(n)

linha,finish,flag_id = 1,0,0

while True:

	try:

		if finish:	#sai do loop se foi encontrado algum char invalido
			break

		line = sys.stdin.readline()

		if len(line) == 1 and ord(line) == 10:	#unico caractere eh o enter, caso contrario eh linha com enter no final
			print('enter')
		else:

			tam_max_id = 0	#tamango max do id comeca como 0
			buff = ''	#buffer para guardar token atual

			for coluna,char in enumerate(line):	

				if ord(char) in range(33,127):	#caracteres imprimiveis

					if re.match(letra,char) and flag_id == 0:	#trata identificadores
						flag_id = 1
						tam_max_id = tam_max_id + 1

					elif re.match(letra,char) and flag_id == 1:
						tam_max_id = tam_max_id + 1

					elif not re.match(letra,char) and flag_id == 1:

						if re.match(numero,char):	#se estou lendo um id e leio numero tudo ok
							continue

						if char in ['+','-','/','*','**','%','<','>','=']	#achei um operador,fim do id

						msg_erro = str(linha) + ' ' + str(coluna + 1)
						erro.append(msg_erro)
						flag_id = 0
						tam_max_id = 0

					elif not re.match(letra,char) and flag_id == 0:
						msg_erro = str(linha) + ' ' + str(coluna + 1)
						erro.append(msg_erro)

					if tam_max_id > 250:	#estourou o tamanho do identificador
						msg_erro = str(linha) + ' ' + str(coluna + 1)
						erro.append(msg_erro)
						flag_id = 0
						tam_max_id = 0

				elif ord(char) in [32,9,10]:	#espacos em branco
					pass
				else:
					print('ARQUIVO INVALIDO')
					finish = 1
									
		linha = linha + 1

		print(erro)

	except EOFError:
		break
