from django import forms
from .models import Income


class AddGraphForm(forms.Form):

    graph_title = forms.CharField(max_length=50,initial="Graph")
    graph_description = forms.CharField(max_length=300,initial="No Description")
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


class EditGraphForm(forms.Form):

    graph_title = forms.CharField(max_length=50)
    graph_description = forms.CharField(max_length=300)
    start_date = forms.DateField()
    end_date = forms.DateField()

    db = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'hidden': 'hidden'})
    )
    graph = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'hidden': 'hidden'})
    )
