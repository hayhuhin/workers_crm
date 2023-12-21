from django.db import models


#models here




class Income(models.Model):
    month = models.DateField()
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.month} -- {self.amount}"



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
        

class GraphPermission(models.Model):
    permited = models.BooleanField(default=False)
    graph_type = models.CharField(max_length=30,default="general_graph")
    max_record_amount = models.IntegerField(default=7)

    description = f"graph_type - {graph_type} graph type - {graph_type} max_amount - {max_record_amount}"

    def __str__(self):
        return self.description
        
