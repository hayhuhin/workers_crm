# from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.auth import authenticate,login
# from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
# from .models import Employer

#---------restwramewok lib
from django.contrib.auth import get_user_model,login,logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .validations import  custom_validation,validate_email,validate_password
from .serializers import UserLoginSerializer,UserRegisterSerializer,UserSerializer





# def home(request):
#     if request.user.is_authenticated:
#         test = Employer.objects.get(user=request.user)
#         return render(request,'code/home.html',{'test':test})
#     else:
#         return redirect('/login')




# # def login(request):
# #     return render(request,'code/login.html')

# def sign_up(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('/dashboard')
#     else:
#         form=UserCreationForm()

#     return render(request,'code/signup.html',{'form':form})

# def test(request):
#     return render(request,'code/base_test.html')



class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)

	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)

	
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny)
	authentication_classes = ()

	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)