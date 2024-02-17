from .serializers import CreateInsightSerializer,UpdateInsightSerializer,DeleteInsightSerializer,GetInsightSerializer
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



#* insight operations

class CreateInsight(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)

    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = CreateInsightSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
            message = {"success":"jsonm example for the post method to create this insight","json_example":get_data[1]}
            return Response(message,status=status.HTTP_200_OK)
        return Response({"error":"invalid fields passed"},status=status.HTTP_404_NOT_FOUND)



    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}

        serializer = CreateInsightSerializer(data=request.data)
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


class UpdateInsight(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)
    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = UpdateInsightSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_data):
                return Response(get_data[1],status=status.HTTP_201_CREATED)
            
            return Response(get_data[1],status=status.HTTP_400_BAD_REQUEST)
        
        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_403_FORBIDDEN)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}

        serializer = UpdateInsightSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):

            created_record = serializer.update(cleaned_data=cleaned_data,user=user)
            if all(created_record):
                return Response(created_record[1],status=status.HTTP_201_CREATED)
            
            return Response(created_record[1],status=status.HTTP_404_NOT_FOUND)
        

        message = {"error":"invalid input. the input have to look like in the example below:"},{
                    "insight_id":"graph_title",
                    }
        return Response(data=message,status=status.HTTP_400_BAD_REQUEST)


class DeleteInsight(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)

    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = DeleteInsightSerializer(data=cleaned_data)
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

        serializer = DeleteInsightSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            created_record = serializer.delete(cleaned_data=cleaned_data,user=user)
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


class GetInsight(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission,FinanceViewPermission)

    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email,"username":request.user.username}
        serializer = GetInsightSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=True):
            serializer_response = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(serializer_response):
                return Response(serializer_response[1],status=status.HTTP_200_OK)
            return Response(serializer_response[1],status=status.HTTP_404_NOT_FOUND)
        message = {"error":"invalid data passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)

