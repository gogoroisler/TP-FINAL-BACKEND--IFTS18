from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from consorcios.selectors import get_departamento_por_titularidad, get_todos_los_consorcios
from usuarios.mixins import RolRequeridoMixin
from usuarios.selectors import get_perfil_por_usuario
from .models import Aviso
from .selectors import get_avisos_activos_por_consorcio, get_todos_los_avisos


@method_decorator(login_required, name='dispatch')
class ListarAvisosAdminView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = Aviso
    template_name = 'avisos/listar_avisos_admin.html'
    context_object_name = 'avisos'

    def get_queryset(self):
        qs = get_todos_los_avisos()
        consorcio_id = self.request.GET.get('consorcio_id')
        if consorcio_id:
            qs = qs.filter(consorcio_id=consorcio_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consorcios'] = get_todos_los_consorcios()
        context['consorcio_id_seleccionado'] = self.request.GET.get('consorcio_id', '')
        return context


@method_decorator(login_required, name='dispatch')
class CrearAvisoView(RolRequeridoMixin, CreateView):
    rol_requerido = 'admin'
    model = Aviso
    template_name = 'avisos/crear_aviso.html'
    fields = ['consorcio', 'titulo', 'contenido']
    success_url = reverse_lazy('listar_avisos_admin')


@method_decorator(login_required, name='dispatch')
class EditarAvisoView(RolRequeridoMixin, UpdateView):
    rol_requerido = 'admin'
    model = Aviso
    template_name = 'avisos/editar_aviso.html'
    fields = ['titulo', 'contenido', 'activo']
    success_url = reverse_lazy('listar_avisos_admin')
    pk_url_kwarg = 'aviso_id'


@method_decorator(login_required, name='dispatch')
class MisAvisosView(RolRequeridoMixin, ListView):
    rol_requerido = 'consorcista'
    model = Aviso
    template_name = 'avisos/mis_avisos.html'
    context_object_name = 'avisos'

    def get_queryset(self):
        departamento = get_departamento_por_titularidad(self.request.user)
        if departamento:
            return get_avisos_activos_por_consorcio(departamento.consorcio)
        return Aviso.objects.none()
