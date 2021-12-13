#import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dashboard.dash_apps import prediccionLSTM as LSTM
from dashboard.dash_apps import patrones

import time
import pandas as pd
from datetime import datetime

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

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
df = obtenerDatos('amazonstocks.csv')

available_indicators = ["NASDAQ: AAPL", "NASWRS: EGPL", "AAWEAQ: AOAL"]
#print(available_indicators)

app = DjangoDash('SimpleExample', external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    html.Div([
        html.P("Seleccionar archivo:"),
        dcc.Dropdown(
            id='crossfilter-xaxis-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='',
        )],
        style={'width': '95%', 'margin': 'auto', 'marginTop': '15px'},
   ),
    dcc.Graph(id="graph"),
    html.Div([
        html.P("Tipo de gráfica:"),
        dcc.RadioItems(
        id='crossfilter-xaxis-type',
        options=[{'label': str(" ") + i, 'value': i} for i in ['Velas', 'Barras','Lineal']],
        value='Velas',
        labelStyle={'display': 'block', 'marginTop': '5px'},
    )],
        style={'marginLeft': '40px', 'float': 'left', 'width': '50%'},
        id="tipografica"
    ),
    html.Div([
        dbc.Button('Buscar patrones', 
            id='buscarPatrones', 
            className="btn btn-primary btn-lg",
            style={'marginRight': '20px', 'background-color': '#527afd'},
            n_clicks=0
        ),
        dbc.Button('Predicción', 
            id='hacerPrediccion',
            className="btn btn-primary btn-lg", 
            style={'background-color': '#527afd'},
            n_clicks=0
        ),
    ],
        style={'marginRight': '50px', 'margin': 'auto','width': '30%'},
    ),
    dcc.Graph(id="graph-patterns"),
    dcc.Graph(id="graph-prediction"),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Parámetros de búsqueda", style={'font-size':'100%'})),
        dbc.ModalBody(
            html.Div([
                html.P("Seleccione los patrones que desea encontrar:"),
                dcc.Checklist(
                    id = "patrones",
                    options=[
                        {'label': ' Triángulo ascendente', 'value': 'tascendente'},
                        {'label': ' Triángulo descendente', 'value': 'tdescendente'},
                        {'label': ' Triángulo lateral', 'value': 'tlateral'},
                    ],
                    value=[],
                    labelStyle={'display': 'block', 'margin-left':'15px'}
                ),
                html.P("Tamaño de patrones: ", style={'margin-top':'20px'}),
                dcc.Slider(
                    id='my-slider',
                    min=0,
                    max=2,
                    step=1,
                    value=1,
                    marks={
                        0: 'Pequeño',
                        1: 'Medio',
                        2: 'Grande'
                    }
                ),
                html.P("La exactitud de la búsqueda está relacionada con el tamaño de datos que serán analizados. Tome en cuenta que a mayor exactitud, mayor será el tiempo de respuesta.",
                className="text-secondary",
                style={'margin-top':'50px', 'font-size':'80%'})
            ])
        ),
        dbc.ModalFooter(
                dbc.Button("Buscar", 
                    id="buscar", 
                    className="ms-auto", 
                    style={'background-color': '#527afd'},
                    n_clicks=0
                )),],
            id="modal-1",
            is_open=False,
        ),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Parámetros de predicción", style={'font-size':'100%'})),
        dbc.ModalBody(
            html.Div([
                html.P("Seleccione la cantidad de días a predecir:"),
                html.P("(A partir del último día que aparece en los datos)",
                    className="text-secondary",
                    style={'font-size':'80%'}
                ),
                dcc.Input(
                    id="dtrue", type="number",
                    debounce=True, placeholder="Ingresa un número",
                ),
                html.P("Exactitud de entrenamiento: ", style={'margin-top':'20px'}),
                dcc.Slider(
                    id='my-slider-2',
                    min=0,
                    max=2,
                    step=1,
                    value=1,
                    marks={
                        0: 'Bajo',
                        1: 'Medio',
                        2: 'Alto'
                    }
                ),
                html.P("La exactitud de entrenamiento define la cantidad de veces que la red neuronal es entrenada, a mayor exactitud tomará más tiempo. Tome en cuenta que el tamaño de los datos también influye en el tiempo de respuesta.",
                className="text-secondary",
                style={'margin-top':'50px', 'font-size':'80%'}),
            ])
        ),
        dbc.ModalFooter(
                dbc.Button("Predecir", 
                    id="predecir", 
                    className="ms-auto",  
                    style={'background-color': '#527afd'},
                    n_clicks=0
                )),],
            id="modal-2",
            is_open=False,
        ),
])


#Precisión de búsqueda de patrones
@app.callback(
    Output('slider-output-container', 'children'),
    [Input('my-slider', 'value')])
