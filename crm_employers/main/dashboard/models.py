from django.db import models
from django.contrib.auth.models import Group,Permission



class GraphPermission(models.Model):
    name = models.CharField(max_length=300)
    permited = models.BooleanField(default=False)
    graph_type = models.CharField(max_length=30,default="general_graph")
    max_record_amount = models.IntegerField(default=7)
    no_sql_db = models.CharField(max_length=50,default="test")
    collection = models.CharField(max_length=50,default="test")

    description = f"name - {name} permited - {permited} max_amount - {max_record_amount}"

    def __str__(self):
        return self.description
        

class GraphInsights(models.Model):
    name = models.CharField(max_length=300)
    permited = models.BooleanField(default=False)
    no_sql_db = models.CharField(max_length=50,default="test")
    collection = models.CharField(max_length=50,default="test")
    max_record_amount = models.IntegerField(default=4)



