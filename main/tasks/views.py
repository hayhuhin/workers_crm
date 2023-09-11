from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DepartmentTask,Lead,Task
from user.models import Employer
from .forms import CreateLead,CreateTask,EditTaskForm,EditLeadForm



@login_required
def tasks(request):
    """ tasks page:
            all buttons in this page are post forms with csrftokens and gives you permission to modify as u want(as a user)
                every add button open a form that must be filled and return post request.
                every complete,delete,edit is done by forms.
    """
    #user data
    user = Employer.objects.get(user=request.user)
    
    employer_department = Employer.objects.get(user=request.user).job_position

    employer_tasks = user.task.all()

    employer_leads = user.lead.all()


    #task and lead forms
    add_lead_form = CreateLead()
    add_task_form = CreateTask()



    #user validation if authenticated and the request.user is equal to the model of the employer
    if str(request.user) == str(user) and request.user.is_authenticated:
        employer_department_tasks = DepartmentTask.objects.filter(department__position=employer_department)

    context = {'context':employer_department_tasks,'employer_tasks':employer_tasks,'leads':employer_leads,'add_task_form':add_task_form,'add_lead_form':add_lead_form,}

    #checking if the method is POST
    if request.method == 'POST':   

        #adding tasks data to DB
        if request.POST.get('add_task'):
            post_data = request.POST

            task_record = Task.objects.create(title=post_data.get('title'),content=post_data.get('content'))        
            user.task.add(task_record)


        if request.POST.get('completed_task'):
            task_data = request.POST

            task_id = int((task_data.get("completed_task")))
            Task.objects.filter(id=task_id).update(completed=True)

            
            return render(request,'code/tasks.html',context)


        if request.POST.get('incompleted_task'):
            task_data = request.POST

            task_id = int((task_data.get("incompleted_task")))
            Task.objects.filter(id=task_id).update(completed=False)
            
            return render(request,'code/tasks.html',context)


        #adding lead to the DB
        if request.POST.get('add_lead'):
            post_data = request.POST

            lead_record = Lead.objects.create(name=post_data.get('name'),description=post_data.get('description'))
            user.lead.add(lead_record)

        
        #DELETE the task from the DB
        if request.POST.get("task_delete"):
            post_data = request.POST

            task_id = int(post_data.get("task_delete"))
            delete_record = Task.objects.get(id=task_id)
            delete_record.delete()

            #messages that represented 
            messages.add_message(request,messages.ERROR,"Deleted")


        if request.POST.get("lead_complete"):
            post_data = request.POST

            lead_id = int(post_data.get("lead_complete"))
            
            Lead.objects.filter(id=lead_id).update(completed=True)
            print(Lead.objects.filter(id=lead_id).values())
  
            
            return render(request,'code/tasks.html',context)

        if request.POST.get("lead_not_completed"):
            post_data = request.POST

            lead_id = int(post_data.get("lead_not_completed"))
            Lead.objects.filter(id=lead_id).update(completed=False)

    return render(request,'code/tasks.html',context)


def Edit_Task(request,ID):
    task_id = Task.objects.get(id=ID)
    form = EditTaskForm(instance=task_id)

    if request.method == "POST":
        form = EditTaskForm(request.POST,instance=task_id)
        if form.is_valid():
            form.save()
            # messages.succsess(request,"updated successfully")
            return redirect("tasks")


    context = {"edit_task_form":form,"task_data":task_id}
    
    return render(request,"code/edit_task.html",context)



def Edit_lead(request,ID):
    lead_id = Lead.objects.get(id=ID)
    form = EditLeadForm(instance=lead_id)

    if request.method == "POST":
        form = EditLeadForm(request.POST,instance=lead_id)
        if form.is_valid():
            form.save()
            # messages.succsess(request,"updated successfully")
            return redirect("tasks")


    context = {"edit_Lead_form":form,"lead_data":lead_id}
    
    return render(request,"code/edit_lead.html",context)
