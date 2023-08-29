from django.shortcuts import render,HttpResponse
from dashboard.graph_utility import graph_creator
from pathlib import Path
from dashboard.models import Job_position,Employer
from .graph import graph_presentation


#current path
curr_path = Path.cwd()


# Create your views here.

def specific_user_rank_query(username:str):

    user = Employer.objects.get(username=username)
    rank = user.job_position_MTM.rank

    return (str(rank))


def employer_detection(request):
    username = request.user
    job_position = request.user.employer.job_position_MTM.position
    job_rank = request.user.employer.job_position_MTM.rank

    user_data = {'username':username,'job_position':job_position,'job_rank':job_rank}
    return user_data



"""funtion that returns data to the webpage at /profile"""

def employer(request):
    curr_path = Path.cwd()
    user_data = employer_detection(request)

    if user_data['job_rank'] <= 300 and user_data['job_rank'] > 200:


        #graph creating class
        # instance_of_graph_creator = graph_creator()
        
        #graph html builder(combine the graph representation with html)
        instance_of_graph_presentation = graph_presentation()


        # contribution pie graph 
        path = str(curr_path) +"/employer_profile/static/employer/images/pie.png"
        values = [20, 50, 37, 18]

        names = ['week 1', 'week 2', 'week 3', 'week 4']
        monthly_pie_graph = instance_of_graph_presentation.pie_graph(names=names,values=values,path=path)



        # contribution pie graph 
        path = str(curr_path)+"/employer_profile/static/employer/images/donut.png"

        values=[20, 20, 20, 20, 20]
        names= ['day 1', 'day 2', 'day 3', 'day 4','day 5']
        weekly_donut_graph = instance_of_graph_presentation.donut_graph(values=values,names= names,path=path)



        #returns html/image as dict to the page
        
        user_data = {'username':'valeri levinson','user_position':'team leader','picture':'"{% static "employer/images/photo.png" %}"'}

        profile_card = instance_of_graph_presentation.user_card(user_data=user_data)

        monthly_graph_card = instance_of_graph_presentation.graph_card('monthly lead',user_calc=monthly_pie_graph)
        weekly_graph_card = instance_of_graph_presentation.graph_card('weekly lead',user_calc=weekly_donut_graph)



        context = {'profile':profile_card,'monthly_graph':monthly_graph_card,'weekly_graph':weekly_graph_card}
        return render(request,'code/profile_test.html',context)


    if user_data['job_rank'] <= 400 and user_data['job_rank'] > 300:


        #graph creating class
        instance_of_graph_creator = graph_creator()
        
        #graph html builder(combine the graph representation with html)
        instance_of_graph_presentation = graph_presentation()


        #in the future there will be funtion that represents the graph 
        #and function that queries and outputs the data for representation
        def teams_completion_daily(arg):
            pass
        def teams_completion_weekly(arg):
            pass
        def teams_completion_monthly(arg):
            pass
        daily_data_query = []
        weekly_data_query = []
        monthly_data_query = []

        #team task compeliton daily

        teams_completion_daily(daily_data_query)

        #team task compelition weekly
        teams_completion_weekly(weekly_data_query)

        #team task compelition monthly
        teams_completion_monthly(monthly_data_query)


        context = {"teams_completion_monthly":teams_completion_monthly}
        return render(request,'code/profile_test.html',context)
