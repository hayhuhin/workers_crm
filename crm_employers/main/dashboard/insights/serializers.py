from rest_framework import serializers
from dashboard.func_tools.graph_calculations import GraphCalculator
from dashboard.mongo_db_graph.mongodb_connector import MongoDBConstructor
from finance.models import Income,Outcome
from employer.models import Employer
from django.db.models import Sum
from django.conf import settings


#* general serializers

class GeneralInsightSerializer(serializers.Serializer):
    db_options = [
        ("income","Income"),
        ("outcome","Outcome")]
    
    graph_database = serializers.ChoiceField(choices=db_options,default=None )
    year_list = serializers.ListField(max_length=5,default=None)

    def check_something(self,cleaned_data):
        return cleaned_data



#* insights operations

class GetInsightSerializer(serializers.Serializer):
    all_insights = serializers.BooleanField(default=False)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["all_insights"]
        
        #* checking if passed empty json
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "pass one of these fields":{
                    "all_insights":"boolean True or False",
                    }}
            return False,message
        
        #* checking if passed valid fields
        for item in cleaned_data.keys():
            if item not in allowed_fields:
                message = {"error":"you must pass at leas one of fields","required_fields":allowed_fields}
                return False,message


       
        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}




        for key,value in self.__getattribute__("data").items():
            if key == "all_insights" and value is True:

                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                records_data = mongodb_handler.get_insights(user=user["username"])
                
                if records_data:
                    message = {"success":"found_records","all_records":records_data}

                    return True,message
                else:
                    message = {"error","no records exists"}
                    return False,message
                

        message = {"error":"invalid value passed"}
        return False,message


class CreateInsightSerializer(serializers.Serializer):
    db_options = [
        ("income","Income"),
        ("outcome","Outcome")]
    
    graph_database = serializers.ChoiceField(choices=db_options,default=None )
    year_list = serializers.ListField(max_length=5,default=None)


    def get_info(self,cleaned_data,user):
        allowed_fields = ["graph_database","year_list"]

        #* returning json example for every get request
        message = {
            "error":"passed empty json",
            "json_example":{
                "graph_database":"income or outcome",
                "year_list":"['2023','2024','2025'] max of 5 years",
                }}
        return True,message

    
    def create(self,cleaned_data,user):
        allowed_fields = ["graph_database","year_list"]

        #* checkinf if passed empty json
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "json_example":{
                    "graph_database":"income or outcome",
                    "year_list":"['2023','2024','2025'] max of 5 years",
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
            return False,message


        #* this initializers are basic steps to get data,do something with dat and save it in mongodb
        graph_calculation = GraphCalculator(user=user["username"],last_save="",db=[Income,Outcome],db_func=[Sum])
        mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)


        calculated_year_data = graph_calculation.get_data_by_year(year=cleaned_data["year_list"],db_name=cleaned_data["graph_database"])
        calculated_dict = {"db":calculated_year_data[1],"data":calculated_year_data[0]}


        added_record = mongodb_handler.add_insights(calculated_dict,max_amount=20)
        if not added_record:
            message = {"error":"exceeded the max amount that allowed"}
            return False,message

        message = {"success","added the insight into the database"}
        return True,message


