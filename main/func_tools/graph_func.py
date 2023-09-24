
#handle DB querying from the arguments passed to the function


def graph_percentage_presentation(user_model,job_position_tasks=None):
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
    

    if not job_position_tasks:

        all_tasks = user_model.task.all()
        completed_tasks = user_model.task.filter(completed=True)

        percentage_single_task = (100/len(all_tasks))

        percentage_done = len(completed_tasks) * percentage_single_task

        return round(percentage_done)