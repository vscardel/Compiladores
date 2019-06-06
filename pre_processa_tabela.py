#copiar o outer html do body da tabela do slr
#script q transforma  o html da tabela em uma lista de listas

from bs4 import BeautifulSoup
import csv
soup = BeautifulSoup(open('tabela.html'), 'html.parser')
lista_linhas = soup.find_all('tr')
head = soup.find_all('p')

f = open('tabela.txt','w')

#monta o dicionario
f.write('{')
for head in head:
	tokens = head.find_all('th')
	for cont3,token in enumerate(tokens):
		if cont3 != len(tokens)-1:
			f.write("'" + token.get_text() + "':"+str(cont3)+',')
		else:
			f.write("'" + token.get_text() + "':"+str(cont3))
f.write('}')
f.write('\n')	


f.write("[")
for cont2,linha in enumerate(lista_linhas):
	celulas = linha.find_all('td')
	f.write('[ ')
	for cont,celula in enumerate(celulas):
		if cont == 0:
			continue
		aux = celula.get_text()
		if aux == u'\xa0':
			if cont != len(celulas)-1:
				f.write('"v",')
			else:
				f.write('"v"')
		else:
			if cont != len(celulas)-1: 
				f.write('"'+ aux + '"' + ',')
			else:
				f.write('"' + aux +'"')
	if cont2 != len(lista_linhas)-1:
		f.write("],")
	else:
		f.write("]")
f.write("]")
