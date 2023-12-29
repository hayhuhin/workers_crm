from rest_framework import serializers
from rest_framework.authtoken.models import Token
import time

gmtime_dict = time.gmtime()
time_now = str(f"{gmtime_dict[0]}-{gmtime_dict[1]}-{gmtime_dict[2]}. {gmtime_dict[3]}:{gmtime_dict[4]}")





class GraphViewSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    db = serializers.CharField(max_length=50)
    collection = serializers.CharField(max_length=50)
    graph_permited = serializers.BooleanField(default=False)
    graph_db_type= serializers.CharField(max_length=50)
    graph_records = serializers.DictField(default={})
    ordered_list = serializers.ListField(default=[])


class AddRecordSerializer(serializers.Serializer):
    graph_title = serializers.CharField(max_length=100)
    graph_description = serializers.CharField(max_length=100)
    graph_type = serializers.CharField(max_length=100)
    db = serializers.CharField(max_length=100)
    start = serializers.CharField(max_length=100)
    end = serializers.CharField(max_length=100)


    def serialize(self,graph_data):
        new_record = {
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
        return new_record
    

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
    

class DeleteRecordSerializer(serializers.Serializer):
    position = serializers.CharField(max_length=5)



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
