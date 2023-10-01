from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Employer


def home(request):
    if request.user.is_authenticated:
        test = Employer.objects.get(user=request.user)
        return render(request,'code/home.html',{'test':test})
    else:
        return redirect('/login')




# def login(request):
#     return render(request,'code/login.html')

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/dashboard')
    else:
        form=UserCreationForm()

    return render(request,'code/signup.html',{'form':form})

def test(request):
    return render(request,'code/base_test.html')