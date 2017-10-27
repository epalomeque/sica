#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.extras import SelectDateWidget
from models import CEDULA, CAT_ESTADO, CAT_MUNICIPIO, CAT_LOCALIDAD, CAT_PADRONES


FILTROBUSQUEDA = {
    (4, '-----'),(3,'Folio de Padrón'),(2,'Folio de Cedula'),(1,'Nombre del Demandante')
}


class formBuscar(forms.Form):
    busqueda = forms.CharField(
        label='Busqueda',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa los datos para la búsqueda'})
    )


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
        fields = ['estatus', 'origen', 'fechCreacion', 'fechCierre', 'asgeneral', 'asdetalle', 'DatInteresado',
                  'respuesta', 'Of_respuesta', 'Of_turnado', 'eseguimiento', 'ulevantamiento', 'uatencion', 'observacion' ]
        labels = {
                'estatus':('Estatus:'),
                'origen':('Origen:'),
                'fechCreacion':('Fecha de Creación:'),
                'fechCierre':('Fecha de Cierre'),
                'asgeneral':('Asunto General:'),
                'asdetalle':('Detalle del Asunto:'),
                'DatInteresado': ('Datos del Interesado'),
                'respuesta':('Respuesta al caso:'),
                'Of_respuesta':('Numero de Oficio de Respuesta:'),
                'Of_turnado':('Numero de Oficio de Turnado:'),
                'eseguimiento':('Encargado de seguimiento:'),
                'ulevantamiento':('Usuario de Levantamiento:'),
                'uatencion':('Usuario de atención:'),
                'observacion':('Observaciones:')
        }
        widgets = {
                'fechCreacion':forms.HiddenInput,
                'fechCierre':forms.HiddenInput,
                'asdetalle':forms.Textarea(attrs={'cols': '47', 'rows': '7'}),
                'DatInteresado':forms.HiddenInput,
                'respuesta':forms.Textarea(attrs={'cols': '47', 'rows': '5'}),
                'Of_respuesta':forms.HiddenInput,
                'Of_turnado':forms.HiddenInput,
                'ulevantamiento':forms.HiddenInput,
                'observacion':forms.Textarea(attrs={'cols': '47', 'rows': '3'}),
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

    EDOSNAC = (('AS', 'AGUASCALIENTES'), ('BC', 'BAJA CALIFORNIA'), ('BS', 'BAJA CALIFORNIA SUR'), ('CC', 'CAMPECHE'),
               ('CL', 'COAHUILA'), ('CM', 'COLIMA'), ('CS', 'CHIAPAS'), ('CH', 'CHIHUAHUA'), ('DF', 'DISTRITO FEDERAL'),
               ('DG', 'DURANGO'), ('GT', 'GUANAJUATO'), ('GR', 'GUERRERO'), ('HG', 'HIDALGO'), ('JC', 'JALISCO'),
               ('MC', 'MÉXICO'), ('MN', 'MICHOACÁN'), ('MS', 'MORELOS'), ('NT', 'NAYARIT'), ('NL', 'NUEVO LEÓN'),
               ('OC', 'OAXACA'), ('PL', 'PUEBLA'), ('QT', 'QUERÉTARO'), ('QR', 'QUINTANA ROO'),
               ('SP', 'SAN LUIS POTOSÍ'), ('SL', 'SINALOA'), ('SR', 'SONORA'), ('TC', 'TABASCO'), ('TS', 'TAMAULIPAS'),
               ('TL', 'TLAXCALA'), ('VZ', 'VERACRUZ'), ('YN', 'YUCATÁN'), ('ZS', 'ZACATECAS'),
               ('NE', 'NACIDO EN EL EXTRANJERO')
               )

    nombre = forms.CharField(max_length=150,label='Nombre',
                             widget=forms.TextInput(attrs={'placeholder': 'Nombre o nombres'}))
    primApellido = forms.CharField(max_length=150,label='Primer Apellido',
                                   widget=forms.TextInput(attrs={'placeholder': 'Primer Apellido'})
                                   )
    segApellido = forms.CharField(max_length=150,label='Segundo Apellido',
                                  widget=forms.TextInput(attrs={'placeholder': 'Segundo Apellido'}))
    sexo = forms.ChoiceField(choices=SEXO, label='Sexo',
                             widget=forms.Select(attrs={'required': True}))
    fecNac = forms.DateField(label='Fec. Nacimiento',
                             widget=forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA', 'format': '%d/%m/%y'})
                             )
    edonac = forms.ChoiceField(
        choices=EDOSNAC, label='Estado de Nacimiento',
        widget=forms.Select(attrs={'required': True})
        )
    curp = forms.CharField(max_length=18, label='CURP:',
                           widget=forms.TextInput(attrs={'placeholder': 'Clave Única de Registro de Población'})
                           )
    telLocal = forms.CharField(max_length=30, label='Teléfono Local',
                               widget=forms.TextInput(attrs={'placeholder': '(XXX)XXX-XX-XX'})
                               )
    telCel = forms.CharField(max_length=30, label='Teléfono Celular',
                             widget=forms.TextInput(attrs={'placeholder': '(XXX)XXX-XX-XX'})
                             )
    email = forms.EmailField(max_length=150,label='Correo Electrónico',
                             widget=forms.EmailInput(attrs={'placeholder': 'correo@dominio.ext'})
                             )
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
    vialidad = forms.CharField(max_length=50, label='Vialidad:',
                               widget=forms.TextInput(attrs={'placeholder': 'Nombre de la calle, andador o camino'})
                               )
    numExterior = forms.CharField(max_length=8, label='Número Exterior:',
                                  widget=forms.TextInput(attrs={'placeholder': 'Número exterior del domicilio'})
                                  )
    numInterior = forms.CharField(max_length=8, label='Número Interior:',
                                  widget=forms.TextInput(attrs={'placeholder': 'Número interior del domicilio'})
                                  )
    codpost = forms.IntegerField(label='Código Postal:')
    referencia = forms.CharField(widget=forms.TextInput, label='Referencia:')
    idcatpadron=forms.ModelChoiceField(label='Padron', queryset=CAT_PADRONES.objects.all(),)

