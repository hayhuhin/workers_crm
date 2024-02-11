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


#* general record serializers
class GeneralRecordSerializer(serializers.Serializer):
    sql_database = serializers.ChoiceField(choices=[("income","Income"),("outcome","Outcome")],default=None)
    graph_title = serializers.CharField(max_length=100,default=None)
    graph_description = serializers.CharField(max_length=100,default=None)
    graph_type = serializers.CharField(max_length=100,default=None)
    start_date = serializers.CharField(max_length=100,default=None)
    end_date = serializers.CharField(max_length=100,default=None)


    def special_fields(self,cleaned_data,user):
        """
        this method calculates the graph and does another calculations if the user updates one of these fields:
        "start_date","end_date","sql_database"

        returns the valid cleaned_data dict 
        """


        #* checkinf if the required_fields are passed
        special_fields_list = ["start_date","end_date","sql_database"]
        field_counter = 0
        for item in special_fields_list:
            if item in cleaned_data.keys():
                field_counter += 1
        if field_counter < 3 or field_counter == 0:
            message = {"error":"if you passing start_date,end_date or sql_database you must pass all three of these togheter"}
            return False,message

        #* getting the employer object 
        employer_obj = Employer.objects.get(email=user["email"])


        #* calculates the graph information again
        graph_calculator = GraphCalculator(user=user["username"],last_save="",db=[Income,Outcome],db_func=[Sum])
        mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)

        new_graph_data = graph_calculator.sum_by_range(start_date=cleaned_data["start_date"],end_date=cleaned_data["end_date"],db=cleaned_data["sql_database"])

        #* after creating the new x,y,y_2 we adding it to the cleaned_data dict

        # cleaned_data["x"] = new_graph_data[1]
        # cleaned_data["y"] = new_graph_data[2]
        # print(new_graph_data)
        if not all(new_graph_data):
            return False,new_graph_data
        

        cleaned_data["y"] = new_graph_data[0]#the values of the cum
        cleaned_data["x"] = new_graph_data[1]#the dates of the sum MM-DD
        return True,cleaned_data


