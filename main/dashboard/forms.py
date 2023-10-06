from django import forms
from .models import Income


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["month", "amount",]
        labels = {"month": "Month", "amount":"Amount"}

