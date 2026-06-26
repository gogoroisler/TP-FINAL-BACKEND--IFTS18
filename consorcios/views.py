from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from consorcios.models import Consorcio, Departamento, Titularidad, SolicitudVinculacion
from consorcios.selectors import (
    get_titularidad_activa_por_departamento,
    get_titularidades_activas_por_departamento,
    get_departamento_por_titularidad,
    get_departamento_por_usuario,
    get_solicitud_por_usuario,
    get_todas_las_solicitudes,
    get_todos_los_consorcios,
    get_todos_los_departamentos,
    get_todas_las_titularidades,
)
from expensas.models import Expensa
from expensas.selectors import get_expensas_por_departamento, get_pagos_por_expensa, get_credito_disponible
from usuarios.mixins import RolRequeridoMixin
from usuarios.selectors import get_perfil_por_usuario


@method_decorator(login_required, name='dispatch')
class MisExpensasView(RolRequeridoMixin, ListView):
    rol_requerido = 'consorcista'
    model = Expensa
    template_name = 'mis_expensas.html'
    context_object_name = 'expensas'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if response.status_code != 200:
            return response
        solicitud = get_solicitud_por_usuario(request.user)
        if solicitud is None:
            return redirect('crear_solicitud')
        if solicitud.estado == 'pendiente':
            return render(request, 'solicitud_pendiente.html', {'solicitud': solicitud})
        if solicitud.estado == 'rechazada':
            return render(request, 'solicitud_rechazada.html', {'solicitud': solicitud})
        return response

    def get_queryset(self):
        departamento = get_departamento_por_titularidad(self.request.user)
        if not departamento:
            departamento = get_departamento_por_usuario(self.request.user)
        if departamento:
            return get_expensas_por_departamento(departamento)
        return Expensa.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departamento = get_departamento_por_titularidad(self.request.user)
        if not departamento:
            departamento = get_departamento_por_usuario(self.request.user)
        context['departamento'] = departamento
        credito_restante = get_credito_disponible(departamento) if departamento else 0
        expensas_con_pagos = []
        for expensa in context['expensas']:
            saldo = expensa.saldo_pendiente
            if saldo > 0 and credito_restante > 0:
                credito_aplicado = min(credito_restante, saldo)
                credito_restante -= credito_aplicado
                monto_a_pagar = saldo - credito_aplicado
            else:
                credito_aplicado = 0
                monto_a_pagar = max(saldo, 0)
            expensas_con_pagos.append({
                'expensa': expensa,
                'pagos': get_pagos_por_expensa(expensa),
                'credito_aplicado': credito_aplicado,
                'monto_a_pagar': monto_a_pagar,
            })
        context['expensas_con_pagos'] = expensas_con_pagos
        return context


@method_decorator(login_required, name='dispatch')
class CrearSolicitudView(RolRequeridoMixin, CreateView):
    rol_requerido = 'consorcista'
    model = SolicitudVinculacion
    template_name = 'crear_solicitud.html'
    fields = ['departamento', 'condicion']
    success_url = reverse_lazy('mis_expensas')

    def dispatch(self, request, *args, **kwargs):
        solicitud = get_solicitud_por_usuario(request.user)
        if solicitud is not None and solicitud.estado != 'rechazada':
            return redirect('mis_expensas')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        SolicitudVinculacion.objects.filter(
            usuario=self.request.user,
            estado='rechazada'
        ).delete()
        form.instance.usuario = self.request.user
        form.instance.consorcio = form.cleaned_data['departamento'].consorcio
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ListarSolicitudesView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = SolicitudVinculacion
    template_name = 'listar_solicitudes.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        return get_todas_las_solicitudes()


@login_required
def informar_pago(request, expensa_id):
    perfil = get_perfil_por_usuario(request.user)
    if perfil is None:
        return render(request, 'sin_perfil.html')
    expensa = get_object_or_404(Expensa, id=expensa_id)
    if request.method == 'POST':
        from expensas.models import Pago
        monto = request.POST.get('monto', expensa.monto)
        nota = request.POST.get('nota', '')
        Pago.objects.create(expensa=expensa, monto=monto, nota=nota)
    return redirect('mis_expensas')