def update_output(value):
    print("PRECISIÓN DE BUSQUEDA")
    if(value < 1):
        print("Bajo")
        return "Bajo"
    elif(value == 0):
        print("Medio")
        return "Medio"
    elif(value == 2):
        print("Alto")
        return "Alto"

#Precisión de predicción
@app.callback(
    Output('slider-output-container-2', 'children'),
    [Input('my-slider-2', 'value')])
def update_output(value):
    aux = value
    print("PRECISIÓN DE BUSQUEDA")
    if(value < 1):
        print("Bajo")
        return "Bajo"
    elif(value == 0):
        print("Medio")
        return "Medio"
    elif(value == 2):
        print("Alto")
        return "Alto"

#Boton de búsqueda
#Entradas: click en buscar patrones, click en buscar (después de seleccionar opciones)
@app.callback(
    Output("modal-1", "is_open"),
    [Input("buscarPatrones", "n_clicks"), Input("buscar", "n_clicks")],
    [State("modal-1", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#Boton de predicción
#Entradas: click en boton predicción, click en boton predecir (después de seleccionar opciones)
@app.callback(
    Output("modal-2", "is_open"),
    [Input("hacerPrediccion", "n_clicks"), Input("predecir", "n_clicks")],
    [State("modal-2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



#Grafica archivo
#Entradas: tipo de gráfica, título del archivo
@app.callback(
    Output("graph", "figure"),
    [Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-xaxis-column','value')]
    )

def display_graphs(graph_type, graph_title):
    
    fig = go.Figure()
    data = df.copy(deep=True)


    if(graph_type == "Velas"):
        fig = go.Figure(go.Candlestick(
            #x=df['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        ))

    elif(graph_type == "Lineal"):
        fig = go.Figure(go.Scatter(
            #x=df['Date'],
            y=data['Close']
        ))

    elif(graph_type == "Barras"):
        fig = go.Figure(go.Ohlc(
            #x=df['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        ))

    fig.update_layout(
        title = graph_title,
        xaxis_rangeslider_visible=False
    )
    
    return fig

#Grafica patrones
@app.callback(
    Output("graph-patterns", "figure"),
    [Input('patrones', 'value'),
    Input("my-slider", "value"),
    Input("buscar", "n_clicks")]
    )
#Entradas: patrones a buscar, error de segmentación
def display_patterns(listaPatrones, errorSegmentacion, botonBuscar):

    fig = go.Figure()
    title = "Búsqueda "

    data = df.copy(deep=True)

    if(botonBuscar != 0 and listaPatrones):

        if errorSegmentacion == 0:
            data_search = patrones.buscaPatrones(data,0.05,listaPatrones)
        if errorSegmentacion == 1:
            data_search = patrones.buscaPatrones(data,1,listaPatrones)
        if errorSegmentacion == 2:
            data_search = patrones.buscaPatrones(data,10,listaPatrones)
        
        fig = go.Figure(go.Scatter(
            #x=df['Date'],
            y=data['Close']
        ))

        for i in range(0,len(data_search)):
            cordenadasx = []
            cordenadasy = []
            segment = data_search[i]
            print(segment)
            print("\n")
            for value in segment[1]:
                cordenadasx.append(value[0])
                cordenadasy.append(value[1])
            if(segment[0] == 0):
                segment[0] = "Triángulo ascendente"
            if(segment[0] == 1):
                segment[0] = "Triángulo descendente"
            if(segment[0] == 2):
                segment[0] = "Triángulo lateral"
            if(segment[0] == 3):
                segment[0] = "Complemento"
            fig.add_trace(go.Scatter(
                            x = cordenadasx, 
                            y = cordenadasy,
                            name= str(segment[0])
                        ))
    fig.update_layout(
        title = title + str(listaPatrones),
        xaxis_rangeslider_visible=False
        )

    return fig


#Grafica prediccion
@app.callback(
    Output("graph-prediction", "figure"),
    [Input('dtrue', 'value'),
    Input("my-slider-2", "value"),
    Input("predecir", "n_clicks")]
    )
#Entradas: dias a predecir, precision de entrenamiento
def display_predictions(diasPrediccion, precisionPrediccion, botonPrediccion):
    
    fig = go.Figure()

    data = df.copy(deep=True)

    if (botonPrediccion != 0 and diasPrediccion > 0 ):
        data_predict = LSTM.prediccionLSTM(data[0:500], diasPrediccion, precisionPrediccion)
        fig = go.Figure(go.Scatter(
            x=data_predict[0].index,
            y=data_predict[0],
            name="Entrenamiento"
        ))
        
        fig.add_trace(go.Scatter(
            x=data_predict[1].index,
            y=data_predict[1],
            name="Predicción"
        ))
        
        
    fig.update_layout(
        title = str(diasPrediccion) + " dias a predecir " + str(precisionPrediccion),
        xaxis_rangeslider_visible=False
        )
       
    return fig