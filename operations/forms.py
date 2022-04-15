from django import forms
from django.db.models import Q
from operations.models import Operations, Categories
from account_manager.models import Currency, Balances
from decimal import Decimal
import gettext
_ = gettext.gettext

class AddOperationForm(forms.ModelForm):
    OPERATION_CHOICES = (('','placeholder'),('+', 'Зачисление'), ('-', 'Списание'))

    operation_type = forms.ChoiceField(
        choices=OPERATION_CHOICES, 
        widget=forms.Select(attrs={
            'class': 'field',
            'name': 'type',
            'size': '1',
            'id':'operations_type'
        }
    ))

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        empty_label='Валюта',
        widget=forms.Select(attrs={
            'class': 'field',
            'name': 'currency',
            'size': '1',
            'id' : 'operations_currency',
        }
    ))

    amount = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'field',
            'name': 'amount-field',
            'size': '1',
            'type': 'text', 
            'maxlength': '50',
            'placeholder': 'Введите сумму',
        }
    ))

    datetime = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'field',
            'type': 'date',
            'name': 'date', 
            'placeholder': 'Выберите дату',
            'id':'operations_date'
        }
    ))
    
    new_category = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'field',
            'id': 'new-category',
            'name': 'new-category',
            'type': 'text',
            'maxlength': '60',
            'placeholder': 'Напишите имя для новой категории'
        }
    ))

    description = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'field',
            'id': 'description',
            'name': 'description',
            'type': 'text',
            'maxlength': '2000',
            'placeholder': 'Описание'
        }
    ))

    class Meta:
        model = Operations
        fields = ['operation_type', 'currency', 'amount', 'category', 'datetime', 'description']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AddOperationForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
            queryset=Categories.objects.filter(Q(user=self.user.id) | Q(user=2)), 
            empty_label='Категория',
            required=False,
            widget=forms.Select(attrs={
                'class': 'field',
                'name': 'category',
                'size': '1',
                'id':'operations_category'
            }
        ))

    def clean(self):
        errors=[]
        new_category = self.cleaned_data.get('new_category')
        category = self.cleaned_data.get('category')
        currency = self.cleaned_data.get('currency')
        operation_type = self.cleaned_data.get('operation_type')
        amount = self.cleaned_data.get('amount')
        
        if not new_category and not category:
            errors.append(forms.ValidationError(_('Нужно указать либо существующую категорию, либо новую.'), code='invalid_category'))
        elif not category:
            category = Categories.objects.create(category_name=new_category, user=self.user)
            self.cleaned_data['category'] = category
        elif new_category and category:
            errors.append( forms.ValidationError(_('Нужно выбрать что-то одно: либо существующую, либо новую категорию.'), code='invalid_category'))
        if errors:
            raise forms.ValidationError(errors)
        currency_wallet = Balances.objects.get_or_create(user_id=self.user, currency_id=currency)
        if operation_type == '+':
            currency_wallet[0].amount += Decimal(amount)
        else:
            currency_wallet[0].amount -= Decimal(amount)
        currency_wallet[0].save()

        return super(AddOperationForm, self).clean()