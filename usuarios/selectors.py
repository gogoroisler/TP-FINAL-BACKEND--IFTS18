from .models import Perfil


def get_perfil_por_usuario(usuario):
    try:
        return Perfil.objects.get(usuario=usuario)
    except Perfil.DoesNotExist:
        return None
