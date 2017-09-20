#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.extras import SelectDateWidget
from models import CEDULA, CAT_ESTADO, CAT_MUNICIPIO, CAT_LOCALIDAD, CAT_PADRONES


FILTROBUSQUEDA = {
    (4,'Folio Padrón'),(3,'Folio Cedula'),(2,'Nombre Beneficiario'),(1,'Nombre de Representante')
}

class Busquedaform(forms.Form):
    CD_filtro = forms.ChoiceField(
        choices=FILTROBUSQUEDA,
        label='Filtro',
    )


    CD_busqueda = forms.CharField(
       label='Busqueda'
    )


class cedulaforms(ModelForm):
    class Meta:
        model = CEDULA
        fields = ['origen','fechCierre','asgeneral','asdetalle','DatInteresado',\
                  'Of_respuesta','Of_turnado','eseguimiento','uatencion', 'estatus', 'fechCreacion', 'ulevantamiento']
        #hidden = ['estatus', 'fechCreacion', 'ulevantamiento']
        labels = {
            'origen':('Origen'),
            'fechCierre':('Fecha de Cierre'),
            'asgeneral':('Asunto General'),
            'asdetalle':('Detalle del Asunto'),
            'respuesta': ('Respuesta'),
            'Of_respuesta':('Numero de Oficio de Respuesta'),
            'Of_turnado': ('Numero de Oficio de Turnado'),
            'eseguimiento': ('Encargado'),
            'utencion':('Usuario atendio')
        }
        widgets = {
            'estatus':forms.HiddenInput,
            'fechCreacion':forms.HiddenInput,
            'ulevantamiento':forms.HiddenInput,
            'DatInteresado':forms.HiddenInput
        }

class FormEstado(forms.Form):
    nomEstado = forms.ModelChoiceField(queryset=CAT_ESTADO.objects.order_by('idEstado'),
        label = 'Estado',
        empty_label=u'----------',
        to_field_name='idEstado',
        widget=forms.Select(attrs={'id': 'post-Estado','required':True})
    )


class FormMunicipio(forms.Form):
    nomMunicipio = forms.ModelChoiceField(queryset = CAT_MUNICIPIO.objects.order_by('idmunicipio'),
        label = 'Municipio',
        empty_label=u'----------',
        to_field_name='idmunicipio',
        widget=forms.Select(attrs={'id': 'post-Municipio', 'required': True})
    )

class FormLocalidad(forms.Form):
    nomLocaliad = forms.ModelChoiceField(queryset = CAT_LOCALIDAD.objects.order_by('idlocalidad'),
        label = 'Localidad',
        empty_label=u'----------',
        to_field_name='idlocalidad',
        widget=forms.Select(attrs={'id': 'post-Localidad', 'required': True})
    )


class datospersonaExiste(forms.Form):
    idcatpadron=forms.IntegerField()
    idpersona=forms.CharField(max_length=10)

class datospersonaNoexiste(forms.Form):
    SEXO = (
        ('', '-------'),
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )

    nombre = forms.CharField(max_length=150,label='Nombre')
    primApellido = forms.CharField(max_length=150,label='Apellido Paterno')
    segApellido = forms.CharField(max_length=150,label='Apellido Materno')
    sexo = forms.ChoiceField(choices=SEXO, label='Sexo',
                             widget=forms.Select(attrs={'required': True}))
    fecNac = forms.DateField(label='Fec. Nacimiento')
    curp = forms.CharField(max_length=18, label='Curp:')
    telLocal = forms.CharField(max_length=30, label='Tel. Local')
    telCel = forms.CharField(max_length=30, label='Tel. Celular')
    email = forms.EmailField(max_length=150,label='Email')
    estado = forms.ModelChoiceField (
        queryset = CAT_ESTADO.objects.order_by('idEstado'),
        label = 'Estado',
        empty_label = u'----------',
        to_field_name = 'idEstado',
        widget=forms.Select(attrs={'id': 'post-Estado', 'required': True})
    )
    municipio = forms.ModelChoiceField(
        queryset=CAT_MUNICIPIO.objects.order_by('idmunicipio'),
        label='Municipio',
        empty_label=u'----------',
        to_field_name='pk',
        widget=forms.Select(attrs={'id': 'post-Municipio', 'required': True})
    )
    localidad = forms.ModelChoiceField(
        queryset=CAT_LOCALIDAD.objects.order_by('idlocalidad'),
        label='Localidad',
        empty_label=u'----------',
        to_field_name='pk',
        widget=forms.Select(attrs={'id': 'post-Localidad', 'required': True})
    )
    vialidad = forms.CharField(max_length=50, label='Vialidad:')
    numExterior = forms.CharField(max_length=8, label='No. Exterior:')
    numInterior = forms.CharField(max_length=8, label='No. Interior:')
    codpost = forms.IntegerField(label='Cod. Postal:')
    referencia = forms.CharField(label='Referencia:')
    idcatpadron=forms.ModelChoiceField(label='Padron', queryset=CAT_PADRONES.objects.all(),)
