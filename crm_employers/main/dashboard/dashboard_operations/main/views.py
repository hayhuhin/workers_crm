from .serializers import CreateRecordSerializer,UpdateRecordSerializer,DeleteRecordSerializer,GetRecordSerializer
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



class CreateRecord(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)
    uri = settings.MONGODB_URI
    def get(self,request):
        message = {"success":"json example","json_example":{
            "graph_title":"title of the graph",
            "graph_description":"graph description",
            "start_date":"the start date of the graph calculation",
            "end_date":"the end date of the graph calculation"
        }}
        return Response(message,status=status.HTTP_200_OK)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}

        serializer = CreateRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            created_record = serializer.create(cleaned_data=cleaned_data,user=user)
            if all(created_record):
                return Response(created_record[1],status=status.HTTP_201_CREATED)
            
            return Response(created_record[1],status=status.HTTP_404_NOT_FOUND)
        

        message = {"error":"invalid input. the input have to look like in the example below:"},{
                    "graph_title":"graph_title",
                    "graph_description":"graph_description",
                    "graph_type":"graph_type",
                    "db":"db",
                    "start":"%Y-%m-%d",
                    "end":"%Y-%m-%d",
                    }
        return Response(data=message,status=status.HTTP_400_BAD_REQUEST)


class DeleteRecord(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)

    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = DeleteRecordSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            serializer_response = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(serializer_response):
                return Response(serializer_response[1],status=status.HTTP_200_OK)
            return Response(serializer_response[1],status=status.HTTP_404_NOT_FOUND)
        message = {"error":"invalid data passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}

        serializer = DeleteRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            created_record = serializer.delete(cleaned_data=cleaned_data,user=user)
            if all(created_record):
                return Response(created_record[1],status=status.HTTP_201_CREATED)
            
            return Response(created_record[1],status=status.HTTP_404_NOT_FOUND)
        

        message = {"error":"invalid input. the input have to look like in the example below:"},{
                    "position":"100",

                    }
        return Response(data=message,status=status.HTTP_400_BAD_REQUEST)


class UpdateRecord(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)


    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = DeleteRecordSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            serializer_response = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(serializer_response):
                return Response(serializer_response[1],status=status.HTTP_200_OK)
            return Response(serializer_response[1],status=status.HTTP_404_NOT_FOUND)
        message = {"error":"invalid data passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}

        serializer = UpdateRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            created_record = serializer.update(cleaned_data=cleaned_data,user=user)
            if all(created_record):
                return Response(created_record[1],status=status.HTTP_201_CREATED)
            
            return Response(created_record[1],status=status.HTTP_404_NOT_FOUND)
        

        message = {"error":"invalid input. the input have to look like in the example below:"},{
                    "position":"100",

                    }
        return Response(data=message,status=status.HTTP_400_BAD_REQUEST)


class GetRecord(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)

    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = DeleteRecordSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            serializer_response = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(serializer_response):
                return Response(serializer_response[1],status=status.HTTP_200_OK)
            return Response(serializer_response[1],status=status.HTTP_404_NOT_FOUND)
        message = {"error":"invalid data passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)

