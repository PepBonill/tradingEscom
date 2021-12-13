def interpolacion(datos, elemento):
	x0 = elemento[0]
	y0 = datos[elemento[0]]
	x1 = elemento[1]
	y1 = datos[elemento[1]]

	return (x0, y0, x1, y1)

# Calcular tendencia de un segmento
def tendencia(s):
	if s[3] > s[1]:
		return 1 # Tendencia ascendente
	else:
		return 0 # Tendencia descendente