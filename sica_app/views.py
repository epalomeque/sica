#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_text, force_text, smart_bytes
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from django.core.serializers.json import DjangoJSONEncoder
from models import ProgCorazonAmigo, CAT_ESTADO, CAT_MUNICIPIO,CAT_LOCALIDAD, PERSONA_DOMICILIO, PERSONA_CONTACTO, \
                    PERSONA_DATOS, INFO_PERSONA, CAT_PADRONES, CEDULA
from forms import Busquedaform, cedulaforms, datospersonaExiste, datospersonaNoexiste, FormEstado, FormMunicipio, \
                    FormLocalidad, formBuscar


# Create your views here.
def validarNone(valor) :
    valorFinal = ''
    valor = str(valor)

    if valor == None or valor == 'None' or valor.strip() == '' or valor == '-1':
        valorFinal = 'Sin Información'
    else:
        valorFinal = valor.strip()

    return valorFinal


def status2txt(status):
    txtstatus = ''
    if status == 1:
        txtstatus = 'Comite'
    elif status == 2:
        txtstatus = 'Aprobado'
    elif status == 3:
        txtstatus = 'No aprobado'
    elif status == 4:
        txtstatus = 'Rechazado'
    elif status == 5:
        txtstatus = 'Cancelado'
    elif status == 6:
        txtstatus = 'Fallecido'
    elif status == 7:
        txtstatus = 'Suspendido'
    elif status == 8:
        txtstatus = 'Revalorado Aprobado'
    elif status == 9:
        txtstatus = 'Revalorado No Aprobado'
    return txtstatus


def anio2txtanio(anio):
    anio = str(anio)
    txtanio = ''

    if anio == '1':
        txtanio = '2014'
    elif anio == '2':
        txtanio = '2015'
    elif anio == '3':
        txtanio = '2016'
    elif anio == '4':
        txtanio = '2017'

    return txtanio


def sexo2text(sexo):
    sexo = str(sexo)
    txtsexo = ''

    if sexo == 'F': # si es Femenino
        txtsexo = 'Mujer'
    elif sexo == 'M': # si es Masculino
        txtsexo = 'Hombre'

    return txtsexo


def cambiaMunicipio(request):

    if request.method == 'GET':
        post_text = request.GET.get('the_post')
        actmunicipio = list(CAT_MUNICIPIO.objects.filter(idEstado__idEstado=post_text))
        data = serializers.serialize("json", actmunicipio )

        return HttpResponse(data,content_type='application/json')

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def cambiaLocalidad(request):

    if request.method == 'GET':
        #print 'menso'
        #print request.GET
        #print 'toy aqui'
        post_text = request.GET.get('the_post')
        #print 'post_text -> %s'% post_text
        edo_actual= request.GET.get('estado_actual')
        #print edo_actual
        #listamunicipio = list(CAT_MUNICIPIO.objects.filter(idEstado__idEstado=post_text))

        #actlocalidad = list(CAT_LOCALIDAD.objects.filter(idMunicipio__idmunicipio=post_text, idMunicipio__idEstado__idEstado=edo_actual ))
        actlocalidad = list(CAT_LOCALIDAD.objects.filter(idMunicipio=post_text,
                                                         idMunicipio__idEstado__idEstado=edo_actual))
        #print actlocalidad
        data = serializers.serialize("json", actlocalidad,fields=('pk','nomLocalidad'))
        #print 'data  -> %s' % data

        #actmunicipio = CAT_MUNICIPIO.objects.all().values()
        return HttpResponse(data,content_type='application/json')

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def guardaRegistroPersona( regcedula = None ):
    if regcedula:
        datos_persona = PERSONA_DATOS(
            nombre=regcedula['nombre'].value(),
            primApellido=regcedula['primApellido'].value(),
            segApellido=regcedula['segApellido'].value(),
            fecNac=regcedula['fecNac'].value(),
            sexo=regcedula['sexo'].value()
        )
        datos_persona.save()

        contacto_persona = PERSONA_CONTACTO(
            telLocal=regcedula['telLocal'].value(),
            telCelular=regcedula['telCel'].value(),
            email=regcedula['email'].value()
        )
        contacto_persona.save()

        domicilio_persona = PERSONA_DOMICILIO(
            id_localidad=CAT_LOCALIDAD.objects.get(pk=int(regcedula['localidad'].value())),
            vialidad=regcedula['vialidad'].value(),
            numExterior=regcedula['numExterior'].value(),
            numInterior=regcedula['numInterior'].value(),
            codpost=regcedula['codpost'].value(),
            referencia=regcedula['referencia'].value()
        )
        domicilio_persona.save()

        persona_info = INFO_PERSONA(
            idPadron=CAT_PADRONES.objects.get(pk=int(regcedula['idcatpadron'].value())),
            idPersona='',
            idDatos=PERSONA_DATOS.objects.get(pk=int(datos_persona.pk)),
            idContacto=PERSONA_CONTACTO.objects.get(pk=int(contacto_persona.pk)),
            iddomicilio=PERSONA_DOMICILIO.objects.get(pk=int(domicilio_persona.pk)),
        )
        persona_info.save()
        print 'persona_info.pk --> %s'%(persona_info.pk)

    else:
        print 'EL FORMULARIO NO CONTENIA DATOS'

    return int(persona_info.pk)


