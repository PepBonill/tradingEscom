def proporciones(segmentos):

	# x = zip(range(len(segmentos))[:-7], range(len(segmentos))[1:-6], range(len(segmentos))[2:-5], range(len(segmentos))[3:-4], range(len(segmentos))[4:-3], range(len(segmentos))[5:-2], range(len(segmentos))[6:-1], range(len(segmentos))[7:])
	# caracteristicas = []

	# for elemento in x:
		
	caracteristicas = []
	p = []
	for indice in range(len(segmentos)- 8):

		if segmentos[indice][3] >= segmentos[indice][1]:
			p.append(1)
		else:
			p.append(-1)

		for i in range(1, 7):
			#print(i)
			p.append((segmentos[indice+i][3] - segmentos[indice+i][1]) / (segmentos[indice+i][1] - segmentos[indice+i-1][1]))

		#p.append((segmentos[indice+6][3] - segmentos[indice][3]) / abs(segmentos[indice+1][3] - segmentos[indice+1][1]))


	#print(p[indice+8:indice+8])

	inicio = 0
	fin = 7
	while fin <= len(p):
		caracteristicas.append(p[inicio:fin])
		inicio = inicio + 7
		fin = fin + 7
	
	return caracteristicas

		# p2 = (segmentos[indice+1][3] - segmentos[indice+1][1]) / (segmentos[indice+1][1] - segmentos[indice][1])
		# p3 = (segmentos[indice+2][3] - segmentos[indice+2][3]) / (segmentos[indice+2][3] - segmentos[indice+1][1])
		# for i in range(2, 7):
