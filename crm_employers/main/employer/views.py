from django.shortcuts import render
from django.contrib.auth import get_user_model,login,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework.authtoken.models import Token
from user.permissions import MediumPermission
from .serializers import CreateEmployerSerializer,DeleteEmployerSerializer,GetEmployerSerializer,UpdateEmployerSerializer
from user.models import User
from employer.models import Employer


#* employer section
class CreateEmployer(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)

	def get(self,request):
		#* just returns json example for the user
		message = {"error":"post method required","post method json example":{
			"first_name":"first name of the employer",
			"last_name":"last name of the employer",
			"email":"have to be the same as the user email",
			"phone":"phone number of the employer"
		}}
		return Response(message,status=status.HTTP_200_OK)

	def post(self, request):
		# cleaned_data = custom_validation(request.data)
		#! later it will have custom method to handle the input data
		
		cleaned_data = request.data
		serializer = CreateEmployerSerializer(data=cleaned_data)
		
		if serializer.is_valid(raise_exception=True):
			created_data = serializer.create(cleaned_data)
			if all(created_data): 
				return Response(created_data[1],status=status.HTTP_201_CREATED)
			
			return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
		return Response({"error":"invalid inputs"},status=status.HTTP_404_NOT_FOUND)


class DeleteEmployer(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)
	

	def get(self,request):
		cleaned_data = request.data

		serializer = DeleteEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=True):
			get_data = serializer.get_info(cleaned_data=cleaned_data)
			if all(get_data):
				return Response(get_data[1],status=status.HTTP_200_OK)

			return Response(get_data[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)
			


	def post(self, request):
		cleaned_data = request.data
		serializer = DeleteEmployerSerializer(data=cleaned_data)
		
		if serializer.is_valid(raise_exception=True):
			delete_data = serializer.delete(cleaned_data=cleaned_data)
			if all(delete_data):
				return Response(delete_data[1],status=status.HTTP_202_ACCEPTED)

			return Response(delete_data[1],status=status.HTTP_404_NOT_FOUND)
			
		return Response({"error":"invalid fields"},status=status.HTTP_404_NOT_FOUND)


class UpdateEmployer(APIView):
	permission_classes = {permissions.IsAuthenticated,MediumPermission,}


	def get(self,request):
		cleaned_data = request.data

		serializer = UpdateEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=True):
			get_data = serializer.get_info(cleaned_data=cleaned_data)
			if all(get_data):
				return Response(get_data[1],status=status.HTTP_200_OK)

			return Response(get_data[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)
			


	
	def post(self,request):
		cleaned_data = request.data
		serializer = UpdateEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=True):
			update_employer = serializer.update(cleaned_data=cleaned_data)
			if update_employer[0]:
				return Response(update_employer[1],status=status.HTTP_201_CREATED)
			
			return Response(update_employer[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"the input is invalid"},status=status.HTTP_404_NOT_FOUND)



class GetEmployer(APIView):
	permission_classes = {permissions.IsAuthenticated,MediumPermission,}

	def get(self,request):
		cleaned_data = request.data
		serializer = GetEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=True):
			employer_exists = serializer.get_employer(cleaned_data=cleaned_data)
			if employer_exists[0]:
				return Response(employer_exists[1],status=status.HTTP_200_OK)
			
			return Response(employer_exists[1],status=status.HTTP_404_NOT_FOUND)
