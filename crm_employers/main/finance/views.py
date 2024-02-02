
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .serializers import CreateIncomeSerializer,DeleteIncomeSerializer,UpdateIncomeSerializer,GetIncomeSerializer,CreateOutcomeSerializer,DeleteOutcomeSerializer,UpdateOutcomeSerializer,GetOutcomeSerializer
from user.models import User
from employer.models import Employer
from user.permissions import FinanceFullPermission,FinanceUpdatePermission,FinanceViewPermission

# Create your views here.



#!need to add an doption to pass email and then search for this worker first
#* Income section
class CreateIncome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission,)

    def get(self,request):
        cleaned_data = request.data
        serializer = CreateIncomeSerializer(data=cleaned_data)
        
        if serializer.is_valid():
            get_data = serializer.get_info(cleaned_data=cleaned_data)

            return Response(get_data[1],status=status.HTTP_200_OK)

        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)
        


    def post(self,request):
        cleaned_data = request.data
        serializer = CreateIncomeSerializer(data=cleaned_data)
        print(cleaned_data)
        if serializer.is_valid(raise_exception=True):
            created_data = serializer.create(cleaned_data=cleaned_data)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
        
        message = {"error":"invalid fields"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



class DeleteIncome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceFullPermission)


    def get(self,request):
        cleaned_data = request.data
        serializer = DeleteIncomeSerializer(data=cleaned_data)
        
        if serializer.is_valid():
            get_data = serializer.get_info(cleaned_data=cleaned_data)

            return Response(get_data[1],status=status.HTTP_200_OK)

        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        serializer = DeleteIncomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.delete(cleaned_data=cleaned_data)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)



class UpdateIncome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)


    def get(self,request):
        cleaned_data = request.data
        serializer = UpdateIncomeSerializer(data=cleaned_data)
        
        if serializer.is_valid():
            get_data = serializer.get_info(cleaned_data=cleaned_data)

            return Response(get_data[1],status=status.HTTP_200_OK)

        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        serializer = UpdateIncomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.update(cleaned_data=cleaned_data)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)



class GetIncome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceViewPermission)

    def get(self,request):
        cleaned_data = request.data
        serializer = GetIncomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.get_info(cleaned_data=cleaned_data)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
        
        message = {"error":"the fields are invalid"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



#*outcome section
class CreateOutcome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceFullPermission)


    def get(self,request):
        cleaned_data = request.data
        serializer = CreateOutcomeSerializer(data=cleaned_data)
        
        if serializer.is_valid():
            get_data = serializer.get_info(cleaned_data=cleaned_data)

            return Response(get_data[1],status=status.HTTP_200_OK)

        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)
        


    def post(self,request):
        cleaned_data = request.data
        serializer = CreateOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.create(cleaned_data=cleaned_data)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)

        return Response({"error":"invalid fields"},status=status.HTTP_404_NOT_FOUND)




class DeleteOutcome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceFullPermission)

    def get(self,request):
        cleaned_data = request.data
        serializer = DeleteOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            get_information = serializer.get_info(cleaned_data=cleaned_data)
            return Response(get_information[1],status=status.HTTP_200_OK)
        
        message = {"error":"invalid get request"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)
    

    def post(self,request):
        cleaned_data = request.data
        serializer = DeleteOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.delete(cleaned_data=cleaned_data)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)




class UpdateOutcome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceFullPermission)

    def get(self,request):
        cleaned_data = request.data
        serializer = UpdateOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.get_info(cleaned_data=cleaned_data)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
        
        message = {"error":"invalid fields"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        serializer = UpdateOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.update(cleaned_data=cleaned_data)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)



class GetOutcome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceViewPermission)

    def get(self,request):
        cleaned_data = request.data
        serializer = GetOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.get_info(cleaned_data=cleaned_data)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)




