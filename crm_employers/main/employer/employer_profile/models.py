from django.db import models


#example of plotly arguments to every graph
values = [20, 50, 37, 18]
names = ['week 1', 'week 2', 'week 3', 'week 4']

class profit_data:
    """ this class will be called every time to query to the database"""
    def __init__(self,user_object):
        self.user_object = user_object

    def weekly_data(self):
        #will return a dict with the day and the profit of this day
        pass

    def monthly_data(self):
        #will sum all days and represent it by weeks
        pass

