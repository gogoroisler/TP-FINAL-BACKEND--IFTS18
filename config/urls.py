from django.contrib import admin
from django.urls import path, include
from core.views import (
    home,
    panel_admin,
    panel_consorcista,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('', home, name='home'),

    path('panel-admin/', panel_admin, name='panel_admin'),

    path('panel-consorcista/', panel_consorcista, name='panel_consorcista'),
]