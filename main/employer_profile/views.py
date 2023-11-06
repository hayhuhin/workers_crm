from django.shortcuts import render,HttpResponse
from pathlib import Path
from django.contrib.auth.decorators import login_required
from func_tools.graph import graph_presentation,employer_data_info


#current path
curr_path = Path.cwd()



@login_required
def profile_page(request):
    #profile page view that represent the employer rank 
    #                       associate data(employers name,
    #                       last name,position.etc..)
    
    #function that gets users name,lastname,position,rank and saved as dict
    request_data = employer_data_info(request)



    #the higher user rank the higher privileges the user have
    if request_data['job_rank'] <= 300 and request_data['job_rank'] > 200:
        #graph html builder(combine the graph representation with html)
        instance_of_graph_presentation = graph_presentation()
        

        # contribution pie graph 
        values = [20, 50, 37, 18]

        names = ['week 1', 'week 2', 'week 3', 'week 4']
        monthly_pie_graph = instance_of_graph_presentation.bar_graph(group=names,value=values)



        # contribution pie graph 

        values=[20, 20, 20, 20, 20,13,51]
        names= ['sunday', 'monday', 'tuesday', 'wednesday','thursday','friday','saturday']
        weekly_donut_graph = instance_of_graph_presentation.donut_graph(values=values,names= names)



        #returns html/image as dict to the page
        
        # request_data = {'username':request_data['username'],'user_position':request_data['job_position']}

        profile_card = instance_of_graph_presentation.user_card(user_data=request_data)

        monthly_graph_card = instance_of_graph_presentation.graph_card('monthly lead',user_calc=monthly_pie_graph)
        weekly_graph_card = instance_of_graph_presentation.graph_card('weekly lead',user_calc=weekly_donut_graph)


        # graph_queries_instance = graph_queries()
        # graph_queries_instance.task_completion(request.user)
        context = {'profile':profile_card,'monthly_graph':monthly_graph_card,'weekly_graph':weekly_graph_card}
        return render(request,'code/profile.html',context)


    if request_data['job_rank'] <= 400 and request_data['job_rank'] > 300:

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
        # graph_queries_inst = graph_queries()
        # graph_queries_inst.task_completion(request.user)
        return render(request,'code/profile.html',context)
