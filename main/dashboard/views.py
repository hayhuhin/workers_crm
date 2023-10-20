from django.shortcuts import render,redirect,HttpResponse
from  pathlib import Path
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm
from .models import Income,Outcome
from django.db.models import Sum
import calendar
from func_tools.graph import sum_month,sum_date_by_range,graph_presentation,save_the_graph,GraphHandler

curr_path = Path.cwd()






# Create your views here.


@login_required
def dashboard(request):


    graph_handler = GraphHandler(user=request.user,db=[Income,Outcome],db_func=[Sum],last_save = "")



    # graph_presentation_instance = graph_presentation()
    income_form = IncomeForm()
    databases = ["Income","Outcome"]
    saved_graph = None

    if request.method == "POST":
        post_data = request.POST
        form_inst = IncomeForm(request.POST)

        if form_inst.is_valid():
            start = form_inst.cleaned_data.get("start_date")
            end = form_inst.cleaned_data.get("end_date")
            db = form_inst.cleaned_data.get("db")
            graph = form_inst.cleaned_data.get("graph")

            
            graph_repr = graph_handler.sum_by_range(start,end)

            # if db.lower() == "income":#TODO add another function or class that handle another parts
                
            #     # data = Income.objects.filter(month__range=(start,end)).all().aggregate(Sum('amount'))
            #     sum_query_dict = sum_date_by_range(start,end,Income,Sum)
            #     graph_output_html = graph_presentation_instance.bar_graph(group=sum_query_dict[1],value=sum_query_dict[0],path="/")




            # if db.lower() == "outcome":
            #     # data = Outcome.objects.filter(month__range=(start,end)).all().aggregate(Sum('amount'))
            #     sum_query_dict = sum_date_by_range(start,end,Outcome,Sum)
            #     graph_output_html = graph_presentation_instance.bar_graph(group=sum_query_dict[1],value=sum_query_dict[0],path="/")

            #     saved_graph = save_the_graph(graph_output_html)


            context = {'databases':databases,'income_form':income_form,'graph_chart':graph_repr}
            return render(request,'code/dashboard.html',context)


    month_data = []
    amount_data = []
    full_amount_list = []
    unique_month = set()



    # data = Income.objects.filter(month__range=("2024-10-01","2025-10-01")).all().values_list()


    # for _,date,amount in data.order_by("month"):

    #     the_month = date
    #     last_day_of_the_month = the_month.replace(day = calendar.monthrange(the_month.year, the_month.month)[1])
    #     full_amount = Income.objects.filter(month__range=(the_month,last_day_of_the_month)).all().annotate(Sum('amount'))
        
    #     # print(full_amount,"---",the_month,last_day_of_the_month)
    #     full_amount_list.append(full_amount)
    #     unique_month.add(date.strftime("%Y-%m"))
    #     month_data.append(date.strftime("%Y-%m"))
    #     amount_data.append(amount)

 
#     df = pd.DataFrame(dict(
#     months = month_data,
#     income = amount_data))


#     graph_fig = px.bar(df, x = 'months', y = 'income')
#     graph_fig.update_xaxes(
#     tickangle=-45,#the angle of the presentation
#     dtick="M1", # sets minimal interval to month
#     tickformat="%d.%m.%Y", # the date format you want 
# )
#     test_graph = graph_fig.to_html()



    # test = px.line(x = month_data,
    #           y = amount_data)
    
    # test.update_xaxes(
    #     tickangle=-45,#the angle of the presentation
    #     dtick="M1", # sets minimal interval to month
    #     tickformat="%d.%m.%Y", # the date format you want 
    # )

    # test_line = test.to_html()


        # print(type(i[2]))
        # string = ((i[0]).strftime("%Y-%m-%d"))
        # print(type(i[0]))
        # month_data.append(string)

    



    context = {'databases':databases,'income_form':income_form,'graph_chart':saved_graph}
    return render(request,'code/dashboard.html',context)


