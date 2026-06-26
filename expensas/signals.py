from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Pago


@receiver(post_save, sender=Pago)
def actualizar_estado_expensa(sender, instance, **kwargs):
    expensa = instance.expensa
    total_pagado = expensa.pagos.aggregate(total=Sum('monto'))['total'] or 0
    pagada = total_pagado >= expensa.monto
    if expensa.pagada != pagada:
        expensa.pagada = pagada
        expensa.save(update_fields=['pagada'])
