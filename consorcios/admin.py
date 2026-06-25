from django.contrib import admin
from .models import Consorcio, Departamento, Titularidad, SolicitudVinculacion

admin.site.register(Consorcio)
admin.site.register(Departamento)
admin.site.register(Titularidad)
admin.site.register(SolicitudVinculacion)
