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
		# cleaned_data = custom_validation(request.data)
		#! later it will have custom method to handle the input data
		
		cleaned_data = request.data
		serializer = GetProfileSerializer(data=cleaned_data)

		if serializer.is_valid(raise_exception=True):
			response_data = serializer.get_profile(cleaned_data=cleaned_data)
			
			#*this section is checking that the there is no unauthorized access

			if response_data[0]:

				response_user_email = response_data[1]["email"]
				found_employer = Employer.objects.get(email=response_user_email).user_id

				if found_employer == request.user.user_id:
					return Response(response_data[1],status=status.HTTP_202_ACCEPTED)
				
				return Response({"error":"cant access this users data"},status=status.HTTP_401_UNAUTHORIZED)
			
			return Response(response_data[1],status=status.HTTP_404_NOT_FOUND)
			
		return Response({"error":"invalid inputs"},status=status.HTTP_404_NOT_FOUND)


class UpdateProfile(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request):
		cleaned_data = request.data
		serialized_data = UpdateProfileSerializer(data=cleaned_data)

		if serialized_data.is_valid():
			updated_data = serialized_data.update_profile(cleaned_data=cleaned_data)

			if updated_data[0]:
				requested_email_data = updated_data[1]["email"]
				found_employer = Employer.objects.get(email=requested_email_data)

				#here im checking that the update method is available only for themself
				if found_employer.user_id == request.user.user_id:
					return Response(updated_data[1],status=status.HTTP_201_CREATED)
				
				return Response({"error":"cant update this users data"},status=status.HTTP_401_UNAUTHORIZED)

			return Response(updated_data[1],status=status.HTTP_404_NOT_FOUND)
		
		return Response({"error":"invalid input data"},status=status.HTTP_404_NOT_FOUND)


