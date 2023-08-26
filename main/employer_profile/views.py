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
    """http render that displays profile page for every user"""
    post = 'vala'
    curr_path = Path.cwd()

    instance_of_graph_creator = graph_creator()
    instance_of_graph_presentation = graph_presentation('calc')

    # contribution pie graph 
    path = str(curr_path) +"/employer_profile/static/employer/images/pie.png"
    values = [20, 50, 37, 18]
    names = ['sales 1', 'sales 2', 'sales 3', 'sales 4']
    revenue_pie_chart = instance_of_graph_creator.pie_graph(names=names,values=values,path=path)


    # contribution pie graph 
    path = str(curr_path)+"/employer_profile/static/employer/images/donut.png"
    values=[20, 50, 37, 18]
    names= ['sales 1', 'sales 2', 'sales 3', 'sales 4']
    contrib_donut_chart = instance_of_graph_creator.donut_graph(values=values,names= names,path=path)



    #returns html/image as dict to the page
    user_data = {'username':'valeri levinson','user_position':'team leader','picture':'"{% static "employer/images/photo.png" %}"'}
    test = instance_of_graph_presentation.user_card(user_data=user_data)
    test2 = instance_of_graph_presentation.graph_card(user_data['username'],user_calc=revenue_pie_chart)
    context = {'revenue_pie_chart':revenue_pie_chart,'contrib_chart':contrib_donut_chart,'profile':test,'monthly':test2}
    return render(request,'code/profile_test.html',context)
