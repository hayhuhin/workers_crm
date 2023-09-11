from .models import Lead,Task
from django import forms


class CreateLead(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "description"]
        labels = {'name': "Name", "description": "Description"}


class EditLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "description"]
        labels = {'name': "Name", "description": "Description"}



class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "content"]
        labels = {'title': "Title", "content": "Content"}



class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "content","id"]
        labels = {'title': "Title", "content": "Content","id":"id"}

