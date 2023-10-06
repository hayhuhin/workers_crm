from django.shortcuts import render,redirect,HttpResponse
import plotly.express as px
import pandas as pd
from  pathlib import Path
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm
from .models import Income
from django.db.models import Sum

curr_path = Path.cwd()






# Create your views here.


@login_required
def dashboard(request):
    income_form = IncomeForm()


    #all of this code below is only for testing and modifying the frontend
    df = pd.DataFrame(dict(
    months = ["1", "2", "3", "4", "5","6","7","8","9","10","11","12"],
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
            form_inst.save()

            data = Income.objects.filter(month__range=("2023-10-01","2023-11-01")).all().aggregate(Sum('amount'))

            context = {'data':data,'income_form':income_form,'graph_chart':graph_chart,'pie_chart':pie_chart,'line_chart':line_chart,'line_2_chart':line_2_chart}
            return render(request,'code/dashboard.html',context)






    context = {'income_form':income_form,'graph_chart':graph_chart,'pie_chart':pie_chart,'line_chart':line_chart,'line_2_chart':line_2_chart}
    return render(request,'code/dashboard.html',context)