@login_required
def gestionar_solicitud(request, solicitud_id):
    perfil = get_perfil_por_usuario(request.user)
    if perfil is None:
        return render(request, 'sin_perfil.html')
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')
    solicitud = get_object_or_404(SolicitudVinculacion, id=solicitud_id)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        nota_admin = request.POST.get('nota_admin', '')
        if accion == 'aprobar':
            titular_activo = get_titularidad_activa_por_departamento(solicitud.departamento)
            if titular_activo:
                # Hay conflicto: mostrar aviso en la lista
                solicitudes = get_todas_las_solicitudes()
                return render(request, 'listar_solicitudes.html', {
                    'solicitudes': solicitudes,
                    'conflicto_solicitud_id': solicitud.id,
                    'titular_activo': titular_activo,
                    'nota_admin': nota_admin,
                })
            # Sin conflicto: aprobar directamente
            solicitud.estado = 'aprobada'
            solicitud.nota_admin = nota_admin
            solicitud.save()
            Titularidad.objects.create(
                departamento=solicitud.departamento,
                usuario=solicitud.usuario,
                fecha_desde=timezone.now().date(),
            )
        elif accion == 'aprobar_reemplazar':
            # Cierra titularidad anterior y crea la nueva
            Titularidad.objects.filter(
                departamento=solicitud.departamento,
                fecha_hasta__isnull=True
            ).update(fecha_hasta=timezone.now().date())
            solicitud.estado = 'aprobada'
            solicitud.nota_admin = nota_admin
            solicitud.save()
            Titularidad.objects.create(
                departamento=solicitud.departamento,
                usuario=solicitud.usuario,
                fecha_desde=timezone.now().date(),
            )
        elif accion == 'aprobar_agregar':
            # Mantiene titular anterior y agrega el nuevo
            solicitud.estado = 'aprobada'
            solicitud.nota_admin = nota_admin
            solicitud.save()
            Titularidad.objects.create(
                departamento=solicitud.departamento,
                usuario=solicitud.usuario,
                fecha_desde=timezone.now().date(),
            )
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
            solicitud.nota_admin = nota_admin
            solicitud.save()
    return redirect('listar_solicitudes')


@method_decorator(login_required, name='dispatch')
class ListarConsorciosView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = Consorcio
    template_name = 'consorcios/listar.html'
    context_object_name = 'consorcios'

    def get_queryset(self):
        return get_todos_los_consorcios()


@method_decorator(login_required, name='dispatch')
class CrearConsorcioView(RolRequeridoMixin, CreateView):
    rol_requerido = 'admin'
    model = Consorcio
    template_name = 'consorcios/crear.html'
    fields = ['nombre', 'direccion', 'cuit', 'telefono', 'email']
    success_url = reverse_lazy('listar_consorcios')


@method_decorator(login_required, name='dispatch')
class EditarConsorcioView(RolRequeridoMixin, UpdateView):
    rol_requerido = 'admin'
    model = Consorcio
    template_name = 'consorcios/editar.html'
    fields = ['nombre', 'direccion', 'cuit', 'telefono', 'email']
    success_url = reverse_lazy('listar_consorcios')
    pk_url_kwarg = 'consorcio_id'


@method_decorator(login_required, name='dispatch')
class EliminarConsorcioView(RolRequeridoMixin, DeleteView):
    rol_requerido = 'admin'
    model = Consorcio
    template_name = 'consorcios/eliminar.html'
    success_url = reverse_lazy('listar_consorcios')
    pk_url_kwarg = 'consorcio_id'


@method_decorator(login_required, name='dispatch')
class ListarDepartamentosView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = Departamento
    template_name = 'departamentos/listar.html'
    context_object_name = 'departamentos'

    def get_queryset(self):
        return get_todos_los_departamentos()


