from django.db import models
from consorcios.models import Departamento


class Expensa(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    pagada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.departamento} - {self.periodo}'
