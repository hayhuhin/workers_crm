from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DepartmentTask
from user.models import Employer



@login_required
def tasks(request):
    #user data
    user = Employer.objects.get(user=request.user)
    employer_department = Employer.objects.get(user=request.user).job_position
    employer_tasks = Employer.objects.get(user=request.user).task
    print(employer_tasks)


    #first user validation
    if str(request.user) == str(user) and request.user.is_authenticated:
        employer_department_tasks = DepartmentTask.objects.filter(department__position=employer_department)


        context = {'context':employer_department_tasks,'user_task':employer_tasks}
        return render(request,'code/tasks.html',context)


def sign_up(request):
    # if request.method == 'POST':
    pass
    # return render(request,'code/signup.html',{'form':form})
