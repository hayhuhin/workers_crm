
#---------  restframewok library
from django.contrib.auth import get_user_model,login,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .validations import  custom_validation,validate_email,validate_password
from .serializers import UserLoginSerializer,UserRegisterSerializer,UserSerializer
from rest_framework.authtoken.models import Token
from .permissions import SystemAdminPermission,ITAdminPermission,FinanceFullPermission,FinanceUpdatePermission,FinanceViewPermission,MediumPermission



#*user section
class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)


	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(user, status=status.HTTP_201_CREATED)
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
	

class AssignFinanceViewPermission(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)


	
class AssignFinanceUpdatePermission(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)

	
class AssignFinanceViewPermission(APIView):
	permission_classes = (permissions.IsAuthenticated,MediumPermission,)
