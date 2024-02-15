from rest_framework import serializers
from dashboard.func_tools.graph_calculations import GraphCalculator
from dashboard.mongo_db_graph.mongodb_connector import MongoDBConstructor
from finance.models import Income,Outcome
from employer.models import Employer
from django.db.models import Sum
from django.conf import settings

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




class UpdateInsightSerializer(serializers.Serializer):
     

    def post(self,request):

        serializer = UpdateInsightSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            #the mongodb handler with CRUD operations
            mongodb_handler = MongoDBConstructor(uri=self.uri,db="test",collection="test",user=str(request.user.username),max_records=7)

            #graph calculator instance
            graph_calculations = GraphCalculator(user=request.user.usernamem,last_save="",db=[Income,Outcome],db_func=[Sum])

            calculated_data = graph_calculations.get_data_by_year(years = serializer.data["year"],db = serializer.data["db"])

            mongodb_handler.update_insights(calculated_data)

            return Response(calculated_data,status=status.HTTP_201_CREATED)
            
        else:
            return Response({"error":"user input vas invalid"},status=status.HTTP_404_NOT_FOUND)


class DeleteInsightsSerializer(serializers.Serializer):
    insights_id = serializers.CharField(max_length=12)


