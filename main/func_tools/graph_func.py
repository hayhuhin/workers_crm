
#handle DB querying from the arguments passed to the function



class progress_bar_class:
    def __init__(self,user_id,model,commands:list,**kwargs):
        self.commands = commands
        self.user_id = user_id
        self.model = model

    def execute_query(self):
        
        print(self.model)
        final_command = str(self.user_id)
        for command in self.commands:
            final_command += "."+ command
        print(str(self.model)+final_command)

        # for model in self.models:
            # model.self.commands


#Employer.objects.get(id=user.id).job_position.task.all()






def progress_bar(user,additional_commands:list,**kwargs):
    if additional_commands :

        final_command = str(user)
        for command in additional_commands:
            final_command += "."+ command

        print(eval(final_command))
            



# progress_bar('Employer.objects.get(id=1)',['job_position','task','all'])



def graph_percentage_presentation(user_model,job_position_tasks=None):
    """ simple percentage function that returns the completed percentage of the tasks"""
    if job_position_tasks:
        
        all_tasks = user_model.job_position.task.all()
        completed_tasks = user_model.job_position.task.filter(completed=True)

        percentage_single_task = (100/len(all_tasks))

        percentage_done = len(completed_tasks) * percentage_single_task

        return round(percentage_done)
    

    if not job_position_tasks:

        all_tasks = user_model.task.all()
        completed_tasks = user_model.task.filter(completed=True)

        percentage_single_task = (100/len(all_tasks))

        percentage_done = len(completed_tasks) * percentage_single_task

        return round(percentage_done)