def buscaFolioCorazonAmigo(folio):
    resbusqueda = ProgCorazonAmigo.objects.using('corazon_amigo').filter(folio=folio)
    if resbusqueda:
        return resbusqueda
    else:
        return False


def buscaFolioCedulaAtencion(folio):
    return False


def busquedaXNombreCA(cdbusqueda):
    busqueda = smart_text(cdbusqueda, encoding='utf-8', strings_only=False, errors='strict')
    print busqueda

    rawquery = "select r.FOLIO, r.VERSIONCA, r.TXTSOLMUNICIPIO, r.REP_SEXO, r.STATUS, " \
               "r.FECREG, r.NOMBRE, r.APPATERNO, r.APMATERNO from PROG_CORAZON_AMIGO r " \
               "where r.NOMBRE || ' ' || r.APPATERNO || ' ' || r.APMATERNO LIKE '%"+busqueda.upper()+"%' " \
               "order by r.STATUS, r.APPATERNO"

    print rawquery

    queryset = ProgCorazonAmigo.objects.using('corazon_amigo').\
        raw(smart_text(rawquery, encoding='utf-8', strings_only=False, errors='strict'))

    c = 0
    for i in queryset:
        c+=1

    if c > 0:
        return queryset
    else:
        return False


def busquedaXNombreCdA(busqueda):
    return False


def vistaformularios(request):
    userdata = {
        'usuario': request.user,
        'CatEstado': FormEstado,
        'CatMunicipio':FormMunicipio,
        'Catlocalidad':FormLocalidad
    }



    return render(request, 'formularios.html',userdata)


# Inician vistas para navegaciòn del sistema
@login_required()
def viewBuscar(request):
    fBuscar = ''
    busqueda = ''
    resultadoCA = ''
    resultadoCdA = ''
    countresultadosCA = 0
    countresultadosCdA = 0

    if request.method == 'POST':
        fBuscar = formBuscar(request.POST, prefix='busq')
        if fBuscar.is_valid():
            busqueda = fBuscar['busqueda'].value()

    # La busqueda a realizar es por folio de padron o folio de cedula
    if busqueda.isdigit():
        resultadoCA = buscaFolioCorazonAmigo(busqueda)
        if resultadoCA:
            countresultadosCA = len(resultadoCA)
        resultadoCdA = buscaFolioCedulaAtencion(busqueda)
        if resultadoCdA:
            countresultadosCdA = len(resultadoCdA)

    # La busqueda a realizar es por nombre del beneficiario o curp
    else:
        resultadoCA = busquedaXNombreCA(busqueda.upper())
        if resultadoCA:
            for i in resultadoCA:
                countresultadosCA += 1
        resultadoCdA = busquedaXNombreCdA(busqueda.upper())
        if resultadoCdA:
            countresultadosCdA = len(resultadoCdA)

    userdata = {
        'usuario': request.user,
        'fBuscar': fBuscar,
        'busqueda': smart_text(busqueda.upper()),
        'resultadoCdA': resultadoCdA,
        'resultadoCA': resultadoCA,
        'countresultadosCA': countresultadosCA,
        'countresultadosCdA': countresultadosCdA
    }

    return render(request, 'buscar.html', userdata)


