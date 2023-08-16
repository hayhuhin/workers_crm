from django.shortcuts import render,redirect,HttpResponse
# import kaleido #required
import plotly.express as px
import pandas as pd


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
    #the pie figure
    revenue_fig = px.pie(values = [20, 50, 37, 18],template="plotly_dark",
             names = ['G1', 'G2', 'G3', 'G4'])
    #the bg color of the pie
    revenue_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    #text position and the font size udjustments
    revenue_fig.update_traces(textposition="outside",textfont_size=30,textinfo='percent+label')
    # takes the plotly figure and transforms it to image that is saved in static/dashboard/images/pie.png that is later is displayed in the html
    revenue_pie_chart = revenue_fig.write_image('/Users/valerilevinson/Desktop/Employers_manager_CRM/main/dashboard/static/dashboard/images/pie.png')


    #the donut figure of the plotly express library
    donut_figure = px.pie(values = [20, 50, 37, 18],template="plotly_dark",
             names = ['G1', 'G2', 'G3', 'G4'],
             color = ['G1', 'G2', 'G3', 'G4'],
             hole = 0.5)
    #the bg color of the pie
    donut_figure.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    #text position and the font size udjustments
    donut_figure.update_traces(textposition="outside",textfont_size=30,textinfo='percent+label')
    # takes the plotly figure and transforms it to image that is saved in static/dashboard/images/donut.png that is later is displayed in the html
    contrib_chart = donut_figure.write_image('/Users/valerilevinson/Desktop/Employers_manager_CRM/main/dashboard/static/dashboard/images/donut.png')


    context = {'revenue_pie_chart':revenue_pie_chart,'contrib_chart':contrib_chart}
    return render(request,'code/profile.html',context)