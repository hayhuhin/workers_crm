from django.db import models
from user.models import User

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    customer_id = models.IntegerField()



class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_entries')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer')])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='income_entries',default=None)

    def __str__(self):
        return f"{self.payment_method} -- {self.amount}"



    #all of this code below is only for testing and modifying the frontend


class Outcome(models.Model):
    month = models.DateField()
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.month} -- {self.amount}"




class CompanyWorth:
    #class the queries and returns dataframe as list format
    def __init__(self,period,model):
        self.period = period
        self.model = model

    def dataframe_query(self,data):
        group = [] 
        value = []
        query_record = self.model.objects.get(data)#TODO add django sum func
        for month,income in query_record:
            group.append(month)
            value.append(income)
        
        if len(group) == len(value):
            return group,value
        else:
            raise ValueError
        