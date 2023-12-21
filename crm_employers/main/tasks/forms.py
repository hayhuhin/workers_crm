from .models import Lead,Task
from django import forms


class CreateLead(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["title", "costumer_name","costumer_id","description"]
        labels = {"title": "Title", "costumer_name":"Costumer Name","costumer_id":"Costumer ID","description": "Description"}


class EditLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["title", "costumer_name","costumer_id","description"]
        labels = {"title": "Title", "costumer_name":"Costumer Name","costumer_id":"Costumer ID","description": "Description"}



class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title","description","additional_description"]
        labels = {'title': "Title","description": "Description", "additional_description":"Additional Description"}



class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description","additional_description"]
        labels = {'title': "Title", "content": "Content","additional_description":"Additional Description"}

