from django.db import models
from consorcios.models import Consorcio


class Aviso(models.Model):
    consorcio = models.ForeignKey(Consorcio, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    activo = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} - {self.consorcio}'
