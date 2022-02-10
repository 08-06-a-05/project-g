from django import forms
from operations.models import Operations

class AddOperationForm(forms.Form):
    OPERATION_CHOICES = (('+', 'Зачисление'), ('-', 'Списание'))

    operation_type = forms.ChoiceField(choices=OPERATION_CHOICES, label='Выберите тип операции')
    currency = forms.CharField(label='Выберите валюту')
    amount = forms.DecimalField(label='Введите сумму')
    datetime = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'type': 'search', 'list': 'categories'}), label='Выберите категорию')
    description = forms.CharField(label='Описание')
