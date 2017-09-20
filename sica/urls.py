"""sica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from sica_app.views import home
from sica_app.views import vistaformularios
from sica_app.views import cambiaMunicipio
from sica_app.views import cambiaLocalidad
from sica_app.views import crearcedula

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^home$', home, name='home'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
    url(r'^formularios$', vistaformularios, name='Formularios '),
    url(r'^datosmunicipio', cambiaMunicipio, name='cambiaMunicipio '),
    url(r'^datoslocalidad', cambiaLocalidad, name='cambiaLocalidad '),
    # url(r'^crearcedula', crearcedula, name='crearcedula '),
    url(r'^crearcedula/(?P<paso>[0-9])', crearcedula, name='crearcedula'),
]
