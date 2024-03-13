from django.db import models
from user.models import User
from company.models import Company


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    customer_id = models.IntegerField()
    company = models.ForeignKey(Company,on_delete=models.CASCADE)



class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_entries')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer')])
    # receipt = models.FileField(upload_to='receipts/', blank=True, null=True) # later it will be used 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='income_entries',default=None)
    # tax_info = models.CharField(max_length=100, blank=True, null=True)#later it will be used
    company = models.ForeignKey(Company,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.payment_method} -- {self.amount}"



    #all of this code below is only for testing and modifying the frontend


class Outcome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50 , choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer')])
    # receipt = models.FileField(upload_to='receipts/', blank=True, null=True) # later it will be used 
    vendor = models.CharField(max_length=100,blank=True,null=True)
    project_or_department = models.CharField(max_length=100,blank=True,null=True)
    # tax_info = models.CharField(max_length=100, blank=True, null=True)#later it will be used
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_time} -- {self.amount}"




