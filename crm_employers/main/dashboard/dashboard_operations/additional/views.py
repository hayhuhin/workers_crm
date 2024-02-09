from .serializers import AddRecordSerializer,UpdateRecordSerializer,DeleteRecordSerializer,CompareRecordSerializer,GetInsightsSerializer,UpdateInsightsSerializer,AddInsightsSerializer,DeleteInsightsSerializer
from user.permissions import GraphGroupPermission,InsightsGroupPermission
from dashboard.models import Income,Outcome
from django.db.models import Sum
from func_tools.graph_calculations import GraphCalculator
from mongo_db_graph.mongodb_connector import MongoDBConstructor
from employer.models import Employer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework.authtoken.models import Token



# class CompareRecord(APIView):
#     permission_classes = (permissions.IsAuthenticated,GraphGroupPermission)
#     uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
#     def post(self,request):
#         #if the user posted any data
#         if request.data:
#             serializer = CompareRecordSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):                
#                 #the graph mongodb CRUD operations class
#                 #the db,collection,max_amount will be accessed from the user database
#                 mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=request.user.username,max_records=7)
#                 mongodb_handler.compare_record(position_1=serializer["src_position"],position_2=serializer["dst_position"])
#                 return Response({"success":"the both records are successfully compared"},status=status.HTTP_201_CREATED)
                
#             return Response({"error":"cant create record"},status=status.HTTP_404_NOT_FOUND)
#         return Response(request.data,status=status.HTTP_400_BAD_REQUEST)

# class SwitchPosition(APIView):
#     permission_classes = (permissions.IsAuthenticated,GraphGroupPermission)
#     uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
#     def post(self,request):
#         #if the user posted any data
#         if request.data:
#             #the graph mongodb CRUD operations class
#             #the db,collection,max_amount will be accessed from the user database
#             mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=request.user.username,max_records=7)
#             src = request.data["src_position"]
#             dst = request.data["dst_position"]
#             mongodb_handler.switch_records(src_position=src,dst_position=dst)

#             return Response({"success":"the records have switched successfuly"},status=status.HTTP_201_CREATED)
#         return Response({"error":"the data is incorrect and cant be added"},status=status.HTTP_404_NOT_FOUND)
    
#     def get(self,request):
#         request.data
#         return Response({"method must be post":{"data structure must be like that":{
#             "src_position":"str(source number)",
#             "dst_position":"str(destination number)"
#         }}},status=status.HTTP_404_NOT_FOUND)  


# class GetInsights(APIView):
#     permission_classes = (permissions.IsAuthenticated,GraphGroupPermission,InsightsGroupPermission)
#     uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"

#     def get(self,request):
#         #the mongodb handler with CRUD operations
#         mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=str(request.user.username),max_records=7)

#         insights_data = mongodb_handler.get_insights(request.user.username)
#         print(insights_data)
#         # if insights_data:
#         #     serializer = GetInsightsSerializer(data=insights_data)
#         #     if serializer.is_valid(raise_exception=True):
#         return Response(insights_data,status=status.HTTP_200_OK)
    
#         # return Response({"error":"user dont have insights"},status=status.HTTP_204_NO_CONTENT)


# class UpdateInsights(APIView):
#     permission_classes = (permissions.IsAuthenticated,GraphGroupPermission,InsightsGroupPermission)
#     uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"

#     def post(self,request):

#         serializer = UpdateInsightsSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):

#             #the mongodb handler with CRUD operations
#             mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=str(request.user.username),max_records=7)

#             #graph calculator instance
#             graph_calculations = GraphCalculator(user=request.user.usernamem,last_save="",db=[Income,Outcome],db_func=[Sum])

#             calculated_data = graph_calculations.get_data_by_year(years = serializer.data["year"],db = serializer.data["db"])

#             mongodb_handler.update_insights(calculated_data)

#             return Response(calculated_data,status=status.HTTP_201_CREATED)
            
#         else:
#             return Response({"error":"user input vas invalid"},status=status.HTTP_404_NOT_FOUND)


# class AddInsights(APIView):
#     permission_classes = (permissions.IsAuthenticated,GraphGroupPermission,InsightsGroupPermission)
#     uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"

#     def post(self,request):

#         serializer = AddInsightsSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):

#             #the mongodb handler with CRUD operations
#             mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=str(request.user.username),max_records=7)


#             #graph calculator instance
#             graph_calculations = GraphCalculator(user=request.user.username,last_save="",db=[Income,Outcome],db_func=[Sum])


#             calculated_data = graph_calculations.get_data_by_year(year = serializer.data["year"],db = serializer.data["db"])
            

#             calculated_dict = {"db":calculated_data[1],"data":calculated_data[0]}


#             added_record = mongodb_handler.add_insights(calculated_dict,max_amount=4)
#             if added_record:
#                 return Response(calculated_dict,status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"error":"max capacity exceded"},status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({"error":"user input vas invalid"},status=status.HTTP_404_NOT_FOUND)

 
# class DeleteInsights(APIView):
#     permission_classes = (permissions.IsAuthenticated,GraphGroupPermission,InsightsGroupPermission)
#     uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"

#     def post(self,request):

#         serializer = DeleteInsightsSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):

#             #the mongodb handler with CRUD operations
#             mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=str(request.user.username),max_records=7)

#             deleted = mongodb_handler.delete_insights(str(serializer.data["insights_id"]))
#             if deleted:
#                 return Response({"you deleted the insight successfully"},status=status.HTTP_200_OK)
#             else:
#                 return Response({"error":"records not exists"},status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({"error":"user input vas invalid"},status=status.HTTP_404_NOT_FOUND)
