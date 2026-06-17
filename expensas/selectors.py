from .models import Expensa, ItemExpensa


def get_todas_las_expensas():
    return Expensa.objects.all()


def get_expensas_por_departamento(departamento):
    return Expensa.objects.filter(departamento=departamento)


def get_expensa_por_id(expensa_id):
    return Expensa.objects.get(id=expensa_id)


def get_items_por_expensa(expensa):
    return ItemExpensa.objects.filter(expensa=expensa)