#* record CRUD operations serializers
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
            if key == "all_records" and value is True:
                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                records_data = mongodb_handler.graph_records()
                if records_data:
                    message = {"success":"found_records","all_records":records_data}
                    return True,message
                else:
                    message = {"error","no records exists"}
                    return False,message
                
            if key == "all_records" and value != True:
                message = {"error":"passed invalid values"}
                return False,message

            if key == "position" and value != None:
                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                found_data = mongodb_handler.get_record_by_position(int(cleaned_data["position"]))
                if all(found_data):
                    return True,found_data

                else:
                    return False,found_data

            # else:
            #     message = {"error":"passed invalid values"}
            #     return False,message

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

    position = serializers.IntegerField(default=None)
    all_records = serializers.BooleanField(default=False)
    update_data = serializers.DictField(default = None)
    # database_name = serializers.ChoiceField(choices=[("income","Income"),("outcome","Outcome")],default=None)
    # graph_title = serializers.CharField(max_length=100,default=None)
    # graph_description = serializers.CharField(max_length=100,default=None)
    # graph_type = serializers.CharField(max_length=100,default=None)
    # start_date = serializers.CharField(max_length=100,default=None)
    # end_date = serializers.CharField(max_length=100,default=None)


    def get_info(self,cleaned_data,user):
        #* checkinf if passed empty json
        allowed_fields = ["position","all_records"]
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "json_example":{
                    "":"postition of the graph",
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
            if key == "all_records" and value is True:
                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                records_data = mongodb_handler.graph_records()
                if records_data:
                    message = {"success":"found_records","all_records":records_data}
                    return True,message
                else:
                    message = {"error","no records exists"}
                    return False,message
                
            if key == "all_records" and value != True:
                message = {"error":"passed invalid values"}
                return False,message

            if key == "position" and value != None:
                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                found_data = mongodb_handler.get_record_by_position(int(cleaned_data["position"]))
                if all(found_data):
                    return True,found_data

                else:
                    return False,found_data

            # else:
            #     message = {"error":"passed invalid values"}
            #     return False,message



    def update(self,cleaned_data,user):
        allowed_update_fields = ["sql_database","graph_title","graph_description","graph_type","start_date","end_date"]
        required_fields = ["position","update_data"]

        #* checkinf if passed empty json
        if not cleaned_data.keys():
            message = {"error":"passed empty json","example_json":{
                "position":1,
                "update_data":{
                    "sql_database":"the sql database",
                    "graph_title":"title of the graph",
                    "graph_description":"some description",
                    "graph_type":"bar_graph or line_graph",
                    "start_date":"YYYY-MM-DD",
                    "end_date":"YYYY-MM-DD"
                }}}
            return False,message
        
        #* checking if passed the required fields
        for item in required_fields:
            if item not in cleaned_data.keys():
                message = {"error":"passed invalid fields","json_example":{
                "position":1,
                "update_data":{
                    "sql_database":"the sql database",
                    "graph_title":"title of the graph",
                    "graph_description":"some description",
                    "graph_type":"bar_graph or line_graph",
                    "start_date":"YYYY-MM-DD",
                    "end_date":"YYYY-MM-DD"
                }}}
                return False,message

        #* checking that the user passed valid fields in the update data
        for item in cleaned_data["update_data"].keys():
            if item not in allowed_update_fields:
                message = {"error":"passed invalid fields in the update data","update_data_example":{
                    "sql_database":"the sql database",
                    "graph_title":"title of the graph",
                    "graph_description":"some description",
                    "graph_type":"bar_graph or line_graph",
                    "start_date":"YYYY-MM-DD",
                    "end_date":"YYYY-MM-DD"
                }}
                return False,message

        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}

        #* this initializers are basic steps to get data,do something with data,save it in mongodb
        graph_calculator = GraphCalculator(user=user["username"],last_save="",db=[Income,Outcome],db_func=[Sum])
        mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)

        #* checking if the record exists
        record_data_exists = mongodb_handler.get_record_by_position(position=cleaned_data["position"])
        if not all(record_data_exists):
            return False,record_data_exists[1]
        current_record_data = record_data_exists[1]


        update_data_serializer = GeneralRecordSerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=True):
            validated_data = update_data_serializer.special_fields(cleaned_data=cleaned_data["update_data"],user=user)
            
            if not all(validated_data):
                message = validated_data[1]
                return False,message
            
            #* this block is taking the old record fields and changing only the ones that user wan to change
            position = cleaned_data["position"]
            new_dict = current_record_data[str(position)]
            for key,value in validated_data[1].items():
                new_dict[key] = value

            mongodb_handler.edit_record(record_position=position,edit_data=new_dict)
            message = {"success":"update all required fields successfully","updated_data":new_dict}
            return True,message
        
            #* now we formatting the data so it can fit into our mongodb 
            # updated_record = {
            #             "graph_title":new_dict["graph_title"],
            #             "graph_description":new_dict["graph_description"],
            #             "graph_type":new_dict["graph_type"],
            #             "created_at" : time_now,
            #             "x":new_dict["x"],
            #             "y":new_dict["y"],
            #             "y_2":[],
            #             'sql_database':new_dict["sql_database"],
            #             "start_date":new_dict["start_date"],
            #             "end_date":new_dict["end_date"],
            #             }
            # print(updated_record)
            # print(40*"g")
            # print(new_dict)


        message = {"error":"invlid update data fields or values"}
        return False,message

        # updated_record = {
        #             "graph_title":self.validated_data.get("graph_title"),
        #             "graph_description":self.validated_data.get("graph_description"),
        #             "graph_type":self.validated_data.get("graph_type"),
        #             "created_at" : time_now,
        #             "x":graph_data[1],
        #             "y":graph_data[0],
        #             "y_2":[],
        #             'sql_database':self.validated_data.get("db"),
        #             "start_date":self.validated_data.get("start"),
        #             "end_date":self.validated_data.get("end"),
        #             }
        # return updated_record
    

class GetRecordSerializer(serializers.Serializer):
    position = serializers.IntegerField(default=None)
    all_records = serializers.BooleanField(default=False)

    def get_info(self,cleaned_data,user):
        #* checking if passed empty json
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
            if key == "all_records" and value is True:
                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                records_data = mongodb_handler.graph_records()
                if records_data:
                    message = {"success":"found_records","all_records":records_data}
                    return True,message
                else:
                    message = {"error","no records exists"}
                    return False,message
                
            if key == "all_records" and value != True:
                message = {"error":"passed invalid values"}
                return False,message

            if key == "position" and value != None:
                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                found_data = mongodb_handler.get_record_by_position(int(cleaned_data["position"]))
                if all(found_data):
                    return True,found_data

                else:
                    return False,found_data

