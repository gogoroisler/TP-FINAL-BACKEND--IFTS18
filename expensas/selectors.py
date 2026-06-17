from .models import Expensa


def get_todas_las_expensas():
    return Expensa.objects.all()


def get_expensas_por_departamento(departamento):
    return Expensa.objects.filter(departamento=departamento)


def get_expensa_por_id(expensa_id):
    return Expensa.objects.get(id=expensa_id)
