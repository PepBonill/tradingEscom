import numpy

def calcular_costo(datos, segmento):
	x1 = segmento[0]
	x2 = segmento[2]
	m, error = cuadradosmin(datos, (x1, x2))

	return error


def cuadradosmin(datos, puntos):
	x = numpy.arange(puntos[0], puntos[1]+1)
	y = numpy.array(datos[puntos[0]:puntos[1]+1])
	matriz = numpy.ones((len(x), 2), float)
	matriz[:,0] = x
	(m, b, rank, s) = numpy.linalg.lstsq(matriz, y)
	try:
		error = b[0]
	except IndexError:
		error = 0.0
	return (m, error)
