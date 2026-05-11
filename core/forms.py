from django import forms

from .models import Expensa


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
