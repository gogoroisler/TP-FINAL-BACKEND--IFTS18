from django import forms as django_forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from consorcios.models import Consorcio, Departamento
from consorcios.selectors import get_todos_los_consorcios, get_todos_los_departamentos
from usuarios.mixins import RolRequeridoMixin
from usuarios.selectors import get_perfil_por_usuario
from .models import Expensa, Proveedor, GastoConsorcio
from .selectors import (
    get_todas_las_expensas,
    get_gastos_por_consorcio_periodo,
    generar_preview_periodo,
    calcular_monto_departamento,
    get_todos_los_proveedores,
    get_todos_los_gastos,
)


@method_decorator(login_required, name='dispatch')
class ListarExpensasView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = Expensa
    template_name = 'listar_expensas.html'
    context_object_name = 'expensas'

    def get_queryset(self):
        qs = get_todas_las_expensas()
        consorcio_id = self.request.GET.get('consorcio_id')
        periodo = self.request.GET.get('periodo')
        departamento_id = self.request.GET.get('departamento_id')
        if consorcio_id:
            qs = qs.filter(departamento__consorcio_id=consorcio_id)
        if periodo:
            qs = qs.filter(periodo=periodo)
        if departamento_id:
            qs = qs.filter(departamento_id=departamento_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consorcio_id = self.request.GET.get('consorcio_id', '')
        context['consorcios'] = get_todos_los_consorcios()
        context['periodos'] = (
            Expensa.objects.values_list('periodo', flat=True)
            .distinct().order_by('-periodo')
        )
        context['departamentos'] = (
            Departamento.objects.filter(consorcio_id=consorcio_id).order_by('numero')
            if consorcio_id
            else get_todos_los_departamentos()
        )
        context['consorcio_id_seleccionado'] = consorcio_id
        context['periodo_seleccionado'] = self.request.GET.get('periodo', '')
        context['departamento_id_seleccionado'] = self.request.GET.get('departamento_id', '')
        return context


@method_decorator(login_required, name='dispatch')
class DetalleExpensaView(RolRequeridoMixin, DetailView):
    rol_requerido = 'admin'
    model = Expensa
    template_name = 'detalle_expensa.html'
    context_object_name = 'expensa'
    pk_url_kwarg = 'expensa_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gastos = get_gastos_por_consorcio_periodo(
            self.object.departamento.consorcio,
            self.object.periodo
        )
        context['gastos'] = gastos
        return context


@method_decorator(login_required, name='dispatch')
class CrearExpensaView(RolRequeridoMixin, CreateView):
    rol_requerido = 'admin'
    model = Expensa
    template_name = 'crear_expensa.html'
    fields = ['departamento', 'periodo', 'fecha_vencimiento']
    success_url = reverse_lazy('listar_expensas')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['periodo'].widget = django_forms.TextInput(attrs={'type': 'month'})
        return form


@method_decorator(login_required, name='dispatch')
class EditarExpensaView(RolRequeridoMixin, UpdateView):
    rol_requerido = 'admin'
    model = Expensa
    template_name = 'editar_expensa.html'
    fields = ['departamento', 'periodo', 'fecha_vencimiento', 'pagada']
    success_url = reverse_lazy('listar_expensas')
    pk_url_kwarg = 'expensa_id'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['periodo'].widget = django_forms.TextInput(attrs={'type': 'month'})
        return form


@method_decorator(login_required, name='dispatch')
class EliminarExpensaView(RolRequeridoMixin, DeleteView):
    rol_requerido = 'admin'
    model = Expensa
    template_name = 'eliminar_expensa.html'
    success_url = reverse_lazy('listar_expensas')
    pk_url_kwarg = 'expensa_id'


@method_decorator(login_required, name='dispatch')
class SeleccionarPreviewView(RolRequeridoMixin, TemplateView):
    rol_requerido = 'admin'
    template_name = 'seleccionar_preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consorcios'] = Consorcio.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        consorcio_id = request.GET.get('consorcio_id')
        periodo = request.GET.get('periodo')
        if consorcio_id and periodo:
            from django.shortcuts import redirect
            return redirect('preview_periodo', consorcio_id=consorcio_id, periodo=periodo)
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class PreviewPeriodoView(RolRequeridoMixin, TemplateView):
    rol_requerido = 'admin'
    template_name = 'preview_periodo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consorcio_id = self.kwargs.get('consorcio_id')
        periodo = self.kwargs.get('periodo')
        consorcio = Consorcio.objects.get(id=consorcio_id)
        context['preview'] = generar_preview_periodo(consorcio, periodo)
        context['consorcio_id'] = consorcio_id
        context['periodo'] = periodo
        return context


