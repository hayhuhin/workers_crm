from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def tasks(request):

    data = ''

    form = {'form':data}
    return render(request,'code/tasks.html',form)


def sign_up(request):
    # if request.method == 'POST':
    pass
    # return render(request,'code/signup.html',{'form':form})
