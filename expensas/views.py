from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from usuarios.selectors import get_perfil_por_usuario
from .models import Expensa
from .selectors import (
    get_todas_las_expensas,
    get_gastos_por_consorcio_periodo,
    generar_preview_periodo,
)


@method_decorator(login_required, name='dispatch')
class ListarExpensasView(ListView):
    model = Expensa
    template_name = 'listar_expensas.html'
    context_object_name = 'expensas'

    def dispatch(self, request, *args, **kwargs):
        perfil = get_perfil_por_usuario(request.user)
        if perfil.rol != 'admin':
            return render(request, 'sin_permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return get_todas_las_expensas()


@method_decorator(login_required, name='dispatch')
class DetalleExpensaView(DetailView):
    model = Expensa
    template_name = 'detalle_expensa.html'
    context_object_name = 'expensa'
    pk_url_kwarg = 'expensa_id'

    def dispatch(self, request, *args, **kwargs):
        perfil = get_perfil_por_usuario(request.user)
        if perfil.rol != 'admin':
            return render(request, 'sin_permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expensa = self.object
        gastos = get_gastos_por_consorcio_periodo(
            expensa.departamento.consorcio,
            expensa.periodo
        )
        context['gastos'] = gastos
        return context


@method_decorator(login_required, name='dispatch')
class CrearExpensaView(CreateView):
    model = Expensa
    template_name = 'crear_expensa.html'
    fields = ['departamento', 'periodo', 'fecha_vencimiento']
    success_url = reverse_lazy('listar_expensas')

    def dispatch(self, request, *args, **kwargs):
        perfil = get_perfil_por_usuario(request.user)
        if perfil.rol != 'admin':
            return render(request, 'sin_permiso.html')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class EditarExpensaView(UpdateView):
    model = Expensa
    template_name = 'editar_expensa.html'
    fields = ['departamento', 'periodo', 'fecha_vencimiento', 'pagada']
    success_url = reverse_lazy('listar_expensas')
    pk_url_kwarg = 'expensa_id'

    def dispatch(self, request, *args, **kwargs):
        perfil = get_perfil_por_usuario(request.user)
        if perfil.rol != 'admin':
            return render(request, 'sin_permiso.html')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class EliminarExpensaView(DeleteView):
    model = Expensa
    template_name = 'eliminar_expensa.html'
    success_url = reverse_lazy('listar_expensas')
    pk_url_kwarg = 'expensa_id'

    def dispatch(self, request, *args, **kwargs):
        perfil = get_perfil_por_usuario(request.user)
        if perfil.rol != 'admin':
            return render(request, 'sin_permiso.html')
        return super().dispatch(request, *args, **kwargs)
