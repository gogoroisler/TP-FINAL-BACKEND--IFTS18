from django.contrib import admin
from .models import Expensa, Proveedor, GastoConsorcio

admin.site.register(Proveedor)
admin.site.register(GastoConsorcio)
admin.site.register(Expensa)
