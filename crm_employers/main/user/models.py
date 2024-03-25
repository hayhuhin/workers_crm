from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from company.models import Company


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
    companies = models.ManyToManyField(Company,blank=True,related_name="company_list")
    selected_company = models.ForeignKey(Company,blank=True,on_delete=models.SET_NULL,null=True,related_name="company")
    is_manager = models.BooleanField(default=False)
    managed_company =  models.ForeignKey(Company,blank=True,on_delete=models.CASCADE,null=True,related_name="managed_company")
    blocked_by = models.ManyToManyField(Company,blank=True,related_name="blocked_by")



    objects = UserManager()

    def has_perm(self,perm,obj=None) -> bool:
        return True
    

    @property
    def is_staff(self):
        return self.is_superuser

    
    def __str__(self) -> str:
        return self.username
    





@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



