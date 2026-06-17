import re
from django.core.exceptions import ValidationError


def validar_formato_periodo(value):
    if not re.match(r'^\d{4}-\d{2}$', value):
        raise ValidationError(
            'El período debe tener el formato YYYY-MM. Ejemplo: 2026-06'
        )
