from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):

    ROLES = (
        ('admin', 'Administrador'),
        ('consorcista', 'Consorcista'),
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return self.usuario.username


class Consorcio(models.Model):

    nombre = models.CharField(max_length=100)

    direccion = models.CharField(max_length=200)

    cuit = models.CharField(max_length=20)

    telefono = models.CharField(max_length=20)

    email = models.EmailField()

    def __str__(self):
        return self.nombre