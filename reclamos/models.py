from django.db import models
from django.contrib.auth.models import User
from consorcios.models import Departamento


class Reclamo(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
    ]

    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.titulo} - {self.departamento} - {self.estado}'
