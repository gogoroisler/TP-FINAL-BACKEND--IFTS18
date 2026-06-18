from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from consorcios.models import Consorcio, Titularidad, SolicitudVinculacion
from consorcios.selectors import (
    get_departamento_por_titularidad,
    get_departamento_por_usuario,
    get_solicitud_por_usuario,
    get_todas_las_solicitudes,
)
from expensas.models import Expensa
from expensas.selectors import get_expensas_por_departamento, get_pagos_por_expensa
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
        expensas_con_pagos = []
        for expensa in context['expensas']:
            expensas_con_pagos.append({
                'expensa': expensa,
                'pagos': get_pagos_por_expensa(expensa),
            })
        context['expensas_con_pagos'] = expensas_con_pagos
        return context


@method_decorator(login_required, name='dispatch')
class CrearSolicitudView(RolRequeridoMixin, CreateView):
    rol_requerido = 'consorcista'
    model = SolicitudVinculacion
    template_name = 'crear_solicitud.html'
    fields = ['consorcio', 'departamento']
    success_url = reverse_lazy('mis_expensas')

    def dispatch(self, request, *args, **kwargs):
        solicitud = get_solicitud_por_usuario(request.user)
        if solicitud is not None and solicitud.estado != 'rechazada':
            return redirect('mis_expensas')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Borra solicitud rechazada anterior si existe
        SolicitudVinculacion.objects.filter(
            usuario=self.request.user,
            estado='rechazada'
        ).delete()
        form.instance.usuario = self.request.user
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
        expensa.pagada = True
        expensa.save()
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


@login_required
def retirar_permisos(request, solicitud_id):
    perfil = get_perfil_por_usuario(request.user)
    if perfil is None:
        return render(request, 'sin_perfil.html')
    if perfil.rol != 'admin':
        return render(request, 'sin_permiso.html')
    solicitud = get_object_or_404(SolicitudVinculacion, id=solicitud_id)
    if request.method == 'POST':
        # Cierra la titularidad activa
        Titularidad.objects.filter(
            usuario=solicitud.usuario,
            departamento=solicitud.departamento,
            fecha_hasta__isnull=True
        ).update(fecha_hasta=timezone.now().date())
        # Marca la solicitud como rechazada
        solicitud.estado = 'rechazada'
        solicitud.nota_admin = request.POST.get('nota_admin', 'Permisos retirados por el administrador')
        solicitud.save()
    return redirect('listar_solicitudes')
