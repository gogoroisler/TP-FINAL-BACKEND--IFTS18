from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .selectors import get_perfil_por_usuario


@login_required
def redirigir_segun_rol(request):
    perfil = get_perfil_por_usuario(request.user)
    if perfil is None:
        return redirect('home')
    if perfil.rol == 'admin':
        return redirect('panel_admin')
    if perfil.rol == 'consorcista':
        return redirect('mis_expensas')
    return redirect('home')
