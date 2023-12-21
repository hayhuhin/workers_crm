from django.db import models



class Lead(models.Model):
    title = models.CharField(max_length=50)
    costumer_name = models.CharField(max_length=50,null=True)
    costumer_id = models.CharField(max_length=50,null=True)
    description = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=350)
    additional_description = models.TextField(max_length=350,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)



    def __str__(self):
        return self.title


class DepartmentTask(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=350)
    additional_description = models.CharField(max_length=350,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)



    def __str__(self):
        return self.title


