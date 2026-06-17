from django.db import models
from django.contrib.auth.models import User


class Consorcio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    cuit = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    consorcio = models.ForeignKey(Consorcio, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    piso = models.CharField(max_length=10)
    propietario = models.CharField(max_length=100)
    metros_cuadrados = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Departamento {self.numero} - {self.consorcio.nombre}'


class Titularidad(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.usuario} - {self.departamento}'
