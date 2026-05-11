from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Perfil, Expensa, Departamento



def home(request):
    return render(request, 'home.html')


@login_required
def panel_admin(request):

    perfil = Perfil.objects.get(usuario=request.user)

    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')

    return render(request, 'panel_admin.html')


@login_required
def panel_consorcista(request):

    perfil = Perfil.objects.get(usuario=request.user)

    if perfil.rol != 'consorcista':
        return render(request, 'sin_permiso.html')

    return render(request, 'panel_consorcista.html')

@login_required
def mis_expensas(request):

    departamento = Departamento.objects.get(usuario=request.user)

    expensas = Expensa.objects.filter(
        departamento=departamento
    )

    return render(
        request,
        'mis_expensas.html',
        {'expensas': expensas}
    )


@login_required
def listar_expensas(request):

    perfil = Perfil.objects.get(usuario=request.user)

    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')

    expensas = Expensa.objects.all()

    return render(
        request,
        'listar_expensas.html',
        {'expensas': expensas}
    )