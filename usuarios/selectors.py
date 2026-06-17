from .models import Perfil


def get_perfil_por_usuario(usuario):
    return Perfil.objects.get(usuario=usuario)