@login_required()
def home(request):
    # cdbusqueda=''
    # cdfiltro=''
    # resbusqueda=''
    # datos_busq={}
    # busqueda = ''
    # cedulaForms = ''
    # elGET = ''
    # nohayregistro = False
    fBuscar = formBuscar(prefix='busq')

    ## Valida el metodo de la peticion (POST o GET)
    # if request.method == 'POST':
    #
    #     # Valida que el formulario haya sido enviado
    #     if 'busq' in request.POST:
    #         # print 'entre busqueda gil'
    #         busqueda = formBuscar(request.POST,prefix='busq')
    #
    #         elGET = True
    #
    #         if busqueda.is_valid():
    #             cdbusqueda = busqueda['CD_busqueda'].value()
    #             cdfiltro = busqueda['CD_filtro'].value()
    #
    #             # Busqueda en blanco
    #             if cdfiltro == '4':
    #                 print 'Filtro 4 | Ninguna busqueda'
    #                 resbusqueda = ''
    #
    #             # Busqueda por folio de padron
    #             if cdfiltro == '3':
    #                 resbusqueda = ProgCorazonAmigo.objects.using('corazon_amigo').filter(folio=cdbusqueda)
    #                 #print len(resbusqueda)
    #                 if len(resbusqueda) >0:
    #                     for registro in resbusqueda:
    #
    #                         datos_busq = {
    #                             'folio': {'valor': validarNone(registro.folio),
    #                                       'etiqueta': 'Folio:'},
    #                             'appaterno': {'valor': validarNone(registro.appaterno),
    #                                           'etiqueta': 'Apellido Paterno: '},
    #                             'apmaterno': {'valor': validarNone(registro.apmaterno),
    #                                           'etiqueta': 'Apellido Materno: '},
    #                             'nombre': {'valor': validarNone(registro.nombre),
    #                                        'etiqueta': 'Nombre: '},
    #                             'sexo': {'valor': validarNone(sexo2text(registro.sexo)),
    #                                      'etiqueta': 'Sexo: '},
    #                             'tel': {'valor': validarNone(registro.tel),
    #                                     'etiqueta': 'Teléfono: '},
    #                             'cvelocal': {'valor': validarNone(registro.cvelocal),
    #                                          'etiqueta': 'Localidad: '},
    #                             'calleynum': {'valor': validarNone(registro.calleynum),
    #                                           'etiqueta': 'Calle y número: '},
    #                             'etapa': {'valor': validarNone(registro.etapa),
    #                                       'etiqueta': 'Etapa: '},
    #                             'curp': {'valor': validarNone(registro.curp),
    #                                       'etiqueta': 'CURP: '},
    #                             'fecnac': {'valor': validarNone(registro.fecnac),
    #                                       'etiqueta': 'Fecha de Nacimiento: '},
    #                             'rep_appaterno': {'valor': validarNone(registro.rep_appaterno),
    #                                               'etiqueta': 'Apellido Paterno: '},
    #                             'rep_apmaterno': {'valor': validarNone(registro.rep_apmaterno),
    #                                               'etiqueta': 'Apellido Materno: '},
    #                             'rep_nombre': {'valor': validarNone(registro.rep_nombre),
    #                                            'etiqueta': 'Nombre: '},
    #                             'rep_sexo': {'valor': validarNone(sexo2text(registro.rep_sexo)),
    #                                          'etiqueta': 'Sexo: '},
    #                             'rep_fecnac': {'valor': validarNone(registro.rep_fecnac),
    #                                            'etiqueta': 'Fecha de Nacimiento:'},
    #                             'rep_tel': {'valor': validarNone(registro.rep_tel),
    #                                         'etiqueta': 'Teléfono: '},
    #                             'rep_municipio': {'valor': validarNone(registro.rep_municipio),
    #                                               'etiqueta': 'Municipio: '},
    #                             'rep_cvelocal': {'valor': validarNone(registro.rep_cvelocal),
    #                                              'etiqueta': 'Localidad: '},
    #                             'rep_calleynum': {'valor': validarNone(registro.rep_calleynum),
    #                                               'etiqueta': 'Calle y número: '},
    #                             'txtsolmunicipio': {'valor': validarNone(registro.txtsolmunicipio),
    #                                                 'etiqueta': 'Municipio: '},
    #                             'txtsollocalidad': {'valor': validarNone(registro.txtsollocalidad),
    #                                                 'etiqueta': 'Localidad: '},
    #                             'txtrepmunicipio': {'valor': validarNone(registro.txtrepmunicipio),
    #                                                 'etiqueta': 'Municpio: '},
    #                             'txtreplocalidad': {'valor': validarNone(registro.txtreplocalidad),
    #                                                 'etiqueta': 'Localidad: '},
    #                             'acomentario': {'valor': validarNone(registro.acomentario),
    #                                             'etiqueta': 'Comentario: '},
    #                             'paquete': {'valor': validarNone(registro.paquete),
    #                                         'etiqueta': 'Paquete: '},
    #                             'status': {'valor': validarNone(status2txt(registro.status)),
    #                                        'etiqueta': 'Estatus'},
    #                             'anio': {'valor': validarNone(anio2txtanio(registro.versionca)),
    #                                      'etiqueta': 'Versión C.A'},
    #                         }
    #
    #                 else:
    #                     nohayregistro=True
    #
    #             # Busqueda por folio de cedula
    #             elif cdfiltro == '2':
    #                 resbusqueda = CEDULA.objects.filter(pk=cdbusqueda)
    #
    #                 if len(resbusqueda) >0:
    #                     print 'Si hay registros'
    #                     for registro in resbusqueda:
    #                         datos_busq = registro
    #                 else:
    #                     print 'No hay registros'
    #                     nohayregistro=True
    #
    #             # Busqueda por nombre del demandante
    #             elif cdfiltro == '1':
    #                 resbusqueda = BusquedaXNombre(cdbusqueda)
    #
    #                 for i in resbusqueda:
    #                     print (
    #                     i.folio, i.status, smart_text(i.nombre, encoding='utf-8', strings_only=False, errors='strict'),
    #                     smart_text(i.appaterno, encoding='utf-8', strings_only=False, errors='strict'),
    #                     smart_text(i.apmaterno, encoding='utf-8', strings_only=False, errors='strict'))
    #
    #
    #     elif 'cedula' in request.POST:
    #         elGET = True
    #         cedulaForms = cedulaforms(request.POST, prefix='cedula')
    #
    #
    # elif request.method == 'GET':
    #     busqueda = formBuscar(prefix='busq')
    #
    # else:
    #     print 'Ni post ni get'
    ##

    userdata = {
        'usuario': request.user,
        'fBuscar': fBuscar,
        # 'cdbusqueda': cdbusqueda,
        # 'cdfiltro': cdfiltro,
        # 'resbusqueda': resbusqueda,
        # 'datos_busq': datos_busq,
        # 'cedulaForms': cedulaForms,
        # 'elGET': elGET,
        # 'DPN': datospersonaNoexiste(),
        # 'DPE': datospersonaExiste(),
        # 'sinregistro': nohayregistro
    }

    # print userdata

    return render(request, 'home.html', userdata)


