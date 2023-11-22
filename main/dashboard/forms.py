from django import forms
from .models import Income


class AddGraphForm(forms.Form):

    graph_title = forms.CharField(max_length=50,initial="Graph")
    graph_description = forms.CharField(initial="No Description")
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
    graph_id = forms.CharField(max_length=10,widget=forms.TextInput(attrs={"hidden":"hidden","class":"vala_id"}))


    db_options = [
        ("income","Income"),
        ("outcome","Outcome")]
    
    graph_options = [
        ("bar_graph","Bar graph"),
        ("line_graph","Line Graph")]

    db = forms.ChoiceField(choices=db_options)
        # widget=forms.TextInput(attrs={'style':'visibility: hidden; position: absolute;'}),

    graph = forms.ChoiceField(choices=graph_options
        # max_length=100,
        # widget=forms.TextInput(attrs={'hidden':'hidden'}),


    )

class DeleteGraphForm(forms.Form):
    graph_id = forms.IntegerField(widget=forms.HiddenInput())


class ChangeGraphPosition(forms.Form):
    src_graph_id = forms.IntegerField(widget=forms.TextInput(attrs={'hidden':'hidden'}))
    dst_graph_id = forms.IntegerField(max_value=8)


