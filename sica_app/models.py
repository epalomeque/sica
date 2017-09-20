from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CAT_PADRONES(models.Model):
    nombre=models.CharField(max_length=150)
    descripcion=models.TextField()
    estatus=models.BinaryField()

    def __unicode__(Self):
        return Self.nombre

class CAT_ESTATUS(models.Model):
    nombre=models.CharField(max_length=20)
    descripcion=models.TextField()
    def __unicode__(Self):
        return Self.nombre


class CAT_ASUNTOS(models.Model):
    idTipo=models.IntegerField()
    nbtipo=models.CharField(max_length=60)
    idSubTipo=models.IntegerField()
    nbSubtipo=models.CharField(max_length=60)
    def __unicode__(Self):
        return '%s | %s'%(Self.nbtipo, Self.nbSubtipo)

class MEDIOS(models.Model):
    nombre=models.CharField(max_length=150)
    descripcion=models.TextField()
    def __unicode__(Self):
        return '%s'%(Self.nombre)

class ORIGEN_CEDULA(models.Model):
    nombre=models.CharField(max_length=150)
    medio=models.ForeignKey(MEDIOS,blank=True)
    descripcion=models.TextField()
    def __unicode__(Self):
        return '%s'%(Self.nombre)


class PERSONA_DATOS(models.Model):
    SEXO = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )

    nombre=models.CharField(max_length=150)
    primApellido=models.CharField(max_length=150)
    segApellido=models.CharField(max_length=150)
    fecNac = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO)

    def __unicode__(Self):
        return Self.nombre


class PERSONA_CONTACTO(models.Model):
    telLocal=models.CharField(max_length=30, verbose_name='Telefono Local')
    telCelular=models.CharField(max_length=30)
    email=models.CharField(max_length=150)


class CAT_ESTADO(models.Model):
    idEstado=models.CharField(max_length=2)
    nomEstado=models.CharField(max_length=150)

    def __unicode__(Self):
        return '%s'%(Self.nomEstado)


class CAT_MUNICIPIO(models.Model):
    idEstado=models.ForeignKey(CAT_ESTADO)
    idmunicipio=models.CharField(max_length=3)
    nomMunicipio=models.CharField(max_length=150)

    def __unicode__(Self):
        return '%s' %(Self.nomMunicipio)


class CAT_LOCALIDAD(models.Model):
    idMunicipio=models.ForeignKey(CAT_MUNICIPIO)
    idlocalidad=models.CharField(max_length=4)
    nomLocalidad=models.CharField(max_length=150)

    def __unicode__(Self):
        return '%s' % (Self.nomLocalidad)


class PERSONA_DOMICILIO(models.Model):
    id_localidad=models.ForeignKey(CAT_LOCALIDAD)
    vialidad=models.CharField(max_length=150)
    numExterior=models.CharField(max_length=8)
    numInterior=models.CharField(max_length=8)
    codpost=models.IntegerField()
    referencia=models.TextField()



class INFO_PERSONA(models.Model):
    idPadron=models.ForeignKey(CAT_PADRONES)
    idPersona=models.CharField(max_length=10)
    idDatos=models.ForeignKey(PERSONA_DATOS,blank=True,default=0,null=True)
    idContacto=models.ForeignKey(PERSONA_CONTACTO,blank=True,default=0,null=True)
    iddomicilio=models.ForeignKey(PERSONA_DOMICILIO,blank=True,default=0,null=True)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in INFO_PERSONA._meta.fields]


class OFICIOREL(models.Model):
    fecha=models.DateField()
    descripcion=models.TextField()
    idOficio=models.CharField(max_length=100)
    docAnexos=models.FileField()


class CEDULA(models.Model):
    estatus=models.ForeignKey(CAT_ESTATUS)
    origen=models.ForeignKey(ORIGEN_CEDULA)
    fechCreacion=models.DateField()
    fechCierre=models.DateField(blank=True,null=True)
    asgeneral=models.ForeignKey(CAT_ASUNTOS)
    asdetalle=models.TextField()
    DatInteresado=models.ForeignKey(INFO_PERSONA)
    respuesta=models.TextField()
    Of_respuesta=models.ForeignKey(OFICIOREL,related_name='respuestaoficio',blank=True,null=True)
    Of_turnado=models.ForeignKey(OFICIOREL,related_name='turnadooficio',blank=True,null=True)
    eseguimiento=models.ForeignKey(User,related_name='eseguimiento',blank=True,null=True)
    ulevantamiento=models.ForeignKey(User,related_name='ulevantamiento')
    uatencion=models.ForeignKey(User,related_name='uatencion',blank=True,null=True)
    observacion=models.TextField()




