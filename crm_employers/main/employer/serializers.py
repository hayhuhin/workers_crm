from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from .models import Employer
from user.models import User


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ["first_name","last_name","email","phone"]


class AddProfileSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Employer
        fields = ["first_name","last_name","email","phone"]
        # fields = ["first_name","last_name","email","phone",""]

    def create(self,cleaned_data):
        data = {}
        user_instance = User.objects.get(email=cleaned_data["email"])

        try:
            status = "HTTP_201_CREATED"
            employer_obj = Employer.objects.create(
                user=user_instance,
                first_name=cleaned_data["first_name"],
                last_name=cleaned_data["last_name"],
                email=cleaned_data["email"],
                phone=cleaned_data["phone"],)
            employer_obj.save()
            data["first_name"] = cleaned_data["first_name"]
            data["last_name"] = cleaned_data["last_name"]
            return data,status
        
        except:
            error_message = {"error":"this user is already exists as employer"}
            status = "HTTP_404_NOT_FOUND"
            return error_message,status


#! fic the class output
class GetProfileSerializer(serializers.Serializer):

    choices = [
    ("specific","Specific"),
    ("all","All")]
    request_options = serializers.ChoiceField(choices=choices)
    email = serializers.EmailField(default="no email provided")

    def get_request(self,cleaned_data):

        #* specific user search
        if cleaned_data["request_options"] == "specific":

            #* have to make sure that the user is exists
            try:
                specific_employer = Employer.objects.get(email=cleaned_data["email"])
                serializer = EmployerSerializer(specific_employer)
                employer_json = {"first_name":serializer.data["first_name"],"email":serializer.data["email"]}
                return employer_json
            
            except:
                error_message = {"error":"employer not exists"}
                return error_message
            
        #* all users search
        if cleaned_data["request_options"] == "all":
            all_employers = Employer.objects.all()
            employer_json = {}
            for employer in all_employers:
                serializer = EmployerSerializer(employer)
                repr_data = {"first_name":serializer.data["first_name"],"email":serializer.data["email"]}
                employer_json[str(employer)] = repr_data
            return employer_json



class DeleteProfileSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    
    def validate_user_id(self,value):
        if not Employer.objects.get(pk=value).exists():
            raise serializers.ValidationError("this user is not exists")
        return value
