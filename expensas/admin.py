from django.contrib import admin
from .models import Expensa, Proveedor, ItemExpensa

admin.site.register(Proveedor)
admin.site.register(Expensa)
admin.site.register(ItemExpensa)
