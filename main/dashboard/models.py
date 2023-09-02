from django.db import models
import plotly.express as px
import pandas as pd
from user.models import CompanyWorthModel

#models here

def dashboard(request):

    #all of this code below is only for testing and modifying the frontend
    df = pd.DataFrame(dict(
    group = ["A", "B", "C", "D", "E"],
    value = [14, 12, 8, 10, 16]))

    graph_fig = px.bar(df, x = 'group', y = 'value')
    graph_chart = graph_fig.to_html()

    pie_fig = px.pie(values = [20, 50, 37, 18],
        names = ['G1', 'G2', 'G3', 'G4'])
    pie_chart = pie_fig.to_html()

    line_fig = px.line(x = [1, 2, 3, 4, 5, 6, 7],
        y = [10, 15, 25, 18, 43, 30, 65])
    line_chart = line_fig.to_html()
    
    line_2_fig = px.line(x = [1, 2, 3, 4, 5, 6, 7],
              y = [10, 15, 25, 18, 43, 30, 65])
    line_2_chart = line_2_fig.to_html()


    context = {'graph_chart':graph_chart,'pie_chart':pie_chart,'line_chart':line_chart,'line_2_chart':line_2_chart}
    return render(request,'code/dashboard.html',context)



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
        
