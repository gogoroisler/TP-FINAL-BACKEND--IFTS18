from django import forms

from .models import Expensa

# Formulario utilizado para crear y editar expensas
class ExpensaForm(forms.ModelForm):

    class Meta:

        model = Expensa

        fields = [
            'departamento',
            'periodo',
            'monto',
            'fecha_vencimiento',
            'pagada',
        ]
