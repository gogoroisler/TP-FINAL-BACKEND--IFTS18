from django.db import models
from consorcios.models import Departamento


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    cuit = models.CharField(max_length=20)
    rubro = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Expensa(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    pagada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.departamento} - {self.periodo}'


class ItemExpensa(models.Model):
    expensa = models.ForeignKey(
        Expensa,
        on_delete=models.CASCADE,
        related_name='items'
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT
    )
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.proveedor} - {self.descripcion} - ${self.monto}'
