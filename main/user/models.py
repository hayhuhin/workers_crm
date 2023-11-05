from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from tasks.models import Lead,Task,DepartmentTask
from dashboard.models import GraphPermission



class Employer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=50,blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(default='profile_pics/profile_picture.jpeg',upload_to='profile_pics')
    job_position = models.ForeignKey("Department",blank=True,null=True,on_delete=models.SET_NULL)
    lead = models.ManyToManyField(Lead)
    task = models.ManyToManyField(Task)
    graph_permission = models.ManyToManyField(GraphPermission)




    def __str__(self):
        return self.first_name


class Department(models.Model):
    position = models.CharField(max_length=50,null=True)
    rank = models.IntegerField(null=True)
    started_at = models.DateTimeField()
    salary = models.IntegerField()
    task = models.ManyToManyField(DepartmentTask,blank=True)


    def __str__(self):
        return self.position


