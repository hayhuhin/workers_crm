from django.db import models

# Create your models here.



class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=350)
    address = models.CharField(max_length=255)
    admin_email = models.EmailField(max_length=50,unique=True)
    # departments = models.ManyToManyField("Department", related_name='companies')

    def __str__(self):
        return self.name

