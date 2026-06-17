from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.selectors import get_perfil_por_usuario
from consorcios.selectors import get_departamento_por_usuario
from expensas.selectors import (
    get_todas_las_expensas,
    get_expensas_por_departamento,
)
from expensas.models import Expensa
from .forms import ExpensaForm


def home(request):
    return render(request, 'home.html')


@login_required
def panel_admin(request):
    perfil = get_perfil_por_usuario(request.user)
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')
    return render(request, 'panel_admin.html')


@login_required
def panel_consorcista(request):
    perfil = get_perfil_por_usuario(request.user)
    if perfil.rol != 'consorcista':
        return render(request, 'sin_permiso.html')
    return render(request, 'panel_consorcista.html')


@login_required
def mis_expensas(request):
    departamento = get_departamento_por_usuario(request.user)
    expensas = get_expensas_por_departamento(departamento)
    return render(request, 'mis_expensas.html', {'expensas': expensas})


@login_required
def listar_expensas(request):
    perfil = get_perfil_por_usuario(request.user)
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')
    expensas = get_todas_las_expensas()
    return render(request, 'listar_expensas.html', {'expensas': expensas})


@login_required
def crear_expensa(request):
    perfil = get_perfil_por_usuario(request.user)
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')
    if request.method == 'POST':
        form = ExpensaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_expensas')
    else:
        form = ExpensaForm()
    return render(request, 'crear_expensa.html', {'form': form})


@login_required
def editar_expensa(request, expensa_id):
    perfil = get_perfil_por_usuario(request.user)
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')
    expensa = get_object_or_404(Expensa, id=expensa_id)
    if request.method == 'POST':
        form = ExpensaForm(request.POST, instance=expensa)
        if form.is_valid():
            form.save()
            return redirect('listar_expensas')
    else:
        form = ExpensaForm(instance=expensa)
    return render(request, 'editar_expensa.html', {'form': form, 'expensa': expensa})


@login_required
def eliminar_expensa(request, expensa_id):
    perfil = get_perfil_por_usuario(request.user)
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')
    expensa = get_object_or_404(Expensa, id=expensa_id)
    if request.method == 'POST':
        expensa.delete()
        return redirect('listar_expensas')
    return render(request, 'eliminar_expensa.html', {'expensa': expensa})
