from django import forms
from .models import Expense, Transfer

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'category', 'date']

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['date'].required = False  # Устанавливаем поле необязательным

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['sender', 'receiver', 'amount', 'date']  # Добавляем поле date

    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'type': 'date'})  # Добавляем виджет для выбора даты