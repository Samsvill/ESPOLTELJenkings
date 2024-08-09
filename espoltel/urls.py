"""
URL configuration for espoltel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from . import views
from .views import download_file

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('solicitud.urls')),
    
    path('api/', include('api.urls')),
    path('api/', include('proyecto.urls')),
    
    path('user/', include('user.urls')),
    
    re_path(r'^media/(?P<path>.*)$', download_file, name='download_file'),
    #ruta con parámetros
    #path('numero/<int:num>/', views.numero, name='numero'),
    #path('vista/', views.vista, name='vista'),
    #path('dinamico/<str:username>', views.dinamico, name='dinamico'),
    #path('estaticos/', views.estaticos, name='estaticos'),

    #path('herencia/', views.herencia, name='herencia'),
    #path('hijo1/', views.hijo1, name='hijo1'),
    #path('hijo2/', views.hijo2, name='hijo2'),

    
]
