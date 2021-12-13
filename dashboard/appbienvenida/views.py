from django.shortcuts import render, redirect
#from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "appbienvenida/index.html")

def indexConocer(request):
    return render(request, "appbienvenida/conocermas.html")

def indexLogin(request):
    return render(request, "appbienvenida/login.html")

def dashInicio(request):
    return render(request, "appbienvenida/inicio.html")

def dashPerfil(request):
    return render(request, "appbienvenida/perfil.html")

def dashAcercade(request):
    return render(request, "appbienvenida/acercade.html")

def indexTutorial(request):
    return render(request, "appbienvenida/tutorial.html")

def indexRegistra(request):
    return render(request, "appbienvenida/registra.html")

#Bibliotecas
import pandas as pd                    #Almacenamiento y análisis de datos 
import numpy as np
from numpy import genfromtxt           #Guardar valores de archivo csv
from datetime import datetime, timedelta       #Filtración rangos de fechas

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


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import UserRegisterForm
from django.urls import reverse_lazy
from django.conf import settings

def dashArchivos(request):
    
    misarchivos = Archivo.objects.all()
    contexto = {
        'misarchivos': misarchivos
    }

    if request.method == 'POST':
       myfile = Archivo()
       myfile.Nombre= request.FILES.get('archivosubido').name
       #myfile.usuario_id = request.settings.AUTH_USER_MODEL()
       myfile.usuario_id = request.user
       myfile.media = request.FILES.get('archivosubido')
       myfile.save()
        

    return render(request, 'appbienvenida/archivos.html', contexto)

def dashGraph(request):
    misarchivos = Archivo.objects.all()
    contexto = {
        'misarchivos': misarchivos
    }
    return render(request, "appbienvenida/dash.html", contexto)
    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'usuario {username} creado')
            return redirect("login")

    else:
        form = UserRegisterForm()
        
    context = {'form':form}
    return render(request, 'appbienvenida/registra.html', context)

