from django.db import models


class Lead(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    created_at = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
