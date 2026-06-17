from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from consorcios.selectors import get_departamento_por_titularidad, get_departamento_por_usuario
from expensas.selectors import get_expensas_por_departamento, get_resumen_gastos_periodo
from expensas.models import Expensa


@method_decorator(login_required, name='dispatch')
class MisExpensasView(ListView):
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
        return context


@login_required
def informar_pago(request, expensa_id):
    expensa = get_object_or_404(Expensa, id=expensa_id)
    if request.method == 'POST':
        expensa.pagada = True
        expensa.save()
    return redirect('mis_expensas')
