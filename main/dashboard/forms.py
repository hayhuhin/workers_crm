from django import forms
from .models import Income
from django.core.exceptions import ValidationError
import random
import string


class AddGraphForm(forms.Form):

    graph_title = forms.CharField(max_length=50,initial="Graph")
    graph_description = forms.CharField(max_length=400,initial="No Description")
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


# forms.py


def validate_file_size(value):
    max_size = 2 * 1024 * 1024  # 5 megabytes

    if value.size > max_size:
        raise ValidationError('File size must be no more than 2 megabytes.')



class ImportCSVForm(forms.Form):
    """this class is handling the first steps of the file importing :
    1.max name length is 12
    2.validating that the maximum file size is 2 megabytes - if more raise ValidationError("File size must be no more than 2 megabytes.")"""
    csv_file = forms.FileField(max_length=22,validators=[validate_file_size])

    def clean_csv_file(self):
        #change the name of the file to random character string
        csv_file = self.cleaned_data.get('csv_file')

        if csv_file:
            # Modify the file name as needed
            new_file_name = ''.join(random.choices(string.ascii_lowercase, k=9))
            
            # Change the name in the request.FILES dictionary
            self.files['csv_file'].name = new_file_name

        return csv_file