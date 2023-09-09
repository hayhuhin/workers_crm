from .models import Lead,Task
from django import forms


class CreateLead(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "description"]
        labels = {'name': "Name", "description": "Description"}

# name = models.CharField(max_length=50)
#     description = models.TextField(max_length=300)
#     created_at = models.DateTimeField()
#     completed = models.BooleanField(default=False)

class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "content"]
        labels = {'title': "Title", "content": "Content"}

    # title = models.CharField(max_length=50)
    # content = models.CharField(max_length=350)
    # created_at = models.DateTimeField(auto_now_add=True)
    # completed = models.BooleanField(default=False)


class EditTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "content","id"]
        labels = {'title': "Title", "content": "Content","id":"id"}

