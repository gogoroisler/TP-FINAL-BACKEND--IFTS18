from django.contrib import admin
from django.urls import path, include

from core.views import home, PanelAdminView, PanelConsorcistView
from consorcios.views import MisExpensasView
from expensas.views import (
    ListarExpensasView,
    CrearExpensaView,
    EditarExpensaView,
    EliminarExpensaView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home, name='home'),
    path('panel-admin/', PanelAdminView.as_view(), name='panel_admin'),
    path('panel-consorcista/', PanelConsorcistView.as_view(), name='panel_consorcista'),
    path('mis-expensas/', MisExpensasView.as_view(), name='mis_expensas'),
    path('listar-expensas/', ListarExpensasView.as_view(), name='listar_expensas'),
    path('crear-expensa/', CrearExpensaView.as_view(), name='crear_expensa'),
    path('editar-expensa/<int:expensa_id>/', EditarExpensaView.as_view(), name='editar_expensa'),
    path('eliminar-expensa/<int:expensa_id>/', EliminarExpensaView.as_view(), name='eliminar_expensa'),
]
