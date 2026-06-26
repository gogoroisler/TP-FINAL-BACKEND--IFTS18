from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from consorcios.selectors import get_departamento_por_titularidad, get_todos_los_consorcios
from usuarios.mixins import RolRequeridoMixin
from usuarios.selectors import get_perfil_por_usuario
from .models import Reclamo
from .selectors import get_reclamos_por_usuario, get_todos_los_reclamos


@method_decorator(login_required, name='dispatch')
class CrearReclamoView(RolRequeridoMixin, CreateView):
    rol_requerido = 'consorcista'
    model = Reclamo
    template_name = 'reclamos/crear_reclamo.html'
    fields = ['titulo', 'descripcion']
    success_url = reverse_lazy('mis_reclamos')

    def form_valid(self, form):
        departamento = get_departamento_por_titularidad(self.request.user)
        if not departamento:
            form.add_error(None, 'No tenés un departamento asignado. Solicitá vinculación antes de crear un reclamo.')
            return self.form_invalid(form)
        form.instance.usuario = self.request.user
        form.instance.departamento = departamento
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class MisReclamosView(RolRequeridoMixin, ListView):
    rol_requerido = 'consorcista'
    model = Reclamo
    template_name = 'reclamos/mis_reclamos.html'
    context_object_name = 'reclamos'

    def get_queryset(self):
        return get_reclamos_por_usuario(self.request.user)


@method_decorator(login_required, name='dispatch')
class ListarReclamosView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = Reclamo
    template_name = 'reclamos/listar_reclamos.html'
    context_object_name = 'reclamos'

    def get_queryset(self):
        qs = get_todos_los_reclamos()
        consorcio_id = self.request.GET.get('consorcio_id')
        estado = self.request.GET.get('estado')
        if consorcio_id:
            qs = qs.filter(departamento__consorcio_id=consorcio_id)
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consorcios'] = get_todos_los_consorcios()
        context['estados'] = Reclamo.ESTADO_CHOICES
        context['consorcio_id_seleccionado'] = self.request.GET.get('consorcio_id', '')
        context['estado_seleccionado'] = self.request.GET.get('estado', '')
        return context


@login_required
def actualizar_estado(request, reclamo_id):
    perfil = get_perfil_por_usuario(request.user)
    if perfil is None:
        return render(request, 'sin_perfil.html')
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)
    if request.method == 'POST':
        estado = request.POST.get('estado')
        reclamo.estado = estado
        reclamo.save()
    return redirect('listar_reclamos')
