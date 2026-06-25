from django.contrib.auth.models import User
from .models import Perfil


def get_perfil_por_usuario(usuario):
    try:
        return Perfil.objects.get(usuario=usuario)
    except Perfil.DoesNotExist:
        return None


def get_todos_los_perfiles():
    return Perfil.objects.all().select_related('usuario').order_by('usuario__username')


def get_todos_los_usuarios():
    return User.objects.all().select_related('perfil').order_by('username')
