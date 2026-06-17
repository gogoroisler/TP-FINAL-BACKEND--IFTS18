from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from usuarios.selectors import get_perfil_por_usuario


def home(request):
    return render(request, 'home.html')


@method_decorator(login_required, name='dispatch')
class PanelAdminView(TemplateView):
    template_name = 'panel_admin.html'

    def dispatch(self, request, *args, **kwargs):
        perfil = get_perfil_por_usuario(request.user)
        if perfil.rol != 'admin':
            return render(request, 'sin_permiso.html')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class PanelConsorcistView(TemplateView):
    template_name = 'panel_consorcista.html'

    def dispatch(self, request, *args, **kwargs):
        perfil = get_perfil_por_usuario(request.user)
        if perfil.rol != 'consorcista':
            return render(request, 'sin_permiso.html')
        return super().dispatch(request, *args, **kwargs)
