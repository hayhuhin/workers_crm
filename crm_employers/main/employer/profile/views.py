from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .serializers import GetProfileSerializer,UpdateProfileSerializer
from user.models import User
from employer.models import Employer



#* profile section 

class GetProfile(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	


	def get(self, request):
		
		cleaned_data = request.data
		serializer = GetProfileSerializer(data=cleaned_data)

		if serializer.is_valid(raise_exception=True):
			response_data = serializer.get_profile(cleaned_data=cleaned_data)
			#*this section is checking that the there is no unauthorized access
			if all(response_data):
				return Response(response_data[1],status=status.HTTP_200_OK)
				
			return Response(response_data[1],status=status.HTTP_404_NOT_FOUND)
			
		return Response({"error":"invalid inputs"},status=status.HTTP_404_NOT_FOUND)


class UpdateProfile(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		cleaned_data = request.data
		cleaned_data["email"] = request.user.email
		serialized_data = UpdateProfileSerializer(data=cleaned_data)

		if serialized_data.is_valid():
			updated_data = serialized_data.get_info(cleaned_data=cleaned_data)
			if all(updated_data):

				return Response(updated_data[1],status=status.HTTP_200_OK)
				#here im checking that the update method is available only for themself

			return Response(updated_data[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"invalid input data"},status=status.HTTP_404_NOT_FOUND)



	def post(self,request):
		cleaned_data = request.data
		cleaned_data["email"] = request.user.email
		serialized_data = UpdateProfileSerializer(data=cleaned_data)

		if serialized_data.is_valid():
			updated_data = serialized_data.update_profile(cleaned_data=cleaned_data)

			if all(updated_data):
				return Response(updated_data[1],status=status.HTTP_201_CREATED)

			return Response(updated_data[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"invalid input data"},status=status.HTTP_404_NOT_FOUND)


