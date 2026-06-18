from django.contrib import admin
from django.urls import path, include

from core.views import home, PanelAdminView, PanelConsorcistView
from consorcios.views import (
    MisExpensasView,
    informar_pago,
    CrearSolicitudView,
    ListarSolicitudesView,
    gestionar_solicitud,
    retirar_permisos,
)
from expensas.views import (
    ListarExpensasView,
    DetalleExpensaView,
    CrearExpensaView,
    EditarExpensaView,
    EliminarExpensaView,
    SeleccionarPreviewView,
    PreviewPeriodoView,
    enviar_expensas,
)
from usuarios.views import redirigir_segun_rol, registro
from reclamos.views import (
    CrearReclamoView,
    MisReclamosView,
    ListarReclamosView,
    actualizar_estado,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home, name='home'),
    path('registro/', registro, name='registro'),
    path('redirigir/', redirigir_segun_rol, name='redirigir_segun_rol'),
    path('panel-admin/', PanelAdminView.as_view(), name='panel_admin'),
    path('panel-consorcista/', PanelConsorcistView.as_view(), name='panel_consorcista'),
    path('mis-expensas/', MisExpensasView.as_view(), name='mis_expensas'),
    path('informar-pago/<int:expensa_id>/', informar_pago, name='informar_pago'),
    path('solicitud/', CrearSolicitudView.as_view(), name='crear_solicitud'),
    path('solicitudes/', ListarSolicitudesView.as_view(), name='listar_solicitudes'),
    path('solicitudes/<int:solicitud_id>/', gestionar_solicitud, name='gestionar_solicitud'),
    path('solicitudes/retirar/<int:solicitud_id>/', retirar_permisos, name='retirar_permisos'),
    path('listar-expensas/', ListarExpensasView.as_view(), name='listar_expensas'),
    path('expensa/<int:expensa_id>/', DetalleExpensaView.as_view(), name='detalle_expensa'),
    path('crear-expensa/', CrearExpensaView.as_view(), name='crear_expensa'),
    path('editar-expensa/<int:expensa_id>/', EditarExpensaView.as_view(), name='editar_expensa'),
    path('eliminar-expensa/<int:expensa_id>/', EliminarExpensaView.as_view(), name='eliminar_expensa'),
    path('generar-expensas/', SeleccionarPreviewView.as_view(), name='seleccionar_preview'),
    path('preview/<int:consorcio_id>/<str:periodo>/', PreviewPeriodoView.as_view(), name='preview_periodo'),
    path('enviar-expensas/<int:consorcio_id>/<str:periodo>/', enviar_expensas, name='enviar_expensas'),
    path('mis-reclamos/', MisReclamosView.as_view(), name='mis_reclamos'),
    path('crear-reclamo/', CrearReclamoView.as_view(), name='crear_reclamo'),
    path('reclamos/', ListarReclamosView.as_view(), name='listar_reclamos'),
    path('reclamos/actualizar/<int:reclamo_id>/', actualizar_estado, name='actualizar_estado'),
]
