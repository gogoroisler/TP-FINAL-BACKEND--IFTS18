from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from consorcios.models import Titularidad, Departamento
from consorcios.selectors import get_todos_los_consorcios, get_todos_los_departamentos
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
        qs = get_todos_los_usuarios().select_related('perfil')
        rol = self.request.GET.get('rol')
        consorcio_id = self.request.GET.get('consorcio_id')
        departamento_id = self.request.GET.get('departamento_id')
        if rol == 'admin':
            qs = qs.filter(perfil__rol='admin')
        elif rol == 'consorcista':
            qs = qs.filter(perfil__rol='consorcista')
        elif rol == 'sin_perfil':
            qs = qs.filter(perfil__isnull=True)
        if consorcio_id:
            qs = qs.filter(
                titularidad__departamento__consorcio_id=consorcio_id,
                titularidad__fecha_hasta__isnull=True
            ).distinct()
        if departamento_id:
            qs = qs.filter(
                titularidad__departamento_id=departamento_id,
                titularidad__fecha_hasta__isnull=True
            ).distinct()
        return qs.prefetch_related(
            Prefetch(
                'titularidad_set',
                queryset=Titularidad.objects.filter(fecha_hasta__isnull=True)
                    .select_related('departamento__consorcio'),
                to_attr='titularidades_activas'
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consorcio_id = self.request.GET.get('consorcio_id', '')
        context['consorcios'] = get_todos_los_consorcios()
        context['departamentos'] = (
            Departamento.objects.filter(consorcio_id=consorcio_id).order_by('numero')
            if consorcio_id
            else get_todos_los_departamentos()
        )
        context['rol_seleccionado'] = self.request.GET.get('rol', '')
        context['consorcio_id_seleccionado'] = consorcio_id
        context['departamento_id_seleccionado'] = self.request.GET.get('departamento_id', '')
        return context


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
