from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import RegistroForm
from .models import Perfil
from .selectors import get_perfil_por_usuario, get_todos_los_perfiles, get_todos_los_usuarios
from usuarios.mixins import RolRequeridoMixin


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


@method_decorator(login_required, name='dispatch')
class ListarPerfilesView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = Perfil
    template_name = 'perfiles/listar.html'
    context_object_name = 'perfiles'

    def get_queryset(self):
        return get_todos_los_perfiles()


@method_decorator(login_required, name='dispatch')
class CrearPerfilView(RolRequeridoMixin, CreateView):
    rol_requerido = 'admin'
    model = Perfil
    template_name = 'perfiles/crear.html'
    fields = ['usuario', 'rol']
    success_url = reverse_lazy('listar_perfiles')


@method_decorator(login_required, name='dispatch')
class EditarPerfilView(RolRequeridoMixin, UpdateView):
    rol_requerido = 'admin'
    model = Perfil
    template_name = 'perfiles/editar.html'
    fields = ['usuario', 'rol']
    success_url = reverse_lazy('listar_perfiles')
    pk_url_kwarg = 'perfil_id'


@method_decorator(login_required, name='dispatch')
class EliminarPerfilView(RolRequeridoMixin, DeleteView):
    rol_requerido = 'admin'
    model = Perfil
    template_name = 'perfiles/eliminar.html'
    success_url = reverse_lazy('listar_perfiles')
    pk_url_kwarg = 'perfil_id'


@method_decorator(login_required, name='dispatch')
class ListarUsuariosView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = User
    template_name = 'usuarios_admin/listar.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return get_todos_los_usuarios()


@method_decorator(login_required, name='dispatch')
class CrearUsuarioView(RolRequeridoMixin, CreateView):
    rol_requerido = 'admin'
    model = User
    template_name = 'usuarios_admin/crear.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('listar_usuarios')


@method_decorator(login_required, name='dispatch')
class EditarUsuarioView(RolRequeridoMixin, UpdateView):
    rol_requerido = 'admin'
    model = User
    template_name = 'usuarios_admin/editar.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
    success_url = reverse_lazy('listar_usuarios')
    pk_url_kwarg = 'usuario_id'


@method_decorator(login_required, name='dispatch')
class EliminarUsuarioView(RolRequeridoMixin, DeleteView):
    rol_requerido = 'admin'
    model = User
    template_name = 'usuarios_admin/eliminar.html'
    success_url = reverse_lazy('listar_usuarios')
    pk_url_kwarg = 'usuario_id'
