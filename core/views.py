from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from usuarios.mixins import RolRequeridoMixin


def home(request):
    return render(request, 'home.html')


@method_decorator(login_required, name='dispatch')
class PanelAdminView(RolRequeridoMixin, TemplateView):
    rol_requerido = 'admin'
    template_name = 'panel_admin.html'


@method_decorator(login_required, name='dispatch')
class PanelConsorcistView(RolRequeridoMixin, TemplateView):
    rol_requerido = 'consorcista'
    template_name = 'panel_consorcista.html'
