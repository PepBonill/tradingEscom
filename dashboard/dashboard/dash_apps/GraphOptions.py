import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash


app = DjangoDash('GraphOptions')

app.layout = html.Div([
    html.P("Tipo de gráfica"),
    dcc.RadioItems(
        id='crossfilter-xaxis-type',
        options=[{'label': i, 'value': i} for i in ['Velas', 'Barras','Lineal']],
        value='Velas',
        labelStyle={'display': 'block'}
    )
])

print("AFBDFBFDB")
print(Input('crossfilter-xaxis-type', 'value'))
print("ppppppppp")
print(Output('crossfilter-xaxis-type', 'value'))