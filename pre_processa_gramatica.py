f = open('lista_gramatica.txt','w')

f.write('[')

with open('gramatica.txt','r') as g:
	for line in g:
		line = line[:-1]
		f.write("'" + line + "'" + ',')

f.write(']')
