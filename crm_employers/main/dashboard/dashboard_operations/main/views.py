from .serializers import CreateRecordSerializer,UpdateRecordSerializer,DeleteRecordSerializer,CompareRecordSerializer,GetInsightsSerializer,UpdateInsightsSerializer,AddInsightsSerializer,DeleteInsightsSerializer
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
        user = {"email":request.user.email}

        serializer = CreateRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            #the graph calculator class
            graph_calculator = GraphCalculator(user=request.user.username,last_save="",db=[Income,Outcome],db_func=[Sum])

            #the graph mongodb CRUD operations class
            #the db,collection,max_amount will be accessed from the user database
            mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=request.user.username,max_records=7)
    

            #serializing the data
            graph_calculated_data = graph_calculator.sum_by_range(db=serializer.data["db"],start_date=serializer.data["start"],end_date=serializer.data["end"])

            created_record = serializer.create(graph_data=graph_calculated_data)
            if created_record:
                mongodb_handler.add_record(created_record)
                return Response(created_record,status=status.HTTP_201_CREATED)
            
            return Response({"error":"cant create record"},status=status.HTTP_404_NOT_FOUND)

        return Response(data=[{"error":"invalid input. the input have to look like in the example below:"},{
                    "graph_title":"graph_title",
                    "graph_description":"graph_description",
                    "graph_type":"graph_type",
                    "db":"db",
                    "start":"%Y-%m-%d",
                    "end":"%Y-%m-%d",
                    }],status=status.HTTP_400_BAD_REQUEST)


class DeleteRecord(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)

    uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
    def post(self,request):
        #if the user posted any data
        if request.data:
            serializer = DeleteRecordSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid(raise_exception=True):
                    #the db,collection,max_amount will be accessed from the user database
                    mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=request.user.username,max_records=7)
                    mongodb_handler.remove_record(required_record=serializer.data["position"])
                    return Response({"status":"the record is deleted"},status=status.HTTP_200_OK)
                    
            return Response({{"error":"the data is not in a valid format"},{"position":"str(number)"}},status=status.HTTP_400_BAD_REQUEST)

        return Response({"error":"no data provided"})


class UpdateRecord(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)

    uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
    def post(self,request):
        #if the user posted any data
        if request.data:
            serializer = UpdateRecordSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                
                #the graph calculator class
                graph_calculator = GraphCalculator(user=request.user.username,last_save="",db=[Income,Outcome],db_func=[Sum])

                #the graph mongodb CRUD operations class
                #the db,collection,max_amount will be accessed from the user database
                mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=request.user.username,max_records=7)

                #serializing the data
                graph_calculated_data = graph_calculator.sum_by_range(db=serializer.data["db"],start_date=serializer.data["start"],end_date=serializer.data["end"])

                updated_record = serializer.update_record(graph_data=graph_calculated_data)
                if updated_record:
                    mongodb_handler.edit_record(record_position=serializer.data["graph_position"],edit_data=updated_record)
                    updated_record["graph_position"] = serializer.data["graph_position"]
                    return Response(updated_record,status=status.HTTP_201_CREATED)
                
                return Response({"error":"cant update record"},status=status.HTTP_404_NOT_FOUND)
            
            return Response(request.data,status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=[{"error":"invalid input. the input have to look like in the example below:"},
                {
                    "graph_title":"graph_title",
                    "graph_description":"graph_description",
                    "graph_type":"graph_type",
                    "db":"db",
                    "start":"%Y-%m-%d",
                    "end":"%Y-%m-%d",
                    "graph_position":"graph_position"
                }],status=status.HTTP_400_BAD_REQUEST)


class GetRecord(APIView):

    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)
    #this handles the connection to the mongodb database
    uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"


    def get(self,request):

        graph_data = []

        mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=str(request.user.username),max_records=7)
        #this checking if the user already have basic record in the mongodb graph
        if not mongodb_handler.user_exists():
            mongodb_handler.create_basic_record()
        
        #method returns dict with records or empty dict if records not exist
        graph_records_dict = mongodb_handler.graph_records()

        #users first basic data
        user_basic_data = mongodb_handler.find_data({"name":request.user.username})


        #checking if the user have records
        if graph_records_dict:
            #itarates over the records keys
            for record in graph_records_dict:
                
                #for comparison methods i should parse "sql_database_compared" even if empty
                #checking if there are any sql_comparison records in the db
                if "sql_database_compared" in graph_records_dict[record]:
                    sql_comparison = graph_records_dict[record]["sql_database_compared"]
                else:
                    sql_comparison = []

                #this is how the structure if the "dict_values" argument have to look like
                dict_values = {"x":graph_records_dict[record]["x"],
                            "y":graph_records_dict[record]["y"],
                            "y_2":graph_records_dict[record]["y_2"],
                            "graph_description":graph_records_dict[record]["graph_description"],
                            "DB_1":graph_records_dict[record]["sql_database"],
                            "DB_2":sql_comparison}

                #this method creating graph html with the data extracted from the mongodb 

                #appending the graph_html to the graph_chart list and the list will be parsed into the html template
                graph_data.append({"graph_data":graph_records_dict[record],"graph_position":record})


            # serializer = GraphViewSerializer(graph_data[])

            return Response(graph_data,status=status.HTTP_200_OK)
            
        return Response({"error":"user dont have records"},status=status.HTTP_204_NO_CONTENT)


