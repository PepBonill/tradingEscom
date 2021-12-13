from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim, show, ylim
from matplotlib.lines import Line2D
from dashboard.dash_apps import segmento
from dashboard.dash_apps import crear
from dashboard.dash_apps import extraer
import pandas as pd                    #Almacenamiento y análisis de datos 
import numpy as np
import joblib
from tensorflow import keras

def obtenerDatos(ruta):
    #Lectura de datos
    try:
        datos = pd.read_csv(ruta)
    except:
        print("No se pude abrir el archivo")
        return -1
    
    #Convierte fecha en marca de tiempo
    #datos.index = datos["Date"].apply(lambda x: pd.Timestamp(x))
    #Remplaza la marca de tiempo como los indices de la matriz
    #datos.drop("Date", axis=1, inplace=True)
    
    #print(datos)
    
    #devuelve una matriz con los datos
    return datos

def draw_plot_gral(datos, titulo):
    plot(range(len(datos)), datos, alpha=0.8, color='red')
    title(titulo)
    xlabel("Tiempo")
    ylabel("Precio")
    xlim(0, len(datos) - 1)

def draw_plot(datos, titulo, xlimite1, xlimite2, ylimite1, ylimite2):
    plot(range(len(datos)), datos, alpha=0.8, color='red')
    title(titulo)
    xlabel("Tiempo")
    ylabel("Precio")
    #xlim(0, len(datos) - 1)
    xlim(xlimite1, xlimite2)
    ylim(ylimite1, ylimite2)

def draw_segments(segmentos):
    ax = gca()
    for segment in segmentos:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)

def buscaPatrones(datos, error_max, listaPatrones):
  lista = []

  print(listaPatrones)
  #error_max = 1
  desde = 0
  hasta = len(datos['Close'])

  # Parametrizar valores de los precios de 0 a 100
  indice = 0
  valor_max = max(datos['Close'])

  for dato in datos['Close']:
      datos['Close'][indice] = (100*dato)/valor_max
      indice = indice + 1

  print(datos['Close'])


  #Obtener grafica simplificada
  segmentos = segmento.bottomup(datos['Close'][desde:hasta], error_max)

  #Obtener proporciones
  caracteristicas = extraer.proporciones(segmentos)

  #Buscar patron
  datos2 = datos['Close']
  precio_cierre = datos2.tolist()
  
  import pathlib
  #print(pathlib.Path().resolve())
  

  buscaAscendente = False
  buscaDescendente = False
  buscaLateral = False
  #Busca en la lista de parametros los patrones a buscar     
  for ptrn in listaPatrones:
      if ptrn == 'tdescendente':
          buscaDescendente = True
      if ptrn == 'tascendente':
          buscaAscendente = True
      if ptrn == 'tlateral':
          buscaLateral = True

  modelo = joblib.load('dashboard/dash_apps/asc_desc_lat1.pkl')

  for c in range(len(caracteristicas)):
    entradas = caracteristicas[c]
    patron = modelo.predict([entradas])
    clase = np.argmax(patron, axis = 1)
    if clase != 3 and patron[0][clase] > 0.85:
      print("Caracteristica", c, caracteristicas[c])
      print("Patron: ", patron)
      print("Clase: ", clase)
      print("Probabilidad: ", patron[0][clase])
      probabilidad = patron[0][clase]

      #Graficar patron
      xlimite1 = precio_cierre.index(segmentos[c][1])
      print("Xlimite1: ", xlimite1)
      
      xlimite2 = precio_cierre.index(segmentos[c+7][1])
      print("Xlimite2: ", xlimite2)
      
      y_valores = [segmentos[c][1], segmentos[c+1][1], segmentos[c+2][1], segmentos[c+3][1], segmentos[c+4][1], segmentos[c+5][1], segmentos[c+6][1], segmentos[c+7][1]]
      y_valores = np.asarray(y_valores)
      print("Y_valores: ", y_valores)
      
      ind1 = np.unravel_index(np.argmin(y_valores, axis=None), y_valores.shape)
      print("Ylimite1: ", y_valores[ind1])
      
      ind2 = np.unravel_index(np.argmax(y_valores, axis=None), y_valores.shape)
      print("Ylimite2: ", y_valores[ind2])

      #figure(figsize=(5, 5), dpi=80)
      #draw_plot(datos['Close'][desde:hasta], "Patron: " + str(patron), xlimite1-10, xlimite2+10, y_valores[ind1]-1, y_valores[ind2]+1)
      #draw_segments(segmentos[c:c+7])
      #show()

      #Obtiene el patron encontrado
      patronresultado = [clase, segmentos[c:c+7]]

      #Si coincide con los que se van buscar, lo agrega a la lista
      if((patronresultado[0] == 0) and buscaAscendente): 
          lista.append(patronresultado)
          #print("es descendente")
      if((patronresultado[0] == 1) and buscaDescendente): 
          lista.append(patronresultado)
          #print("es ascendente")
      if((patronresultado[0] == 2) and buscaLateral): 
          lista.append(patronresultado)
          #print("es ascendente")
      if(patronresultado[0] == 3):
          #lista.append(patronresultado)
          print("complemento")
        
  return lista

'''
ruta = 'amazonstocks.csv'

segmentos = segmento.bottomup(datos['Close'][0:len(datos['Close'])], 1)
datos = obtenerDatos(ruta)
#Graficar precios
figure(figsize=(28, 8), dpi=80)
aux = datos['Close'][0:len(datos['Close'])]
print(aux.index)
draw_plot_gral(aux, "Bottom-up e interpolacion")
draw_segments(segmentos)
show()


ruta = 'amazonstocks.csv'
aux = buscaPatrones(obtenerDatos(ruta))

for i in range(0,len(aux)):
  print(aux[i])
  print("\n")

'''
