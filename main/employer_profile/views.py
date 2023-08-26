from django.shortcuts import render,HttpResponse
from dashboard.graph_utility import graph_creator
from pathlib import Path
from dashboard.models import Job_position,Employer


# Create your views here.

def spesific_user_rank_query(username:str):

    user = Employer.objects.get(username=username)
    rank = user.job_position_MTM.rank

    return (str(rank))


def html_rank_policy(user,rank,calculations):
    """this function combine bootstrap html with the user specific calculations that defined by the rank of the user"""
    if rank <= 200:
        html = f"<div>{calculations}<div>"
        data = {'personal_data':html}

    return data




def employer(request):
    curr_path = Path.cwd()

 #graph creating class
    instance_of_graph_creator = graph_creator()
 


    # contribution pie graph 
    path = str(curr_path) +"/employer_profile/static/employer/images/pie.png"
    values = [20, 50, 37, 18]
    names = ['week 1', 'week 2', 'week 3', 'week 4']
    revenue_pie_chart = instance_of_graph_creator.pie_graph(names=names,values=values)


    # contribution pie graph 
    path = str(curr_path)+"/employer_profile/static/employer/images/donut.png"
    values=[20, 50, 37, 18,22]
    names= ['day 1', 'day 2', 'day 3', 'day 4','day 5']
    contrib_donut_chart = instance_of_graph_creator.donut_graph(values=values,names= names)



    #returns html/image as dict to the page
    context = {'revenue_pie_chart':revenue_pie_chart,'contrib_chart':contrib_donut_chart}
    return render(request,'code/profile.html',context)
