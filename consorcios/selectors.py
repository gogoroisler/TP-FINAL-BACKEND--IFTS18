from django.utils import timezone
from .models import Departamento, Titularidad, SolicitudVinculacion


def get_departamento_por_usuario(usuario):
    return Departamento.objects.filter(usuario=usuario).first()


def get_titularidad_activa(usuario):
    hoy = timezone.now().date()
    return Titularidad.objects.filter(
        usuario=usuario,
        fecha_desde__lte=hoy,
        fecha_hasta__isnull=True
    ).first()


def get_departamento_por_titularidad(usuario):
    titularidad = get_titularidad_activa(usuario)
    if titularidad:
        return titularidad.departamento
    return None


def get_titular_en_periodo(departamento, fecha):
    return Titularidad.objects.filter(
        departamento=departamento,
        fecha_desde__lte=fecha,
        fecha_hasta__isnull=True
    ).first()


def get_solicitud_por_usuario(usuario):
    return SolicitudVinculacion.objects.filter(
        usuario=usuario
    ).order_by('-fecha').first()


def get_todas_las_solicitudes():
    return SolicitudVinculacion.objects.all().order_by('-fecha')


def get_solicitudes_pendientes():
    return SolicitudVinculacion.objects.filter(
        estado='pendiente'
    ).order_by('-fecha')

def get_titularidad_activa_por_departamento(departamento):
    return Titularidad.objects.filter(
        departamento=departamento,
        fecha_hasta__isnull=True
    ).first()

def get_titularidades_activas_por_departamento(departamento):
    return Titularidad.objects.filter(
        departamento=departamento,
        fecha_hasta__isnull=True
    )


def get_todos_los_consorcios():
    from .models import Consorcio
    return Consorcio.objects.all().order_by('nombre')


def get_todos_los_departamentos():
    return Departamento.objects.all().order_by('consorcio', 'numero')


def get_todas_las_titularidades():
    return Titularidad.objects.all().select_related('departamento', 'usuario').order_by('departamento__consorcio', 'departamento__numero')