@login_required()
def viewCedula(request, paso=''):
    datousuario = ''
    userdata = {}
    if not paso:
        paso = '1'

    print 'request.method --> %s '% request.method
    print 'paso --> %s | tipo --> %s'% (paso, type(paso))

    if request.method == 'GET':
        print '----- GET ----- y paso %s' % paso
        userdata = {
            'usuario': request.user,
            'regcedula': datospersonaNoexiste(),
            'paso':paso
        }

    elif request.method == 'POST':
        if paso == '2':
            regcedula = datospersonaNoexiste(request.POST)

            if regcedula.is_valid() :
                # CREAR VARIABLES QUE INSTANCIE A LOS MODELOS CORRESPONDIENTES y ASIGNAR LOS CAMPOS CORRESPONDIENTES DE CADA MODELO
                pkUsuario = guardaRegistroPersona(regcedula)
                print 'registro guardado con id --> %s' % pkUsuario
                datousuario = INFO_PERSONA.objects.get(pk=pkUsuario)
                print 'datousuario --> %s' % datousuario

                userdata = {
                    'usuario': request.user,
                    'datousuario': datousuario,
                    'cedulaNueva': cedulaforms(initial={'DatInteresado':datousuario,
                                                        'fechCreacion':datetime.now(),
                                                        'fechCierre': '',
                                                        'ulevantamiento': request.user,
                                                        'Of_respuesta': '',
                                                        'Of_turnado': ''
                                                        }),
                    'paso':paso
                }

        elif paso == '3':
            cedula = cedulaforms(request.POST)

            if cedula.is_valid():
                lacedula = cedula.save()

                print 'Cedula salvada'
                print lacedula

                print 'Datos del interesado ID --> %s' % cedula['DatInteresado'].value()
                #datoUsuario =


            userdata = {
                'usuario': request.user,
                'datousuario': INFO_PERSONA.objects.get( pk=cedula['DatInteresado'].value() ),
                'cedula': lacedula,
                'paso': paso
            }


    return render(request, 'crearcedula.html', userdata)


@login_required()
def viewRegistro(request, padron, folio):
    print padron
    print folio
    registro = ProgCorazonAmigo.objects.using('corazon_amigo').filter(folio=folio)

    print registro[0].folio, registro[0].nombre, registro[0].appaterno, registro[0].apmaterno

    return True