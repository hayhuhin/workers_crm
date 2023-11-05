from django import forms
from .models import Income


class AddGraphForm(forms.Form):

    start_date = forms.DateField()
    end_date = forms.DateField()
    # db = forms.CharField(max_length=100)
    db = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'hidden': 'hidden'})
    )
    graph = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'hidden': 'hidden'})
    )


    # fields = ["start_date","end_date","db"]
    # labels = {"start_date":"start date","end_date":"end date","db":"data base"}

