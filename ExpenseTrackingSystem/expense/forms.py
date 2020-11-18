from django import forms
from expense.models import Expense


class AddExpense(forms.Form):
    description = forms.CharField(max_length=150)
    amount = forms.FloatField()

    class Meta:
        model = Expense
        fields = ('description', 'amount',)