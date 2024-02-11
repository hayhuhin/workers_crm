from rest_framework import serializers
from dashboard.func_tools.graph_calculations import GraphCalculator
from dashboard.mongo_db_graph.mongodb_connector import MongoDBConstructor
from finance.models import Income,Outcome
from django.db.models import Sum
from employer.models import Employer
from django.conf import settings 
import time

#time of utc then making it local time and representing as a string 
current_time_utc = time.gmtime()
gmtime_dict = time.localtime(time.mktime(current_time_utc) + 2 * 3600)
time_now = str(f"{gmtime_dict[0]}-{gmtime_dict[1]}-{gmtime_dict[2]}. {gmtime_dict[3]}:{gmtime_dict[4]}")



    #* later it will be usefull for our graph repr 
class GraphViewSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    db = serializers.CharField(max_length=50)
    collection = serializers.CharField(max_length=50)
    graph_permited = serializers.BooleanField(default=False)
    graph_db_type= serializers.CharField(max_length=50)
    graph_records = serializers.DictField(default={})
    ordered_list = serializers.ListField(default=[])



class CreateRecordSerializer(serializers.Serializer):
    database_name = serializers.ChoiceField(choices=[("income","Income"),("outcome","Outcome")],default=None)
    graph_title = serializers.CharField(max_length=100,default=None)
    graph_description = serializers.CharField(max_length=100,default=None)
    graph_type = serializers.CharField(max_length=100,default=None)
    start_date = serializers.CharField(max_length=100,default=None)
    end_date = serializers.CharField(max_length=100,default=None)


    def create(self,cleaned_data,user):
        allowed_fields = ["database_name","graph_title","graph_description","graph_type","start_date","end_date"]
        uri = settings.MONGODB_URI

        #* checkinf if passed empty json
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "json_example":{
                    "database_name":"income or outcome",
                    "graph_title":"title of the graph",
                    "graph_description":"graph description",
                    "graph_type":"bar_graph or line_graph",
                    "start_date":"the start date of the graph calculation",
                    "end_date":"the end date of the graph calculation"
                    }}
            return False,message

        #* checking if passed all required fields
        for item in allowed_fields:
            if item not in cleaned_data.keys():
                message = {"error":"you must pass all fields","required_fields":allowed_fields}
                return False,message


        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}


        #* this initializers are basic steps to get data,do something with data,save it in mongodb
        graph_calculator = GraphCalculator(user=user["username"],last_save="",db=[Income,Outcome],db_func=[Sum])
        mongodb_handler = MongoDBConstructor(uri=uri,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)


        #* creating graph data
        created_graph_data = graph_calculator.sum_by_range(start_date=cleaned_data["start_date"],end_date=cleaned_data["end_date"],db=cleaned_data["database_name"])
        #* checking that its really created the calculation
        if all(created_graph_data):
            # print(created_graph_data)


            create_record = {
                        "graph_title":cleaned_data["graph_title"],
                        "graph_description":cleaned_data["graph_description"],
                        "graph_type":cleaned_data["graph_type"],
                        "created_at" : time_now,
                        "x":created_graph_data[1],
                        "y":created_graph_data[0],
                        "y_2":[],
                        'sql_database':cleaned_data["database_name"],
                        "start_date":cleaned_data["start_date"],
                        "end_date":cleaned_data["end_date"],
                        }
            mongodb_handler.add_record(create_record)
            message = {"success":"created successfuly","created_data":create_record}
            print(message)
            return True,message
        else:
            message = created_graph_data[1]
            return False,message


class DeleteRecordSerializer(serializers.Serializer):
    position = serializers.IntegerField(default=None)
    all_records = serializers.BooleanField(default=False)

    def get_info(self,cleaned_data,user):
        #* checkinf if passed empty json
        allowed_fields = ["position","all_records"]
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "json_example":{
                    "position":"postition of the graph",
                    "all_records":"true or false"
                    }}
            return False,message

        #* checking that the user passed valid fields
        for item in cleaned_data.keys():
            if item not in allowed_fields:
                message = {"error":"passed invalid fields"}


        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}


        for key,value in self.__getattribute__("data").items():
            if key == "all_records" and value == True:
                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                records_data = mongodb_handler.graph_records()
                if records_data:
                    message = {"success":"found_records","all_records":records_data}
                    return True,message
                else:
                    message = {"error","no records exists"}
                    return False,message

            if key == "position" and value != None:
                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                found_data = mongodb_handler.get_record_by_position(int(cleaned_data["position"]))
                if all(found_data):
                    return True,found_data

                else:
                    return False,found_data

            message = {"error":"passed invalid values"}
            return False,message


    def delete(self,cleaned_data,user):

        #* checkinf if passed empty json
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "json_example":{
                    "position":"postition of the graph",
                    }}
            return False,message


        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}


        mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
        delete_action = mongodb_handler.remove_record(required_record=cleaned_data["position"])
        if all(delete_action):
            return True,delete_action[1]
        
        message = delete_action[1]
        return False,message
    

class UpdateRecordSerializer(serializers.Serializer):
    graph_title = serializers.CharField(max_length=100)
    graph_description = serializers.CharField(max_length=100)
    graph_type = serializers.CharField(max_length=100)
    db = serializers.CharField(max_length=100)
    start = serializers.CharField(max_length=100)
    end = serializers.CharField(max_length=100)
    graph_position = serializers.CharField(max_length=5)

    def update_record(self,graph_data):
        updated_record = {
                    "graph_title":self.validated_data.get("graph_title"),
                    "graph_description":self.validated_data.get("graph_description"),
                    "graph_type":self.validated_data.get("graph_type"),
                    "created_at" : time_now,
                    "x":graph_data[1],
                    "y":graph_data[0],
                    "y_2":[],
                    'sql_database':self.validated_data.get("db"),
                    "start_date":self.validated_data.get("start"),
                    "end_date":self.validated_data.get("end"),
                    }
        return updated_record
    


class CompareRecordSerializer(serializers.Serializer):
    src_position = serializers.CharField(max_length=5)
    dst_position = serializers.CharField(max_length=5)


class GetInsightsSerializer(serializers.Serializer):
    income_year = serializers.ListField()
    outcome_year = serializers.ListField()
    income_amount = serializers.ListField()
    outcome_amount = serializers.ListField()


class UpdateInsightsSerializer(serializers.Serializer):
    income_year = serializers.ListField()
    outcome_year = serializers.ListField()
    income_amount = serializers.ListField()
    outcome_amount = serializers.ListField()

    def to_json(self):
        pass


class AddInsightsSerializer(serializers.Serializer):
    db_options = [
        ("income","Income"),
        ("outcome","Outcome")]
    
    db = serializers.ChoiceField(choices=db_options)
    year = serializers.ListField()
    # amount = serializers.ListField()


class DeleteInsightsSerializer(serializers.Serializer):
    insights_id = serializers.CharField(max_length=12)