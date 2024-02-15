from rest_framework import serializers
from dashboard.func_tools.graph_calculations import GraphCalculator
from dashboard.mongo_db_graph.mongodb_connector import MongoDBConstructor
from finance.models import Income,Outcome
from django.db.models import Sum
from employer.models import Employer
from django.conf import settings 
import time

gmtime_dict = time.gmtime()
time_now = str(f"{gmtime_dict[0]}-{gmtime_dict[1]}-{gmtime_dict[2]}. {gmtime_dict[3]}:{gmtime_dict[4]}")




class CompareRecordSerializer(serializers.Serializer):
    src_position = serializers.CharField(max_length=5,default=None)
    dst_position = serializers.CharField(max_length=5,default=None)


    def get_info(self,cleaned_data,user):

        message = {
            "error":"you need to pass data as post request",
            "json_example_of_post_request":{
                "src_position":"source position of the required graph that you want to compare with",
                "dst_position":"destination position of the required graph that you want to be compared with"
                }}
        return False,message

    def compare(self,cleaned_data,user):
        required_fields = ["src_position","dst_position"]
        #* checking that the user passed valid fields
        for item in required_fields:
            if item not in cleaned_data.keys():
                message = {"error":"must pass all required fields","required_fields":required_fields}
                return False,message

        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}


        #* main classed that handle the calc and the mongodb CRUD operations
        mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
        compared_data = mongodb_handler.compare_record(position_1=cleaned_data["src_position"],position_2=cleaned_data["dst_position"])

        if not all(compared_data):
            message = {"error":compared_data[1]}
            return False,message

        else:
            message = {"success":compared_data[1]}
            return True,message



class SwitchRecordSerializer(serializers.Serializer):
    src_position = serializers.CharField(max_length=5,default=None)
    dst_position = serializers.CharField(max_length=5,default=None)

    def get_info(self,cleaned_data,user):

        message = {
            "error":"you need to pass data as post request",
            "json_example_of_post_request":{
                "src_position":"source position of the required graph that you want to compare with",
                "dst_position":"destination position of the required graph that you want to be compared with"
                }}
        return False,message

    def switch(self,cleaned_data,user):
        required_fields = ["src_position","dst_position"]
        #* checking that the user passed valid fields
        for item in required_fields:
            if item not in cleaned_data.keys():
                message = {"error":"must pass all required fields","required_fields":required_fields}
                return False,message

        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}


        #* main classed that handle the calc and the mongodb CRUD operations
        mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
        switched_data = mongodb_handler.switch_records(src_position=cleaned_data["src_position"],dst_position=cleaned_data["dst_position"])

        if not all(switched_data):
            message = switched_data[1]
            return False,message

        else:
            message = switched_data[1]
            return True,message


