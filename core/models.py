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



class Departamento(models.Model):

    consorcio = models.ForeignKey(
        Consorcio,
        on_delete=models.CASCADE
    )

    numero = models.CharField(max_length=10)

    piso = models.CharField(max_length=10)

    propietario = models.CharField(max_length=100)

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Departamento {self.numero} - {self.consorcio.nombre}'

class Expensa(models.Model):

    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE
    )

    periodo = models.CharField(max_length=20)

    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    fecha_vencimiento = models.DateField()

    pagada = models.BooleanField(default=False)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.departamento} - {self.periodo}'