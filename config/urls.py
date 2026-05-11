from django.contrib import admin
from django.urls import path, include
from core.views import (
    home,
    panel_admin,
    panel_consorcista,
    mis_expensas,
    listar_expensas,
    crear_expensa,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('', home, name='home'),

    path('panel-admin/', panel_admin, name='panel_admin'),

    path('panel-consorcista/', panel_consorcista, name='panel_consorcista'),

    path('mis-expensas/', mis_expensas, name='mis_expensas'),

    path('listar-expensas/', listar_expensas, name='listar_expensas'),

    path('crear-expensa/', crear_expensa, name='crear_expensa'),
]