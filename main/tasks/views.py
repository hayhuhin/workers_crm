from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DepartmentTask,Lead,Task
from user.models import Employer
from .forms import CreateLead,CreateTask,EditTaskForm,EditLeadForm
from func_tools.graph_func import graph_percentage_presentation


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


    department_task_graph = graph_percentage_presentation(user,job_position_tasks=True)
    employer_task_graph = graph_percentage_presentation(user,job_position_tasks=False)

    graph_representation = {"department_task_graph":str(department_task_graph),"employer_task_graph":str(employer_task_graph)}



    #user validation if authenticated and the request.user is equal to the model of the employer
    if str(request.user) == str(user) and request.user.is_authenticated:
        department_tasks = DepartmentTask.objects.filter(department__position=employer_department)



    #department tasks section


        #checking if the method is POST
        if request.method == "POST":   
            print(request.POST)
            if request.POST.get("name") == "department_task_complete":
                post_data = request.POST
                task_id = int((post_data.get("id")))
                DepartmentTask.objects.filter(id=task_id).update(completed=True)


            if request.POST.get("name") == "department_task_on_progress":
                post_data = request.POST
                task_id = int((post_data.get("id")))
                DepartmentTask.objects.filter(id=task_id).update(completed=False)

            
            if request.POST.get("name") == "department_task_delete":
                post_data = request.POST
                task_id = int((post_data.get("id")))
                delete_record = DepartmentTask.objects.get(id=task_id)
                delete_record.delete()




            #adding tasks data to DB
            if request.POST.get("name") == "submit_new_task":
                post_data = request.POST
                

                task_record = Task.objects.create(title=post_data.get("title"),description=post_data.get("description"),additional_description=post_data.get("additional_description"))        
                user.task.add(task_record)


            if request.POST.get("name")  == "complete_task_form":
                post_data = request.POST

                task_id = int((post_data.get("id")))
                Task.objects.filter(id=task_id).update(completed=True)
                messages.add_message(request, messages.INFO, "Hello world.")



            if request.POST.get("name") == "task_on_progress":
                post_data = request.POST

                task_id = int((post_data.get("id")))
                Task.objects.filter(id=task_id).update(completed=False)

 

            #adding lead to the DB
            if request.POST.get("name") == "submit_new_lead":
                post_data = request.POST

                lead_record = Lead.objects.create(title=post_data.get("title"),description=post_data.get("description"),costumer_name=post_data.get("costumer_name"),costumer_id=post_data.get("costumer_id"))
                user.lead.add(lead_record)
                print(40*"%")

            
            #DELETE the task from the DB
            if request.POST.get("name") == "task_delete":
                post_data = request.POST

                task_id = int(post_data.get("id"))
                delete_record = Task.objects.get(id=task_id)
                delete_record.delete()

                #messages that represented 



            if request.POST.get("name") == "lead_complete":
                post_data = request.POST

                lead_id = int(post_data.get("id"))
                Lead.objects.filter(id=lead_id).update(completed=True)


            if request.POST.get("name") == "lead_on_progress":
                post_data = request.POST

                lead_id = int(post_data.get("id"))
                Lead.objects.filter(id=lead_id).update(completed=False)

            if request.POST.get("name") == "lead_delete":
                post_data = request.POST

                lead_id = int(post_data.get("id"))
                delete_record = Lead.objects.get(id=lead_id)
                delete_record.delete()



            context = {"department_tasks":department_tasks,"employer_tasks":employer_tasks,"employer_tasks_len":len(employer_tasks),"leads":employer_leads,"add_task_form":add_task_form,"add_lead_form":add_lead_form,"messager":"this works"}
            return render(request,"code/tasks.html",context)
        if request.method == "GET":  

            context = {"department_tasks":department_tasks,"employer_tasks":employer_tasks,"leads":employer_leads,"add_task_form":add_task_form,"add_lead_form":add_lead_form,"graph_presentation":graph_representation}
            return render(request,"code/tasks.html",context)


@login_required
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


@login_required
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
