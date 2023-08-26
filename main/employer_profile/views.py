from django.shortcuts import render,HttpResponse
from dashboard.graph_utility import graph_creator
from pathlib import Path
from dashboard.models import Job_position,Employer
from .graph import graph_presentation


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
    
    #graph html builder(combine the graph representation with html)
    instance_of_graph_presentation = graph_presentation('calc')


    # contribution pie graph 
    path = str(curr_path) +"/employer_profile/static/employer/images/pie.png"
    values = [20, 50, 37, 18]

    names = ['sales 1', 'sales 2', 'sales 3', 'sales 4']
    monthly_pie_graph = instance_of_graph_creator.pie_graph(names=names,values=values,path=path)



    # contribution pie graph 
    path = str(curr_path)+"/employer_profile/static/employer/images/donut.png"

    values=[20, 50, 37, 18]
    names= ['sales 1', 'sales 2', 'sales 3', 'sales 4']
    weekly_donut_graph = instance_of_graph_creator.donut_graph(values=values,names= names,path=path)



    #returns html/image as dict to the page
    user_data = {'username':'valeri levinson','user_position':'team leader','picture':'"{% static "employer/images/photo.png" %}"'}

    profile_card = instance_of_graph_presentation.user_card(user_data=user_data)

    monthly_graph_card = instance_of_graph_presentation.graph_card('mothly lead',user_calc=monthly_pie_graph)
    weekly_graph_card = instance_of_graph_presentation.graph_card('weakly lead',user_calc=weekly_donut_graph)



    context = {'profile':profile_card,'monthly_graph':monthly_graph_card,'weekly_graph':weekly_graph_card}
    return render(request,'code/profile_test.html',context)
