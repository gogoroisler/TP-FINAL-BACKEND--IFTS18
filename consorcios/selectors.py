from .models import Departamento, Titularidad
from django.utils import timezone


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
    ).filter(
        fecha_hasta__isnull=True
    ).first()
