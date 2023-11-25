import random 
import string
#handle DB querying from the arguments passed to the function


def graph_percentage_presentation(user_model,job_position_tasks=False,personal_tasks=False,leads=False):
    """ simple percentage function that returns the completed percentage of the tasks"""
    if job_position_tasks:
        
        all_tasks = user_model.job_position.task.all()
        completed_tasks = user_model.job_position.task.filter(completed=True)

        if len(all_tasks):
            percentage_single_task = (100/len(all_tasks))

            percentage_done = len(completed_tasks) * percentage_single_task

            return round(percentage_done)
        else:
            return 0
    

    if  personal_tasks:

        all_tasks = user_model.task.all()
        completed_tasks = user_model.task.filter(completed=True)

        percentage_single_task = (100/len(all_tasks))

        percentage_done = len(completed_tasks) * percentage_single_task

        return round(percentage_done)
    
    if leads:


        all_leads = user_model.lead.all()
        completed_leads = user_model.lead.filter(completed=True)

        percentage_single_lead = (100/len(all_leads))

        percentage_done = len(completed_leads) * percentage_single_lead

        return round(percentage_done)
    

