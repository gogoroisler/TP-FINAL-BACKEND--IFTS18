from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from .models import Perfil, Expensa, Departamento
from .forms import ExpensaForm



def home(request):
    return render(request, 'home.html')


# Vista exclusiva para administradores
@login_required
def panel_admin(request):

    perfil = Perfil.objects.get(usuario=request.user)

# Verifica que el usuario sea administrador
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')

    return render(request, 'panel_admin.html')


# Vista exclusiva para consorcistas
@login_required
def panel_consorcista(request):

    perfil = Perfil.objects.get(usuario=request.user)

# Verifica que el usuario sea consorcista
    if perfil.rol != 'consorcista':
        return render(request, 'sin_permiso.html')

    return render(request, 'panel_consorcista.html')


# Muestra únicamente las expensas del usuario logueado
@login_required
def mis_expensas(request):

    departamento = Departamento.objects.get(usuario=request.user)
    
# Obtiene únicamente las expensas del departamento del usuario
    expensas = Expensa.objects.filter(
        departamento=departamento
    )

    return render(
        request,
        'mis_expensas.html',
        {'expensas': expensas}
    )

# Permite al administrador visualizar todas las expensas
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

# Permite al administrador crear nuevas expensas
@login_required
def crear_expensa(request):

    perfil = Perfil.objects.get(usuario=request.user)

    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')

    if request.method == 'POST':

        form = ExpensaForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('listar_expensas')

    else:

        form = ExpensaForm()

    return render(
        request,
        'crear_expensa.html',
        {'form': form}
    )

# Permite modificar una expensa existente
@login_required
def editar_expensa(request, expensa_id):

    perfil = Perfil.objects.get(usuario=request.user)

    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')

    expensa = get_object_or_404(
        Expensa,
        id=expensa_id
    )

    if request.method == 'POST':

        form = ExpensaForm(
            request.POST,
            instance=expensa
        )

        if form.is_valid():

            form.save()

            return redirect('listar_expensas')

    else:

        form = ExpensaForm(instance=expensa)

    return render(
        request,
        'editar_expensa.html',
        {
            'form': form,
            'expensa': expensa
        }
    )

# Permite eliminar expensas del sistema
@login_required
def eliminar_expensa(request, expensa_id):

    perfil = Perfil.objects.get(usuario=request.user)

    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')

    expensa = get_object_or_404(
        Expensa,
        id=expensa_id
    )

    if request.method == 'POST':

        expensa.delete()

        return redirect('listar_expensas')

    return render(
        request,
        'eliminar_expensa.html',
        {'expensa': expensa}
    )