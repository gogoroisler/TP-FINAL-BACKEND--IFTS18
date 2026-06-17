from .models import Departamento, Titularidad


def get_departamento_por_usuario(usuario):
    return Departamento.objects.filter(usuario=usuario).first()


def get_titularidad_activa(departamento):
    return Titularidad.objects.filter(
        departamento=departamento,
        fecha_hasta__isnull=True
    )
