#copiar o outer html do body da tabela do slr
#script q transforma  o html da tabela em uma lista de listas

from bs4 import BeautifulSoup
import csv
soup = BeautifulSoup(open('tabela.html'), 'html.parser')
lista_linhas = soup.find_all('tr')

f = open('tabela.txt','w')

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