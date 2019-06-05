#copiar o outer html do body da tabela do slr 

from bs4 import BeautifulSoup
import csv
soup = BeautifulSoup(open('tabela.html'), 'html.parser')
lista_linhas = soup.find_all('tr')

f = open('tabela.csv','w')
writer = csv.writer(f, delimiter=";")

for linha in lista_linhas:
	celulas = linha.find_all('td')
	lista_escreve = []
	for celula in celulas:
		aux = celula.get_text()
		if aux == u'\xa0':
			lista_escreve.append('v')
		else:
			lista_escreve.append(aux)
	writer.writerow(lista_escreve)
