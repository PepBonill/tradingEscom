#Bibliotecas
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import plotly.graph_objects as go

#Cargar datos
#Recibe como parámetro la ruta del archivo csv
#Devuelve una matriz con los datos
def obtenerDatos(ruta):
    #Lectura de datos
    try:
        my_data = pd.read_csv(ruta)
    except:
        print("No se pude abrir el archivo")
        return -1
    
    #Convierte fecha en marca de tiempo
    my_data.index = my_data["Date"].apply(lambda x: pd.Timestamp(x))
    #Remplaza la marca de tiempo como los indices de la matriz
    my_data.drop("Date", axis=1, inplace=True)
    
    #print(my_data)
    
    #devuelve una matriz con los datos
    return my_data

#Grafica datos de manera linea (precio de cierre 'Close')
#Recibe como parámetros un dataframe
def graficaDatos(data):
  plt.figure(figsize=(16,8))
  plt.title(" Historial de precio 'Cierre' ")
  plt.plot(data['Close'])
  plt.xlabel('Fecha')
  plt.ylabel('Precio de Cierre USD ($)')
  plt.show()

def prediccionLSTM(data, dias, exactitud):
    #PREPARACIÓN DE DATOS

    aux = dias
    aux2 = exactitud
    #data = obtenerDatos('amazonstocks.csv')
    print(data)
    data.shape
    #graficaDatos(data)

    #Convertir dataframe a numpy array, solo con el precio de Cierre
    dataArray = data.filter(['Close']).values
    #print(dataArray)

    #Escalado de datos (normalizar valores entre 0 y 1)
    scaler = MinMaxScaler(feature_range=(0,1))
    scaledData = scaler.fit_transform(dataArray)

    #Obtener conjunto de entrenamiento (80% de los datos)
    trainData = scaledData[0:math.ceil((len(dataArray)*0.8)), :]
    #print(trainData)

    #Dividir conjunto de entrenamiento
    x_train = []
    y_train = []

    for i in range(60, len(trainData)):
        x_train.append(trainData[i-60:i, 0])
        y_train.append(trainData[i,0])

    """
    if i <= 60
        print("\nx_train")
        print(x_train)
        print("\ny_train")
        print(y_train)
    """
    #Convertir x_train, y_train en numpy array
    x_train, y_train = np.array(x_train),np.array(y_train)

    #Reedimensionar x_train para ser entradas de la red neuronal
    #print(x_train.shape)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    #print(x_train.shape)


    #Construcción de modelo LSTM
    modelo = Sequential()
    #Primera capa con 50 neuronas, con memoria,entradas del tamaño del conjunto de entrenamiento
    modelo.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1],1)))
    #Segunda capa con 50 neuronas, sin memoria
    modelo.add(LSTM(50, return_sequences=False))
    #Tercera capa tipo densa con 25 neuronas
    modelo.add(Dense(25))
    #Capa de salida tipo densa con una neurona
    modelo.add(Dense(1))

    #Compilar modelo
    modelo.compile(optimizer='adam', loss='mean_squared_error')

    #Entrenamiento del modelo
    modelo.fit(x_train, y_train, batch_size=1, epochs=1)

    #Creación conjunto de prueba
    testData = scaledData[len(trainData)-60:, :]
    #Dividir conjunto de prueba
    x_test = []
    y_test = dataArray[len(trainData):, :]

    for i in range(60, len(testData)):
        x_test.append(testData[i-60:i, 0])

    #Convertir conjunto de prueba en np array
    x_test = np.array(x_test)

    #Reedimensionar conjunto de prueba para ser entrada de la red neuronal
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    #Predicciones
    prediccion = modelo.predict(x_test)
    #Quitar escalado a los valores
    prediccion = scaler.inverse_transform(prediccion)

    #Evaluar el modelo

    #Obtener root mean squared error
    rmse = np.sqrt(np.mean(prediccion - y_test)**2)
    print(rmse)

    #Graficar resultados
    entrenamiento = data[:len(trainData)]
    validaciones = data[len(trainData):]
    validaciones['Prediccion'] = prediccion

    '''
    plt.figure(figsize=(16,8))
    plt.title('LSTM ejemplo')
    plt.xlabel('Fecha')
    plt.ylabel('Precio de Cierre USD ($)')
    plt.plot(entrenamiento['Close'])
    plt.plot(validaciones[['Close', 'Prediccion']])
    plt.legend(['Entrenamiento', 'Validaciones', 'Prediccion' ], loc='lower right')
    plt.savefig("qwe.png")
    plt.show()
    '''

    return [entrenamiento["Close"],validaciones["Prediccion"]]