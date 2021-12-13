"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LoginView, LogoutView
from appbienvenida import views
from dashboard.dash_apps import SimpleExample
#from .views import registro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('conocermas/', views.indexConocer),
    #path('login/', views.indexLogin),
    path('login/', LoginView.as_view(template_name='appbienvenida/login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(template_name='appbienvenida/index.html'), name = 'logout'),
    path('dash/', views.dashGraph, name="dash"),
    path('inicio/', views.dashInicio),
    path('perfil/', views.dashPerfil),
    path('archivos/', views.dashArchivos),
    path('acercade/', views.dashAcercade),
    path('tutorial/', views.indexTutorial),
    #path('registra/', views.indexRegistra),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    #path('registro/', views.registro, name="registro"),
    #path("register", views.register_request, name="register")
    #url(r'^registrar', RegistroUsuario.as_view(), name="registrar"),
    path('register/', views.register, name='register'),
]

urlpatterns += staticfiles_urlpatterns()