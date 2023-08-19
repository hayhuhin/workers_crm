from django.shortcuts import render,redirect,HttpResponse
# import kaleido #required
import plotly.express as px
import pandas as pd

from .graph_utility import graph_creator



# Create your views here.
def index(request):
    return render(request,"code/base.html")

def dashboard(request):

    #all of this code below is only for testing and modifying the frontend
    df = pd.DataFrame(dict(
    group = ["A", "B", "C", "D", "E"],
    value = [14, 12, 8, 10, 16]))
    print(df)

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



def teams(request):

    return render(request,'code/teams.html',{})

def personal_tasks(request):
    return render(request,'code/personal_tasks.html',{})

def daily_tasks(request):
    return render(request,'code/daily_tasks.html',{})

def profile(request):
    instance_of_graph_creator = graph_creator()
    
    
    # contribution pie graph 
    path = r"C:\Users\hayhuhin\Desktop\crm_project\main\dashboard\static\dashboard\images\pie.png"
    values = [20, 50, 37, 18]
    names = ['G1', 'G2', 'G3', 'G4']
    revenue_pie_chart = instance_of_graph_creator.pie_graph(names=names,values=values,to_html=False,path=path)


    # contribution pie graph 
    path = r"C:\Users\hayhuhin\Desktop\crm_project\main\dashboard\static\dashboard\images\donut.png"
    values=[20, 50, 37, 18]
    names= ['sales 1', 'sales 2', 'sales 3', 'sales 4']
    contrib_donut_chart = instance_of_graph_creator.donut_graph(values=values,names= names,path=path)



    #returns html/image as dict to the page
    context = {'revenue_pie_chart':revenue_pie_chart,'contrib_chart':contrib_donut_chart}
    return render(request,'code/profile.html',context)