class ProgCorazonAmigo(models.Model):
    folio = models.IntegerField(primary_key=True)
    curp = models.CharField(max_length=20, blank=True, null=True)
    folio_elec = models.CharField(max_length=20, blank=True, null=True)
    gral_ocr = models.CharField(max_length=20, blank=True, null=True)
    fecinsert = models.DateTimeField(blank=True, null=True)
    fecreg = models.DateField(blank=True, null=True)
    fecnac = models.DateField(blank=True, null=True)
    appaterno = models.CharField(max_length=50)
    apmaterno = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    edocivil = models.CharField(max_length=1, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    municipio = models.IntegerField()
    cvelocal = models.IntegerField()
    calleynum = models.CharField(max_length=100, blank=True, null=True)
    ref_dir_sol = models.CharField(max_length=500, blank=True, null=True)
    doc_presenta = models.CharField(max_length=1, blank=True, null=True)
    obs_gral = models.CharField(max_length=500, blank=True, null=True)
    etapa = models.IntegerField(blank=True, null=True)
    rep_appaterno = models.CharField(max_length=30, blank=True, null=True)
    rep_apmaterno = models.CharField(max_length=30, blank=True, null=True)
    rep_nombre = models.CharField(max_length=30, blank=True, null=True)
    rep_sexo = models.CharField(max_length=1, blank=True, null=True)
    rep_fecnac = models.DateTimeField(blank=True, null=True)
    rep_tel = models.CharField(max_length=20, blank=True, null=True)
    rep_municipio = models.IntegerField(blank=True, null=True)
    rep_cvelocal = models.IntegerField(blank=True, null=True)
    rep_calleynum = models.CharField(max_length=100, blank=True, null=True)
    ref_dir_rep = models.CharField(max_length=500, blank=True, null=True)
    rep_doc_presenta = models.CharField(max_length=1, blank=True, null=True)
    fecrecepcion = models.DateTimeField(blank=True, null=True)
    fecdemanda = models.DateTimeField(blank=True, null=True)
    fecevaluacion = models.DateTimeField(blank=True, null=True)
    nombredr = models.CharField(max_length=60, blank=True, null=True)
    efdescrip = models.CharField(max_length=500, blank=True, null=True)
    doc_sreg_o = models.CharField(max_length=1, blank=True, null=True)
    reg_crleg_o = models.CharField(max_length=1, blank=True, null=True)
    reg_efun_o = models.CharField(max_length=1, blank=True, null=True)
    reg_tcen_o = models.CharField(max_length=1, blank=True, null=True)
    sol_anac_c = models.CharField(max_length=1, blank=True, null=True)
    sol_ife_c = models.CharField(max_length=1, blank=True, null=True)
    sol_cdom_c = models.CharField(max_length=1, blank=True, null=True)
    rep_anac_c = models.CharField(max_length=1, blank=True, null=True)
    rep_ife_c = models.CharField(max_length=1, blank=True, null=True)
    rep_cdom_c = models.CharField(max_length=1, blank=True, null=True)
    viv_compartida = models.CharField(max_length=1, blank=True, null=True)
    viv_piso = models.CharField(max_length=1, blank=True, null=True)
    viv_paredes = models.CharField(max_length=1, blank=True, null=True)
    viv_techos = models.CharField(max_length=1, blank=True, null=True)
    viv_ncuartos = models.IntegerField(blank=True, null=True)
    viv_ncdormir = models.IntegerField(blank=True, null=True)
    viv_cocina = models.CharField(max_length=1, blank=True, null=True)
    viv_fogon = models.CharField(max_length=1, blank=True, null=True)
    viv_estufa = models.CharField(max_length=1, blank=True, null=True)
    viv_aguaentub = models.CharField(max_length=1, blank=True, null=True)
    viv_pozo = models.CharField(max_length=1, blank=True, null=True)
    viv_pipa = models.CharField(max_length=1, blank=True, null=True)
    viv_rios = models.CharField(max_length=1, blank=True, null=True)
    viv_aguautil = models.CharField(max_length=1, blank=True, null=True)
    viv_dexcretas = models.CharField(max_length=1, blank=True, null=True)
    viv_ebasura = models.CharField(max_length=1, blank=True, null=True)
    viv_elect = models.CharField(max_length=1, blank=True, null=True)
    viv_radio = models.CharField(max_length=1, blank=True, null=True)
    viv_tv = models.CharField(max_length=1, blank=True, null=True)
    viv_refri = models.CharField(max_length=1, blank=True, null=True)
    evf_servsalud = models.CharField(max_length=1, blank=True, null=True)
    evf_segpop = models.CharField(max_length=1, blank=True, null=True)
    evf_nescolar = models.CharField(max_length=1, blank=True, null=True)
    evf_dmotriz = models.CharField(max_length=1, blank=True, null=True)
    evf_dvisual = models.CharField(max_length=1, blank=True, null=True)
    evf_dauditiva = models.CharField(max_length=1, blank=True, null=True)
    evf_dlenguaje = models.CharField(max_length=1, blank=True, null=True)
    evf_dmental = models.CharField(max_length=1, blank=True, null=True)
    evf_dotra = models.CharField(max_length=100, blank=True, null=True)
    evf_lalimentacion = models.IntegerField(blank=True, null=True)
    evf_laseopers = models.IntegerField(blank=True, null=True)
    evf_ltraslado = models.IntegerField(blank=True, null=True)
    evf_lcomunicacion = models.IntegerField(blank=True, null=True)
    evf_lvestido = models.IntegerField(blank=True, null=True)
    th = models.DecimalField(max_digits=9, decimal_places=0)
    tm = models.IntegerField()
    cnta = models.CharField(max_length=16, blank=True, null=True)
    feccancel = models.DateTimeField(blank=True, null=True)
    txtsolmunicipio = models.CharField(max_length=50, blank=True, null=True)
    txtsollocalidad = models.CharField(max_length=100, blank=True, null=True)
    txtrepmunicipio = models.CharField(max_length=50, blank=True, null=True)
    txtreplocalidad = models.CharField(max_length=100, blank=True, null=True)
    latsol = models.FloatField(blank=True, null=True)
    lonsol = models.FloatField(blank=True, null=True)
    latrep = models.FloatField(blank=True, null=True)
    lonrep = models.FloatField(blank=True, null=True)
    viv_encuestador = models.CharField(max_length=100, blank=True, null=True)
    viv_fecencuesta = models.DateTimeField(blank=True, null=True)
    motivo_cancel = models.CharField(max_length=2, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    acomentario = models.CharField(max_length=255, blank=True, null=True)
    tincidencia = models.SmallIntegerField(blank=True, null=True)
    numhabitantes = models.SmallIntegerField()
    jsuser = models.CharField(max_length=30)
    paquete = models.IntegerField()
    nominaid = models.DecimalField(max_digits=9, decimal_places=0, blank=True, null=True)
    estudiante = models.CharField(max_length=1)
    empleado = models.CharField(max_length=1)
    mesaid = models.SmallIntegerField(blank=True, null=True)
    sol_curp = models.CharField(max_length=1, blank=True, null=True)
    ceduladr = models.CharField(max_length=7, blank=True, null=True)
    viv_propiedad = models.CharField(max_length=1, blank=True, null=True)
    sueldoben = models.FloatField(blank=True, null=True)
    empleadorep = models.CharField(max_length=1, blank=True, null=True)
    sueldorep = models.FloatField(blank=True, null=True)
    noempleado = models.CharField(max_length=1, blank=True, null=True)
    versionca = models.CharField(max_length=1, blank=True, null=True)
    cuentabanco = models.CharField(max_length=10, blank=True, null=True)
    unidadsalud = models.CharField(max_length=15, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prog_corazon_amigo'