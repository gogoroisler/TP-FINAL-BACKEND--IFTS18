from django.db import models
from consorcios.models import Consorcio, Departamento
from .validators import validar_formato_periodo


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    cuit = models.CharField(max_length=20, unique=True)
    rubro = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class GastoConsorcio(models.Model):
    TIPO_CHOICES = [
        ('ordinario', 'Ordinario'),
        ('extraordinario', 'Extraordinario'),
    ]
    ALCANCE_CHOICES = [
        ('general', 'General'),
        ('por_departamento', 'Por departamento'),
    ]
    PRORRATEO_CHOICES = [
        ('proporcional', 'Proporcional a m2'),
        ('igualitario', 'Partes iguales'),
    ]

    consorcio = models.ForeignKey(Consorcio, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    periodo = models.CharField(
        max_length=7,
        validators=[validar_formato_periodo],
        help_text='Formato: YYYY-MM'
    )
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='ordinario')
    alcance = models.CharField(
        max_length=20,
        choices=ALCANCE_CHOICES,
        default='general',
        help_text='Solo aplica para gastos extraordinarios'
    )
    prorrateo = models.CharField(
        max_length=20,
        choices=PRORRATEO_CHOICES,
        default='proporcional',
        help_text='Criterio de division entre departamentos'
    )
    departamentos = models.ManyToManyField(
        Departamento,
        blank=True,
        help_text='Solo para extraordinarios por departamento'
    )

    def __str__(self):
        return f'{self.consorcio} - {self.periodo} - {self.descripcion}'


class Expensa(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    periodo = models.CharField(
        max_length=7,
        validators=[validar_formato_periodo],
        help_text='Formato: YYYY-MM'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    pagada = models.BooleanField(default=False)
    publicada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    @property
    def saldo_pendiente(self):
        total_pagado = self.pagos.aggregate(total=models.Sum('monto'))['total'] or 0
        return self.monto - total_pagado

    def __str__(self):
        return f'{self.departamento} - {self.periodo}'


class Pago(models.Model):
    expensa = models.ForeignKey(
        Expensa,
        on_delete=models.CASCADE,
        related_name='pagos'
    )
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nota = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'Pago {self.expensa} - {self.fecha} - ${self.monto}'
