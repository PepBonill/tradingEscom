from dashboard.dash_apps import crear
import costo

def bottomup(datos, error_max):
	# Crear segmentos iniciales
	x = zip(range(len(datos))[:-1], range(len(datos))[1:])
	segmentos = []

	for elemento in x:
		segmentos.append(crear.interpolacion(datos, elemento))

	# Crear linea entre el primer punto con el ultimo de dos segmentos juntos
	y = zip(segmentos[:-1], segmentos[1:])
	segmentos_unidos = []

	for elemento1, elemento2 in y:
		segmentos_unidos.append((crear.interpolacion(datos, (elemento1[0], elemento2[2]))))

	# Calcular el costo de unir segmentos
	costos = []
	for segmento in segmentos_unidos:
		costos.append(costo.calcular_costo(datos, segmento))
	
	# print("Costos: ", costos)
	# print("Costo minimo: ", min(costos))

	while min(costos) < error_max:
		#print("Costos: ", costos)
		indice = costos.index(min(costos))
		segmentos[indice] = segmentos_unidos[indice]
		del segmentos[indice+1]

		# Crear linea entre el nuevo segmento y su vecino izquierdo, y calcular su costo
		if indice > 0:
			segmentos_unidos[indice-1] = crear.interpolacion(datos, (segmentos[indice-1][0],segmentos[indice][2]))
			costos[indice-1] = costo.calcular_costo(datos, segmentos_unidos[indice-1])

		# Crear linea entre el nuevo segmento y su vecino derecho, y calcular su costo
		if indice+1 < len(segmentos_unidos):
			segmentos_unidos[indice+1] = crear.interpolacion(datos, (segmentos[indice][0], segmentos[indice+1][2]))
			costos[indice+1] = costo.calcular_costo(datos, segmentos_unidos[indice+1])
		
		# Eliminar linea entre el viejo segmento y su costo
		del segmentos_unidos[indice]
		del costos[indice]
		#print("Costos: ", costos)
	
	# Unir segmentos juntos que compartan tendencia	
	# z = zip(segmentos[:-1], segmentos[1:])
	# inicio = [0,0,0,0]
	# indice = 0

	# for s1, s2 in z:
	# 	if indice < len(segmentos)-1:
	# 		if crear.tendencia(s1) == crear.tendencia(s2): #parece que s1 es igual que inicio en tendencia
	# 			# print("Segmentos: ", segmentos[indice], segmentos[indice+1], "IGUALES")
	# 			if inicio[0] == 0 and inicio[2] == 0:
	# 				segmentos[indice] = crear.interpolacion(datos, (s1[0], s2[2]))
	# 				del segmentos[indice+1]
	# 				inicio = segmentos[indice]
	# 				# print("Segmento ", segmentos[indice], "inicio: ", inicio)
	# 			else:
	# 				segmentos[segmentos.index(inicio)] = crear.interpolacion(datos, (inicio[0], s2[2]))
	# 				del segmentos[indice+1]
	# 				aux = inicio[0]
	# 				inicio = crear.interpolacion(datos, (aux, s2[2]))
	# 		else:
	# 			# print("Segmentos: ", segmentos[indice], segmentos[indice+1], "DIFERENTES")
	# 			# inicio = [0, 0, 0, 0]
	# 			print("else")
			
	# 		indice = indice + 1

	indice = 0
	while indice != len(segmentos)-1:
		z = zip(segmentos[:-1], segmentos[1:])
		for s1, s2 in z:
			indice = segmentos.index(s2)
			# print("Indice: ", indice)
			# print("Cantidad: ", len(segmentos))
			if crear.tendencia(s1) == crear.tendencia(s2):
				segmentos[segmentos.index(s1)] = crear.interpolacion(datos, (s1[0], s2[2]))
				del segmentos[segmentos.index(s2)]
				break

	

	# print("Cantidad de segmentos finales: ", len(segmentos))

	return segmentos