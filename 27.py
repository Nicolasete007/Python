# Aquest programa ve del concurs "HP Codewars"
# Aquesta va ser la meva solució al problema 27
#
# El programa fa castells fent servir "#" com a
# castellers. L'usuari ha d'introduir el castell
# que vol en llenguatge natural, i el programa
# imprimirà per pantalla el castell.
# Exemple: tres de vuit amb folre i l'agulla

c = {
	'pilar': 1,
	'torre': 2,
	'dos': 2,
	'tres': 3,
	'quatre': 4,
	'cinc': 5,
	'sis': 6,
	'set': 7,
	'vuit': 8,
	'nou': 9,
	'deu': 10
}

z = input("Escrigui un castell: ").split(' ')

try:
	z.remove('de')
except:
	pass
try:
	z.remove('amb')
except:
	pass
try:
	z.remove('i')
except:
	pass


y = c[z[0]]
if 'l\'agulla' in z:
	y += 1
j = y
n = c[z[1]]

if 'pilar' in z:
	for i in range(n-1):
		print(" #")
	print("###")
else:
	if 'folre' in z:
		if 'manilles' in z:
			j += 6
			n -= 6
		else:
			j += 4
			n -= 5
	else:
		j += 2
		n -= 4

	m = n+3

	if j % 2 == 0:
		print((j//2-1) * ' ' + '#')
		print((j//2-1) * ' ' + '#')
	else:
		print((j//2) * ' ' + '#')
		print((j//2) * ' ' + '#')

	if j % 2 == 0:
		print((j//2-1) * ' ' + '##')
	else:
		print((j//2-1) * ' ' + '# #')

	p = (j-y)//2
	for x in range(n):
		print(p * ' ' + y*'#')
	for x in range(c[z[1]] - m):
		p -= 1
		y += 2
		print(p * ' ' + y*'#')