#TODO need to think further about this operation(maybe this method not necesery)
class UpdateInsightSerializer(serializers.Serializer):
    all_insights = serializers.BooleanField(default=False)
    insight_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default=None)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["all_insights"]
        
        #* checking if passed empty json
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "pass one of these fields":{
                    "all_insights":"boolean True or False",
                    }}
            return False,message
        
        #* checking if passed valid fields
        for item in cleaned_data.keys():
            if item not in allowed_fields:
                message = {"error":"you must pass at leas one of fields","required_fields":allowed_fields}
                return False,message


       
        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}




        for key,value in self.__getattribute__("data").items():
            if key == "all_insights" and value is True:

                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                records_data = mongodb_handler.get_insights(user=user["username"])
                
                if records_data:
                    message = {"success":"found_records","all_records":records_data}

                    return True,message
                else:
                    message = {"error","no records exists"}
                    return False,message
                

        message = {"error":"invalid value passed"}
        return False,message

 
     

    def update(self,cleaned_data,user):

        required_fields = ["insight_id","update_data"]
        
        #* checking if passed empty json
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "you must pass the insight id":{
                    "insight_id":"integer",
                    "update_data":{
                        "graph_database":"some database",
                        "year_list":"['2023','2025'] up to 5 years"
                    }
                    }}
            
            return False,message
        
        #* checking if passed valid fields
        for item in required_fields:
            if item not in cleaned_data.keys():
                message = {"error":"you must pass all the required fields","required_fields":required_fields}
                return False,message


       
        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}



        for key,value in self.__getattribute__("data").items():
            if key == "insight_id" and value != None:

                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                found_records= mongodb_handler.get_insights(user=user["username"])
                if found_records:
                    for item in found_records.keys():
                        if value == item:
                            record_exists = found_records
                
                else:
                    message = {"error":"no records found"}
                    return False,message
            
            if key == "update_data" and value != None:
                general_serializer = GeneralInsightSerializer(data=value)
                if general_serializer.is_valid():
                    update_data = general_serializer.data
                else:
                    message = {"error":"invalid values in the update_data"}

            if key == "update_data" and value == None:
                message = {"error":"cabnt pass empty update data","update_data":{
                        "graph_database":"some database",
                        "year_list":'["2023","2025"] up to 5 years'
                    }}
                return False,message



        #* this section is where the calculations starts and the user passed valid fields








        # serializer = UpdateInsightSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):

        #     #the mongodb handler with CRUD operations
        #     mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=str(request.user.username),max_records=7)

        #     #graph calculator instance
        #     graph_calculations = GraphCalculator(user=request.user.usernamem,last_save="",db=[Income,Outcome],db_func=[Sum])

        #     calculated_data = graph_calculations.get_data_by_year(years = serializer.data["year"],db = serializer.data["db"])

        #     mongodb_handler.update_insights(calculated_data)

        #     return Response(calculated_data,status=status.HTTP_201_CREATED)
            
        # else:
        #     return Response({"error":"user input vas invalid"},status=status.HTTP_404_NOT_FOUND)


class DeleteInsightSerializer(serializers.Serializer):
    insights_id = serializers.IntegerField(default=None)
    all_insights = serializers.BooleanField(default=None)


    def get_info(self,cleaned_data,user):
        allowed_fields = ["all_insights"]
        
        #* checking if passed empty json
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "pass one of these fields":{
                    "all_insights":"boolean True or False",
                    }}
            return False,message
        
        #* checking if passed valid fields
        for item in cleaned_data.keys():
            if item not in allowed_fields:
                message = {"error":"you must pass at leas one of fields","required_fields":allowed_fields}
                return False,message


       
        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}




        for key,value in self.__getattribute__("data").items():
            if key == "all_insights" and value is True:

                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                records_data = mongodb_handler.get_insights(user=user["username"])
                
                if records_data:
                    message = {"success":"found_records","all_records":records_data}

                    return True,message
                else:
                    message = {"error","no records exists"}
                    return False,message
                

        message = {"error":"invalid value passed"}
        return False,message

    
    def delete(self,cleaned_data,user):

        required_fields = ["insight_id"]
        
        #* checking if passed empty json
        if not cleaned_data.items():
            message = {
                "error":"passed empty json",
                "you must pass the insight id":{
                    "insight_id":"integer of the id"
                    }}
            
            return False,message
        
        #* checking if passed valid fields
        for item in required_fields:
            if item not in cleaned_data.keys():
                message = {"error":"you must pass all the required fields","required_fields":required_fields}
                return False,message


       
        #* checking if the user is exists as employer
        user_exists_as_employer = Employer.objects.filter(email=user["email"]).exists()
        if user_exists_as_employer:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"user not exists as employer"}



        for key,value in self.__getattribute__("data").items():
            if key == "insight_id" and value != None:

                mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
                found_records = mongodb_handler.get_insights(user=user["username"])
                if not found_records:
                    message = {"error":"no records found"}
                    return False,message
        
        #* checkinf if the specific provided id is exists
        mongodb_handler = MongoDBConstructor(uri=settings.MONGODB_URI,db="test",collection=employer_obj.graph_db,user=user["username"],max_records=7)
        found_records = mongodb_handler.get_insights(user=user["username"])

        for item in found_records.keys():
            if item == cleaned_data["insight_id"]:
                mongodb_handler.delete_insights(insights_id=item)
                message = {"success":"deleted successfully the required insight"}
                return True,message
            else:
                message = {"error":"the provided id is not exists"}
                return False,message


        #* this section is where the calculations starts and the user passed valid fields





