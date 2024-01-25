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


	def post(self, request):
		# cleaned_data = custom_validation(request.data)
		#! later it will have custom method to handle the input data
		
		cleaned_data = request.data
		serializer = CreateEmployerSerializer(data=cleaned_data)
		
		if serializer.is_valid(raise_exception=True):
			created_data = serializer.create(cleaned_data)
			if created_data[0]: 
				return Response(created_data[1],status=status.HTTP_201_CREATED)
			
			return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
		return Response({"error":"invalid inputs"},status=status.HTTP_404_NOT_FOUND)


class DeleteEmployer(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)
	

	def post(self, request):
		# cleaned_data = custom_validation(request.data)
		#! later it will have custom method to handle the input data
		
		cleaned_data = request.data
		serializer = DeleteEmployerSerializer(data=cleaned_data)
		
		if serializer.is_valid(raise_exception=True):
			employer_exists = serializer.validate_employer_exists(cleaned_data)

			if employer_exists[0] == True:
				Employer.objects.get(email=employer_exists[1]).delete()
				return Response({"success":"deleted successfuly"},status=status.HTTP_202_ACCEPTED)
			else:
				return Response(employer_exists[1],status=status.HTTP_404_NOT_FOUND)
			
		return Response({"error":"user not exists"},status=status.HTTP_204_NO_CONTENT)


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


class UpdateEmployer(APIView):
	permission_classes = {permissions.IsAuthenticated,MediumPermission,}
	
	
	def post(self,request):
		cleaned_data = request.data
		serializer = UpdateEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=True):
			update_employer = serializer.update_employer_fields(cleaned_data=cleaned_data)
			if update_employer[0]:
				return Response(update_employer[1],status=status.HTTP_201_CREATED)
			
			return Response(update_employer[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"the input is invalid"},status=status.HTTP_404_NOT_FOUND)