@method_decorator(login_required, name='dispatch')
class CrearDepartamentoView(RolRequeridoMixin, CreateView):
    rol_requerido = 'admin'
    model = Departamento
    template_name = 'departamentos/crear.html'
    fields = ['consorcio', 'numero', 'piso', 'propietario', 'metros_cuadrados']
    success_url = reverse_lazy('listar_departamentos')


@method_decorator(login_required, name='dispatch')
class EditarDepartamentoView(RolRequeridoMixin, UpdateView):
    rol_requerido = 'admin'
    model = Departamento
    template_name = 'departamentos/editar.html'
    fields = ['consorcio', 'numero', 'piso', 'propietario', 'metros_cuadrados']
    success_url = reverse_lazy('listar_departamentos')
    pk_url_kwarg = 'departamento_id'


@method_decorator(login_required, name='dispatch')
class EliminarDepartamentoView(RolRequeridoMixin, DeleteView):
    rol_requerido = 'admin'
    model = Departamento
    template_name = 'departamentos/eliminar.html'
    success_url = reverse_lazy('listar_departamentos')
    pk_url_kwarg = 'departamento_id'


@method_decorator(login_required, name='dispatch')
class ListarTitularidadesView(RolRequeridoMixin, ListView):
    rol_requerido = 'admin'
    model = Titularidad
    template_name = 'titularidades/listar.html'
    context_object_name = 'titularidades'

    def get_queryset(self):
        return get_todas_las_titularidades()


@method_decorator(login_required, name='dispatch')
class CrearTitularidadView(RolRequeridoMixin, CreateView):
    rol_requerido = 'admin'
    model = Titularidad
    template_name = 'titularidades/crear.html'
    fields = ['departamento', 'usuario', 'fecha_desde', 'fecha_hasta']
    success_url = reverse_lazy('listar_titularidades')


@method_decorator(login_required, name='dispatch')
class EditarTitularidadView(RolRequeridoMixin, UpdateView):
    rol_requerido = 'admin'
    model = Titularidad
    template_name = 'titularidades/editar.html'
    fields = ['departamento', 'usuario', 'fecha_desde', 'fecha_hasta']
    success_url = reverse_lazy('listar_titularidades')
    pk_url_kwarg = 'titularidad_id'


@method_decorator(login_required, name='dispatch')
class EliminarTitularidadView(RolRequeridoMixin, DeleteView):
    rol_requerido = 'admin'
    model = Titularidad
    template_name = 'titularidades/eliminar.html'
    success_url = reverse_lazy('listar_titularidades')
    pk_url_kwarg = 'titularidad_id'


@login_required
def retirar_permisos(request, solicitud_id):
    perfil = get_perfil_por_usuario(request.user)
    if perfil is None:
        return render(request, 'sin_perfil.html')
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')
    solicitud = get_object_or_404(SolicitudVinculacion, id=solicitud_id)
    if request.method == 'POST':
        nota_admin = request.POST.get('nota_admin', 'Permisos retirados por el administrador')
        titularidad_id = request.POST.get('titularidad_id')
        if titularidad_id:
            # Retira permisos solo al titular seleccionado
            Titularidad.objects.filter(
                id=titularidad_id,
                fecha_hasta__isnull=True
            ).update(fecha_hasta=timezone.now().date())
        else:
            # Cierra todas las titularidades activas del depto
            Titularidad.objects.filter(
                usuario=solicitud.usuario,
                departamento=solicitud.departamento,
                fecha_hasta__isnull=True
            ).update(fecha_hasta=timezone.now().date())
        # Verifica si quedan titularidades activas en el depto
        titularidades_restantes = get_titularidades_activas_por_departamento(solicitud.departamento)
        if not titularidades_restantes.exists():
            solicitud.estado = 'rechazada'
            solicitud.nota_admin = nota_admin
            solicitud.save()
    return redirect('listar_solicitudes')
