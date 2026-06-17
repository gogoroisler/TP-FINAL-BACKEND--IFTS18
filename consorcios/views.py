from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from consorcios.selectors import get_departamento_por_titularidad, get_departamento_por_usuario
from expensas.selectors import get_expensas_por_departamento
from expensas.models import Expensa


@method_decorator(login_required, name='dispatch')
class MisExpensasView(ListView):
    model = Expensa
    template_name = 'mis_expensas.html'
    context_object_name = 'expensas'

    def get_queryset(self):
        # Primero busca por titularidad activa
        departamento = get_departamento_por_titularidad(self.request.user)
        # Si no tiene titularidad, cae al campo usuario directo
        if not departamento:
            departamento = get_departamento_por_usuario(self.request.user)
        if departamento:
            return get_expensas_por_departamento(departamento)
        return Expensa.objects.none()
