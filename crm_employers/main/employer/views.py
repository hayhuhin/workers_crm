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
from custom_validation.validation import OutputMessages


#* employer section
class CreateEmployer(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)

	def get(self,request):
		#* just returns json example for the user
		main_message = "post method required"
		second_message = {"json_example":{
			"first_name":"first name of the employer",
			"last_name":"last name of the employer",
			"email":"have to be the same as the user email",
			"phone":"phone number of the employer"
		}}
		response_message = OutputMessages.error_with_message(main_message=main_message,second_message=second_message)
		return Response(response_message[1],status=status.HTTP_200_OK)

	def post(self, request):
		cleaned_data = request.data
		user = {"email":request.user.email}

		serializer = CreateEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=False):
			created_data = serializer.create(cleaned_data,user=user)
			if all(created_data): 
				return Response(created_data[1],status=status.HTTP_201_CREATED)
			
			return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
		return Response({"error":"invalid fields passed"},status=status.HTTP_404_NOT_FOUND)


class DeleteEmployer(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)
	

	def get(self,request):
		query_dict = {**request.GET}
		cleaned_data = {key: value[0] for key, value in query_dict.items()}
		user = {"email":request.user.email}

		serializer = DeleteEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=False):
			get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
			if all(get_data):
				return Response(get_data[1],status=status.HTTP_200_OK)

			return Response(get_data[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)
			


	def post(self, request):
		cleaned_data = request.data
		user = {"email":request.user.email}
		serializer = DeleteEmployerSerializer(data=cleaned_data)
		
		if serializer.is_valid(raise_exception=True):
			delete_data = serializer.delete(cleaned_data=cleaned_data,user=user)
			if all(delete_data):
				return Response(delete_data[1],status=status.HTTP_202_ACCEPTED)

			return Response(delete_data[1],status=status.HTTP_404_NOT_FOUND)
			
		return Response({"error":"invalid fields"},status=status.HTTP_404_NOT_FOUND)


class UpdateEmployer(APIView):
	permission_classes = {permissions.IsAuthenticated,MediumPermission,}


	def get(self,request):
		query_dict = {**request.GET}
		cleaned_data = {key: value[0] for key, value in query_dict.items()}
		user = {"email":request.user.email}

		serializer = UpdateEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=False):
			get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
			if all(get_data):
				return Response(get_data[1],status=status.HTTP_200_OK)

			return Response(get_data[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)
			


	
	def post(self,request):
		cleaned_data = request.data
		user = {"email":request.user.email}

		serializer = UpdateEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=False):
			update_employer = serializer.update(cleaned_data=cleaned_data,user=user)
			if all(update_employer):
				return Response(update_employer[1],status=status.HTTP_201_CREATED)
			
			return Response(update_employer[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"the input is invalid"},status=status.HTTP_404_NOT_FOUND)



class GetEmployer(APIView):
	permission_classes = {permissions.IsAuthenticated,MediumPermission,}

	def get(self,request):
		query_dict = {**request.GET}
		cleaned_data = {key: value[0] for key, value in query_dict.items()}
		user = {"email":request.user.email}

		serializer = GetEmployerSerializer(data=cleaned_data)
		if serializer.is_valid(raise_exception=False):
			employer_exists = serializer.get_info(cleaned_data=cleaned_data,user=user)
			if all(employer_exists):
				return Response(employer_exists[1],status=status.HTTP_200_OK)
			
			return Response(employer_exists[1],status=status.HTTP_404_NOT_FOUND)
		return Response({"error":"invalid fields"},status=status.HTTP_404_NOT_FOUND)
