from django.shortcuts import render
from django.contrib.auth import get_user_model,login,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .serializers import AddProfileSerializer
from rest_framework.authtoken.models import Token
from user.permissions import CanCreateEployers,CanUpdateGetEmployers
from .serializers import AddProfileSerializer,DeleteProfileSerializer,GetProfileSerializer
from user.models import User
from employer.models import Employer


# Create your views here.

class AddProfile(APIView):
	permission_classes = (permissions.IsAuthenticated,CanCreateEployers)
	

	def post(self, request):
		# cleaned_data = custom_validation(request.data)
		#! later it will have custom method to handle the input data
		
		cleaned_data = request.data
		serializer = AddProfileSerializer(data=cleaned_data)
		
		if serializer.is_valid(raise_exception=True):
			created_data = serializer.create(cleaned_data)
			if created_data[1] == "HTTP_201_CREATED": 
				return Response(created_data[0],status=status.HTTP_201_CREATED)
			
			return Response(created_data[0],status=status.HTTP_404_NOT_FOUND)
		return Response({"error":"invalid inputs"},status=status.HTTP_404_NOT_FOUND)


class DeleteProfile(APIView):
	permission_classes = (permissions.IsAuthenticated,CanCreateEployers)
	

	def post(self, request):
		# cleaned_data = custom_validation(request.data)
		#! later it will have custom method to handle the input data
		
		cleaned_data = request.data
		serializer = DeleteProfileSerializer(data=cleaned_data)
		
		if serializer.is_valid(raise_exception=True):
			user_id = serializer.validate_user_id(cleaned_data)
			if user_id:
				Employer.objects.delete(user_id) 
				return Response({"success":"deleted successfuly"},status=status.HTTP_202_ACCEPTED)
			
			return Response({"error":"user not exists"},status=status.HTTP_204_NO_CONTENT)
		return Response({"error":"invalid input"},status=status.HTTP_404_NOT_FOUND)


class GetProfile(APIView):
	permission_classes = (permissions.IsAuthenticated,CanCreateEployers)
	

	def get(self, request):
		# cleaned_data = custom_validation(request.data)
		#! later it will have custom method to handle the input data
		
		cleaned_data = request.data
		serializer = GetProfileSerializer(data=cleaned_data)
		
		if serializer.is_valid(raise_exception=True):

			response_data = serializer.get_request(cleaned_data=cleaned_data)
			return Response(response_data,status=status.HTTP_202_ACCEPTED)
		return Response({"error":"invalid inputs"},status=status.HTTP_404_NOT_FOUND)




# class UpdateProfile(APIView):
# 	permission_classes = (permissions.IsAuthenticated,CanModifyEmployer)
	
# 	def post(self, request):
# 		# cleaned_data = custom_validation(request.data)
# 		#! later it will have custom method to handle the input data
		
# 		cleaned_data = request.data
# 		serializer = AddProfileSerializer(data=cleaned_data)
		
# 		if serializer.is_valid(raise_exception=True):
# 			created_data = serializer.create(cleaned_data)
# 			if created_data[1] == "HTTP_201_CREATED": 
# 				return Response(created_data[0],status=status.HTTP_201_CREATED)
			
# 			return Response(created_data[0],status=status.HTTP_404_NOT_FOUND)
# 		return Response({"error":"invalid inputs"},status=status.HTTP_404_NOT_FOUND)




# class DeleteProfile(APIView):
# 	permission_classes = (permissions.IsAuthenticated,CanCreateEployers)
	

# 	def post(self, request):
# 		# cleaned_data = custom_validation(request.data)
# 		#! later it will have custom method to handle the input data
		
# 		cleaned_data = request.data
# 		serializer = AddProfileSerializer(data=cleaned_data)
		
# 		if serializer.is_valid(raise_exception=True):
# 			created_data = serializer.create(cleaned_data)
# 			if created_data[1] == "HTTP_201_CREATED": 
# 				return Response(created_data[0],status=status.HTTP_201_CREATED)
			
# 			return Response(created_data[0],status=status.HTTP_404_NOT_FOUND)
# 		return Response({"error":"invalid inputs"},status=status.HTTP_404_NOT_FOUND)


