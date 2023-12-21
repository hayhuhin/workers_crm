from django.db import models
from django.db.models.signals import post_save
from tasks.models import Lead,Task,DepartmentTask
from dashboard.models import GraphPermission
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("An Email Required.")

        if not password:
            raise ValueError("A password required.")
        
        #this method checking that the email is in correct format
        email = self.normalize_email(email)

        #this setups the django username as email
    
        user = self.model(email=email,username=username)
        #setting the password


        user.set_password(password)
        #saving the user
    
        user.save()
        return user
    

    def create_superuser(self,email,username,password=None):
        if not email:
            raise ValueError("An Email Required.")

        if not password:
            raise ValueError("A password required.")
        

        #this method checking that the email is in correct format
        user = self.create_user(email=email,username=username,password=password)
        #this setups the user as a super user
        user.is_superuser = True
        #saving the user
        user.save()
        return user
    

class User(AbstractBaseUser,PermissionsMixin):

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50,unique=True)
    username = models.CharField(max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def has_perm(self,perm,obj=None) -> bool:
        return True
    

    @property
    def is_staff(self):
        return self.is_superuser

    
    def __str__(self) -> str:
        return self.username
    


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


