from django.contrib import admin

from .models import (
    Perfil,
    Consorcio,
    Departamento,
    Expensa
)

admin.site.register(Perfil)
admin.site.register(Consorcio)
admin.site.register(Departamento)
admin.site.register(Expensa)