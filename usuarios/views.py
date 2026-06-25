from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import Perfil
from .selectors import get_perfil_por_usuario


def registro(request):
    if request.user.is_authenticated:
        return redirect('redirigir_segun_rol')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(usuario=user, rol='consorcista')
            login(request, user)
            return redirect('panel_consorcista')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


@login_required
def redirigir_segun_rol(request):
    perfil = get_perfil_por_usuario(request.user)
    if perfil is None:
        return redirect('home')
    if perfil.rol == 'admin':
        return redirect('panel_admin')
    if perfil.rol == 'consorcista':
        return redirect('panel_consorcista')
    return redirect('home')
