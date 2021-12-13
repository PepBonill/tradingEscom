from django.urls import path, include
from django.urls.conf import re_path
from django.views import static
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from dashboard.dash_apps import SimpleExample
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

#from views import RegistroUsuario

#from appbienvenida.views import registro



urlpatterns = [
    path('', views.index),
    path('dash/', views.dashGraph),
    path('conocermas/', views.indexConocer),
    path('login/', LoginView.as_view(template_name='appbienvenida/login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(template_name='appbienvenida/index.html'), name = 'logout'),
    path('tutorial/', views.indexTutorial),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
   # path('registro/', views.registro, name="registro"),
    #path("register", views.register_request, name="register")
    #url(r'^registrar', RegistroUsuario.as_view(), name="registrar"),
    path('register/', views.register, name='register'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]