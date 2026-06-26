from .models import Reclamo


def get_reclamos_por_usuario(usuario):
    return Reclamo.objects.filter(usuario=usuario).order_by('-fecha_creacion')


def get_todos_los_reclamos():
    return Reclamo.objects.select_related('departamento__consorcio', 'usuario').order_by('-fecha_creacion')


def get_reclamo_por_id(reclamo_id):
    return Reclamo.objects.get(id=reclamo_id)