@method_decorator(login_required, name='dispatch')
class ListarProveedoresView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = Proveedor
    template_name = 'proveedores/listar.html'
    context_object_name = 'proveedores'

    def get_queryset(self):
        return get_todos_los_proveedores()


@method_decorator(login_required, name='dispatch')
class CrearProveedorView(RolRequeridoMixin, CreateView):
    rol_requerido = 'admin'
    model = Proveedor
    template_name = 'proveedores/crear.html'
    fields = ['nombre', 'cuit', 'rubro']
    success_url = reverse_lazy('listar_proveedores')


@method_decorator(login_required, name='dispatch')
class EditarProveedorView(RolRequeridoMixin, UpdateView):
    rol_requerido = 'admin'
    model = Proveedor
    template_name = 'proveedores/editar.html'
    fields = ['nombre', 'cuit', 'rubro']
    success_url = reverse_lazy('listar_proveedores')
    pk_url_kwarg = 'proveedor_id'


@method_decorator(login_required, name='dispatch')
class EliminarProveedorView(RolRequeridoMixin, DeleteView):
    rol_requerido = 'admin'
    model = Proveedor
    template_name = 'proveedores/eliminar.html'
    success_url = reverse_lazy('listar_proveedores')
    pk_url_kwarg = 'proveedor_id'


@method_decorator(login_required, name='dispatch')
class ListarGastosView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = GastoConsorcio
    template_name = 'gastos/listar.html'
    context_object_name = 'gastos'

    def get_queryset(self):
        qs = get_todos_los_gastos()
        consorcio_id = self.request.GET.get('consorcio_id')
        proveedor_id = self.request.GET.get('proveedor_id')
        periodo = self.request.GET.get('periodo')
        if consorcio_id:
            qs = qs.filter(consorcio_id=consorcio_id)
        if proveedor_id:
            qs = qs.filter(proveedor_id=proveedor_id)
        if periodo:
            qs = qs.filter(periodo=periodo)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consorcios'] = get_todos_los_consorcios()
        context['proveedores'] = get_todos_los_proveedores()
        context['periodos'] = (
            GastoConsorcio.objects.values_list('periodo', flat=True)
            .distinct().order_by('-periodo')
        )
        context['consorcio_id_seleccionado'] = self.request.GET.get('consorcio_id', '')
        context['proveedor_id_seleccionado'] = self.request.GET.get('proveedor_id', '')
        context['periodo_seleccionado'] = self.request.GET.get('periodo', '')
        return context


@method_decorator(login_required, name='dispatch')
class CrearGastoView(RolRequeridoMixin, CreateView):
    rol_requerido = 'admin'
    model = GastoConsorcio
    template_name = 'gastos/crear.html'
    fields = ['consorcio', 'proveedor', 'periodo', 'descripcion', 'monto', 'tipo', 'alcance', 'prorrateo', 'departamentos']
    success_url = reverse_lazy('listar_gastos')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['periodo'].widget = django_forms.TextInput(attrs={'type': 'month'})
        return form


@method_decorator(login_required, name='dispatch')
class EditarGastoView(RolRequeridoMixin, UpdateView):
    rol_requerido = 'admin'
    model = GastoConsorcio
    template_name = 'gastos/editar.html'
    fields = ['consorcio', 'proveedor', 'periodo', 'descripcion', 'monto', 'tipo', 'alcance', 'prorrateo', 'departamentos']
    success_url = reverse_lazy('listar_gastos')
    pk_url_kwarg = 'gasto_id'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['periodo'].widget = django_forms.TextInput(attrs={'type': 'month'})
        return form


@method_decorator(login_required, name='dispatch')
class EliminarGastoView(RolRequeridoMixin, DeleteView):
    rol_requerido = 'admin'
    model = GastoConsorcio
    template_name = 'gastos/eliminar.html'
    success_url = reverse_lazy('listar_gastos')
    pk_url_kwarg = 'gasto_id'


@login_required
def enviar_expensas(request, consorcio_id, periodo):
    perfil = get_perfil_por_usuario(request.user)
    if perfil is None:
        return render(request, 'sin_perfil.html')
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')

    if request.method == 'POST':
        consorcio = Consorcio.objects.get(id=consorcio_id)
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        deptos = consorcio.departamento_set.all()

        for depto in deptos:
            monto = calcular_monto_departamento(depto, periodo)
            Expensa.objects.update_or_create(
                departamento=depto,
                periodo=periodo,
                defaults={
                    'monto': monto,
                    'fecha_vencimiento': fecha_vencimiento,
                    'publicada': True,
                }
            )
        return redirect('listar_expensas')

    return redirect('listar_expensas')
