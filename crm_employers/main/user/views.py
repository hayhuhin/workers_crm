
#---------  restframewok library
from django.contrib.auth import get_user_model,login,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .validations import  custom_validation,validate_email,validate_password
from .serializers import UserLoginSerializer,UserRegisterSerializer,UserSerializer,AssignFinanceFullPermissionSerializer,AssignFinanceUpdatePermissionSerializer,AssignFinanceViewPermissionSerializer,DisallowFinanceFullPermissionSerializer,DisallowFinanceUpdatePermissionSerializer,DisallowFinanceViewPermissionSerializer,CreateUserSerializer
from rest_framework.authtoken.models import Token
from .permissions import SystemAdminPermission,ITAdminPermission,MediumPermission
from .models import User
from custom_validation.validation import OutputMessages




#*normal user creation
class CreateUser(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)

	def get(self,request):
		query_dict = {**request.GET}
		cleaned_data = {key: value[0] for key, value in query_dict.items()}
		user = {"email":request.user.email}

		serializer = CreateUserSerializer(data=cleaned_data)
		get_data = serializer.get_info(cleaned_data=cleaned_data)
		message = {"success":get_data[1]}
		return Response(message,status=status.HTTP_200_OK)


	def post(self,request):
		cleaned_data = request.data
		user = {"email":request.user.email}
		serializer = CreateUserSerializer(data=cleaned_data)

		if serializer.is_valid(raise_exception=True):
			get_data = serializer.create(cleaned_data=cleaned_data,user=user)
			if not all(get_data):
				return Response(get_data[1],status=status.HTTP_404_NOT_FOUND)
			

			return Response(get_data[1],status=status.HTTP_201_CREATED)
		
		
		main = "passed invalid fields"
		err_msg = OutputMessages.error_with_message(main)
		return Response(err_msg,status=status.HTTP_404_NOT_FOUND)
			

#*Admin user creation
class AdminUserRegister(APIView):
	permission_classes = (permissions.AllowAny,)

	def get(self,request):
		main = "request must be as post"
		second = {"json_example":{
			"username":"hero",
			"email":"hero@hero.com",
			"password":"Aa1122!!"
		}}
		err_msg = OutputMessages.error_with_message(main,second)
		return Response(err_msg,status=status.HTTP_400_BAD_REQUEST)


	def post(self, request):
		check_validation = custom_validation(request.data)
		if not all(check_validation):
			main = check_validation[1]
			return Response(main,status=status.HTTP_400_BAD_REQUEST)

		cleaned_data = check_validation[1]
		serializer = UserRegisterSerializer(data=cleaned_data)
		if serializer.is_valid():
			user_created = serializer.create(cleaned_data=cleaned_data)
			if all(user_created):
				return Response(user_created[1], status=status.HTTP_201_CREATED)
			return Response(status=status.HTTP_400_BAD_REQUEST)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	
	def post(self, request):
		print(request.data)
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)

			data = {}
			data["username"] = user.username
			data["email"] = user.email
			data["token"] = str(Token.objects.get(user=user))
			return Response(data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)


	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)
	



#* assign rules to employer

#TODO 
	#1.assign rules to employer

	#constraints:
		#the user that assigning must have the specific permission of assiggning
		#the assignment must be protected as much as posible
	
	#questions?
		#which assigning?
		#how much ?
	

class AssignFinanceFullPermission(APIView):
	permission_classes = (permissions.IsAuthenticated,ITAdminPermission,)

	def post(self,request):
		user_email = request.user.email
		user_data = request.data
		serializer = AssignFinanceFullPermissionSerializer(data=user_data)

		if serializer.is_valid():
			assigned_user = serializer.assign(user_data)
			if all(assigned_user):
				return Response(assigned_user[1],status=status.HTTP_202_ACCEPTED)
			
			return Response(assigned_user[1],status=status.HTTP_404_NOT_FOUND)


		return Response(assigned_user[1],status=status.HTTP_403_FORBIDDEN)


class AssignFinanceViewPermission(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)

	def post(self,request):
		user_data = request.data
		serializer = AssignFinanceViewPermissionSerializer(data=user_data)

		if serializer.is_valid():
			assigned_user = serializer.assign(user_data)
			if all(assigned_user):
				return Response(assigned_user[1],status=status.HTTP_202_ACCEPTED)
			
			return Response(assigned_user[1],status=status.HTTP_404_NOT_FOUND)


		return Response(assigned_user[1],status=status.HTTP_403_FORBIDDEN)

	
class AssignFinanceUpdatePermission(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)

	def post(self,request):
		user_data = request.data
		serializer = AssignFinanceUpdatePermissionSerializer(data=user_data)

		if serializer.is_valid():
			assigned_user = serializer.assign(user_data)
			if all(assigned_user):
				return Response(assigned_user[1],status=status.HTTP_202_ACCEPTED)
			
			return Response(assigned_user[1],status=status.HTTP_404_NOT_FOUND)

		return Response(assigned_user[1],status=status.HTTP_403_FORBIDDEN)



#*disallow section

class DisallowFinanceFullPermission(APIView):
	permission_classes = (permissions.IsAuthenticated,ITAdminPermission,)

	def post(self,request):
		user_data = request.data
		serializer = DisallowFinanceFullPermissionSerializer(data=user_data)

		if serializer.is_valid():
			assigned_user = serializer.disallow(user_data)
			if all(assigned_user):
				return Response(assigned_user[1],status=status.HTTP_202_ACCEPTED)
			
			return Response(assigned_user[1],status=status.HTTP_404_NOT_FOUND)

		return Response(assigned_user[1],status=status.HTTP_403_FORBIDDEN)



class DisallowFinanceViewPermission(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)

	def post(self,request):
		user_data = request.data
		serializer = DisallowFinanceViewPermissionSerializer(data=user_data)

		if serializer.is_valid():
			assigned_user = serializer.disallow(user_data)
			if all(assigned_user):
				return Response(assigned_user[1],status=status.HTTP_202_ACCEPTED)
			
			return Response(assigned_user[1],status=status.HTTP_404_NOT_FOUND)

		return Response(assigned_user[1],status=status.HTTP_403_FORBIDDEN)


class DisallowFinanceUpdatePermission(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)

	def post(self,request):
		user_data = request.data
		serializer = DisallowFinanceUpdatePermissionSerializer(data=user_data)

		if serializer.is_valid():
			assigned_user = serializer.disallow(user_data)
			if all(assigned_user):
				return Response(assigned_user[1],status=status.HTTP_202_ACCEPTED)
			
			return Response(assigned_user[1],status=status.HTTP_404_NOT_FOUND)

		return Response(assigned_user[1],status=status.HTTP_403_FORBIDDEN)

