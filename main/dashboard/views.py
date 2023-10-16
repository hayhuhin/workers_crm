from django.shortcuts import render,redirect,HttpResponse
import plotly.express as px
import pandas as pd
from  pathlib import Path
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm
from .models import Income,Outcome
from django.db.models import Sum
import calendar
import datetime
from func_tools.graph import sum_month,sum_date_by_range,graph_presentation

curr_path = Path.cwd()






# Create your views here.


@login_required
def dashboard(request):
    graph_presentation_instance = graph_presentation()
    income_form = IncomeForm()
    databases = ["Income","Outcome"]



    #all of this code below is only for testing and modifying the frontend
    df = pd.DataFrame(dict(
    months = ["jul 1 2024", "jul 2 2024", "jul 3 2024", "jul 4 2024", "jul 5 2024","jul 6 2024","jul 7 2024","8","9","10","11","12"],
    income = [14, 12, 8, 10, 16,14, 12, 8, 10, 16,15,1]))


    graph_fig = px.bar(df, x = 'months', y = 'income')
    graph_chart = graph_fig.to_html()

    pie_fig = px.pie(values = [20, 50, 37, 18],
        names = ['G1', 'G2', 'G3', 'G4'])
    pie_chart = pie_fig.to_html()

    line_fig = px.line(x = [1, 2, 3, 4, 5, 6, 7,8,9,10,11,12],
        y = [10, 15, 25, 18, 43, 30, 65,25,35,67,1,89])
    line_chart = line_fig.to_html()
    
    line_2_fig = px.line(x = [1, 2, 3, 4, 5, 6, 7],
              y = [10, 15, 25, 18, 43, 30, 65])
    line_2_chart = line_2_fig.to_html()


    if request.method == "POST":
        post_data = request.POST
        form_inst = IncomeForm(request.POST)

        if form_inst.is_valid():
            start = form_inst.cleaned_data.get("start_date")
            end = form_inst.cleaned_data.get("end_date")
            db = form_inst.cleaned_data.get("db")
            graph = form_inst.cleaned_data.get("graph")



            #this block of code below will be moved to another file in the future
            # sum_query_dict = sum_date_by_range(start,end,Income,Sum)








            
            if db.lower() == "income":#TODO add another function or class that handle another parts
            
                data = Income.objects.filter(month__range=(start,end)).all().aggregate(Sum('amount'))
                sum_query_dict = sum_date_by_range(start,end,Income,Sum)
                # print(sum_query_dict[1])



                # df = pd.DataFrame(dict(
                #     months = sum_query_dict[1],
                #     income = sum_query_dict[0]))


                # graph_fig = px.bar(df, x = 'months', y = 'income')
                # graph_chart_test = graph_fig.to_html()

                test = graph_presentation_instance.bar_graph(group=sum_query_dict[1],value=sum_query_dict[0],path="/")




            if db.lower() == "outcome":

                data = Outcome.objects.filter(month__range=(start,end)).all().aggregate(Sum('amount'))
                

            context = {'databases':databases,'data':data,'income_form':income_form,'graph_chart':test,'pie_chart':pie_chart,'line_chart':line_chart,'line_2_chart':line_2_chart}
            return render(request,'code/dashboard.html',context)


    month_data = []
    amount_data = []
    full_amount_list = []
    unique_month = set()



    data = Income.objects.filter(month__range=("2024-10-01","2025-10-01")).all().values_list()


    for _,date,amount in data.order_by("month"):

        the_month = date
        last_day_of_the_month = the_month.replace(day = calendar.monthrange(the_month.year, the_month.month)[1])
        full_amount = Income.objects.filter(month__range=(the_month,last_day_of_the_month)).all().annotate(Sum('amount'))
        
        # print(full_amount,"---",the_month,last_day_of_the_month)
        full_amount_list.append(full_amount)
        unique_month.add(date.strftime("%Y-%m"))
        month_data.append(date.strftime("%Y-%m"))
        amount_data.append(amount)

 
    df = pd.DataFrame(dict(
    months = month_data,
    income = amount_data))


    graph_fig = px.bar(df, x = 'months', y = 'income')
    graph_fig.update_xaxes(
    tickangle=-45,#the angle of the presentation
    dtick="M1", # sets minimal interval to month
    tickformat="%d.%m.%Y", # the date format you want 
)
    test_graph = graph_fig.to_html()



    test = px.line(x = month_data,
              y = amount_data)
    
    test.update_xaxes(
        tickangle=-45,#the angle of the presentation
        dtick="M1", # sets minimal interval to month
        tickformat="%d.%m.%Y", # the date format you want 
    )

    test_line = test.to_html()


        # print(type(i[2]))
        # string = ((i[0]).strftime("%Y-%m-%d"))
        # print(type(i[0]))
        # month_data.append(string)

    



    context = {'databases':databases,'income_form':income_form,'graph_chart':test_line,'pie_chart':pie_chart,'line_chart':line_chart,'line_2_chart':line_2_chart}
    return render(request,'code/dashboard.html',context)


