from django import forms
from operations.models import Operations, Categories

class AddOperationForm(forms.ModelForm):
    OPERATION_CHOICES = (('+', 'Зачисление'), ('-', 'Списание'))

    operation_type = forms.ChoiceField(choices=OPERATION_CHOICES, label='Выберите тип операции')
    currency = forms.CharField(label='Выберите валюту')
    amount = forms.DecimalField(label='Введите сумму')
    datetime = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    # category = forms.ModelChoiceField(queryset=Categories.objects.select_related().filter(user=user_id))
    description = forms.CharField(label='Описание', required=False)

    class Meta:
        model = Operations
        fields = ['operation_type', 'currency', 'amount', 'category', 'datetime', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('user')
        print(user)
        super(AddOperationForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Categories.objects.filter(user=user))
