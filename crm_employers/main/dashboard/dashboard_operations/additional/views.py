from .serializers import CompareRecordSerializer,SwitchRecordSerializer
from user.permissions import FinanceUpdatePermission,FinanceViewPermission
from finance.models import Income,Outcome
from django.db.models import Sum
from dashboard.func_tools.graph_calculations import GraphCalculator
from dashboard.mongo_db_graph.mongodb_connector import MongoDBConstructor
from employer.models import Employer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework.authtoken.models import Token
from django.conf import settings 




class CompareRecord(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission,FinanceViewPermission)

    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = CompareRecordSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_data):

                return Response(get_data[1],status=status.HTTP_201_CREATED)

            return Response(get_data[1],status=status.HTTP_406_NOT_ACCEPTABLE)

            
        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = CompareRecordSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            get_data = serializer.compare(cleaned_data=cleaned_data,user=user)
            if all(get_data):

                return Response(get_data[1],status=status.HTTP_201_CREATED)

            return Response(get_data[1],status=status.HTTP_406_NOT_ACCEPTABLE)

            
        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)

class SwitchRecord(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission,FinanceViewPermission)

    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = SwitchRecordSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_data):

                return Response(get_data[1],status=status.HTTP_201_CREATED)

            return Response(get_data[1],status=status.HTTP_406_NOT_ACCEPTABLE)

            
        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = SwitchRecordSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            get_data = serializer.switch(cleaned_data=cleaned_data,user=user)
            if all(get_data):

                return Response(get_data[1],status=status.HTTP_201_CREATED)

            return Response(get_data[1],status=status.HTTP_406_NOT_ACCEPTABLE)

            
        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)
