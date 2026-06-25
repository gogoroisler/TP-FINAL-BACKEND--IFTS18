from .models import Aviso


def get_avisos_activos_por_consorcio(consorcio):
    return Aviso.objects.filter(
        consorcio=consorcio,
        activo=True
    ).order_by('-fecha')


def get_todos_los_avisos_por_consorcio(consorcio):
    return Aviso.objects.filter(
        consorcio=consorcio
    ).order_by('-fecha')


def get_todos_los_avisos():
    return Aviso.objects.all().order_by('-fecha')
