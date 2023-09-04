from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from tasks.models import Lead,Task,DepartmentTask



class Employer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=50,blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    job_position = models.ForeignKey("Department",blank=True,null=True,on_delete=models.SET_NULL)
    lead = models.ForeignKey(Lead,blank=True,null=True,on_delete=models.SET_NULL)
    task = models.ForeignKey(Task,blank=True,null=True,on_delete=models.SET_NULL)

    


    def __str__(self):
        return self.first_name


class Department(models.Model):
    position = models.CharField(max_length=50,null=True)
    rank = models.IntegerField(null=True)
    started_at = models.DateTimeField()
    salary = models.IntegerField()
    task = models.ForeignKey(DepartmentTask,blank=True,null=True,on_delete=models.SET_NULL)


    def __str__(self):
        return self.position




# class Personal_task(models.Model):
#     title = models.CharField(max_length=50)
#     content = models.CharField(max_length=350)
#     created_at = models.DateTimeField()
#     completed = models.BooleanField(default=False)
#     employer_FK = models.ForeignKey("Employer",blank=True,on_delete=models.CASCADE)


#     def __str__(self):
#         return self.title


# class Lead_Creator(models.Model):
#     name = models.CharField(max_length=50)
#     action = models.CharField(max_length=50,default="None",null=True)
#     profit = models.IntegerField(default=0,null=True)
#     completed = models.BooleanField(default=False)
#     created_by = models.ForeignKey(Employer,on_delete=models.PROTECT)
#     created_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.name
    

# class Company_Cache_Income(models.Model):
#     last_year = models.IntegerField()
#     current_year = models.IntegerField()
#     last_updated = models.DateField()



# class Profit(models.Model):
#     worker_name = models.ForeignKey('Employer',null=True,on_delete=models.SET_NULL)
#     income_amount = models.IntegerField()
#     date = models.DateTimeField()


class CompanyWorthModel:
    pass