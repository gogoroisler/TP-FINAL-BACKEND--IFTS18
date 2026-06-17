from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from consorcios.selectors import get_departamento_por_titularidad, get_departamento_por_usuario
from expensas.models import Expensa, Pago
from expensas.selectors import get_expensas_por_departamento, get_pagos_por_expensa
from usuarios.mixins import RolRequeridoMixin
from usuarios.selectors import get_perfil_por_usuario


@method_decorator(login_required, name='dispatch')
class MisExpensasView(RolRequeridoMixin, ListView):
    rol_requerido = 'consorcista'
    model = Expensa
    template_name = 'mis_expensas.html'
    context_object_name = 'expensas'

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


@login_required
def informar_pago(request, expensa_id):
    perfil = get_perfil_por_usuario(request.user)
    if perfil is None:
        return render(request, 'sin_perfil.html')
    expensa = get_object_or_404(Expensa, id=expensa_id)
    if request.method == 'POST':
        monto = request.POST.get('monto', expensa.monto)
        nota = request.POST.get('nota', '')
        Pago.objects.create(
            expensa=expensa,
            monto=monto,
            nota=nota,
        )
        expensa.pagada = True
        expensa.save()
    return redirect('mis_expensas')
