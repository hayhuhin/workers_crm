from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DepartmentTask,Lead,Task
from user.models import Employer
from .forms import CreateLead,CreateTask,EditTask



@login_required
def tasks(request):
    """ tasks page:
            all buttons in this page are post forms with csrftokens and gives you permission to modify as u want(as a user)
                every add button open a form that must be filled and return post request.
                every complete,delete,edit is done by forms.
    """
    #user data
    user = Employer.objects.get(user=request.user)
    
    def task_id_record(data):
        if data:
            return data 
        else:
            return None

    instance_id = None

    employer_department = Employer.objects.get(user=request.user).job_position

    employer_tasks = user.task.all()

    employer_leads = user.lead.all()

    #tast and lead forms
    add_task_form = CreateTask()
    add_lead_form = CreateLead()
    edit_task_form = EditTask()

    #first user validation
    if str(request.user) == str(user) and request.user.is_authenticated:
        employer_department_tasks = DepartmentTask.objects.filter(department__position=employer_department)


    if request.method == 'POST':   
        #adding tasks data to DB
        if request.POST.get('add_task') == "add_task":
            post_data = request.POST

            task_record = Task.objects.create(title=post_data.get('title'),content=post_data.get('content'))
            user.task.add(task_record)

        if request.POST.get('add_lead') == 'add_lead':
            post_data = request.POST

            lead_record = Lead.objects.create(name=post_data.get('name'),description=post_data.get('description'))
            user.lead.add(lead_record)

        #modify,edit,delete existent data to DB

        if request.POST.get('task_done'):
            #will set the task as DONE
            post_data = request.POST

        
        if request.POST.get("task_delete"):
            #DELETE the task from the DB
            post_data = request.POST
            task_id = int(post_data.get("task_delete"))
            delete_record = Task.objects.get(id=task_id)
            delete_record.delete()

        if request.POST.get("task_edit"):
            post_data = request.POST
            task_id = int(post_data.get("task_edit"))
            instance_id = task_id_record(task_id)
            edit_task_data = Task.objects.get(id=task_id)

            context = {'context':employer_department_tasks,'employer_tasks':employer_tasks,'leads':employer_leads,'add_task_form':add_task_form,'add_lead_form':add_lead_form,'edit_task_form':edit_task_form,'task_data':edit_task_data}
            return render(request,'code/tasks.html',context)

        #TODO fix the acces to global variable from local place
        if request.POST.get("add_task_submited"):
            post_data = request.POST
            print(instance_id)

            task_record = user.task.get(id=task_id)
            print(task_record)
            task_record.update(title=post_data.get('title'),content=post_data.get('content'))

    context = {'context':employer_department_tasks,'employer_tasks':employer_tasks,'leads':employer_leads,'add_task_form':add_task_form,'add_lead_form':add_lead_form}

    return render(request,'code/tasks.html',context)



def sign_up(request):
    # if request.method == 'POST':
    pass
    # return render(request,'code/signup.html',{'form':form})
