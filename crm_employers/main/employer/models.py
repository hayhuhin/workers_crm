from django.db import models
#! need to uncomment it after fixing the dashboard application
# from dashboard.models import GraphPermission,GraphInsights
from user.models import User
from finance.models import Customer


#* employer and department section models 

class Employer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=50,blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(default='profile_pics/profile_picture.jpeg',upload_to='profile_pics')
    job_position = models.ForeignKey("Department",blank=True,null=True,on_delete=models.SET_NULL)
    lead = models.ForeignKey("Lead",blank=True,null=True,on_delete=models.SET_NULL)
    task = models.ManyToManyField("Task",default=None)
    #! need to uncomment it after fixing the dashboard application
    # graph_permission = models.ManyToManyField(GraphPermission,default=None)
    # insights_permission = models.ManyToManyField(GraphInsights,default=None)


    def __str__(self):
        return self.first_name


class Department(models.Model):
    name = models.CharField(max_length=50,null=True)
    rank = models.IntegerField(null=True)
    started_at = models.DateTimeField(auto_now=True)
    salary = models.IntegerField()
    task = models.ManyToManyField("DepartmentTask",blank=True)


    def __str__(self):
        return self.name



#* specific employer or department operations
    
class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company = models.ForeignKey(Customer,on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('lost', 'Lost'),
        ('converted', 'Converted'),
    ], default='new')
    source = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='leads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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


