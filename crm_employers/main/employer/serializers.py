from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from .models import Employer
from user.models import User

#* each class with the name employer in it is a high previlage serializers that done by the admin,hr,managers employers


class EmployerSerializer(serializers.ModelSerializer):
    """
    main model serializer class of the Employer model.
    this needed to represent the values as json
    """
    class Meta:
        model = Employer
        fields = ["first_name","last_name","email","phone"]


class CreateEmployerSerializer(serializers.ModelSerializer):
    """
    creating the Employer
    """
    class Meta:
        model = Employer
        fields = ["first_name","last_name","email","phone"]
        # fields = ["first_name","last_name","email","phone",""]

    def create(self,cleaned_data):
        """
        creating the employer object if the email is already exists in the User model.
        the User model can be modified only by IT or System Admin
        """
        data = {}
        user_instance = User.objects.get(email=cleaned_data["email"])

        #TODO add the department,lead,task foreign key later

        try:
            employer_obj = Employer.objects.create(
                user=user_instance,
                first_name=cleaned_data["first_name"],
                last_name=cleaned_data["last_name"],
                email=cleaned_data["email"],
                phone=cleaned_data["phone"],)
            employer_obj.save()
            data["first_name"] = cleaned_data["first_name"]
            data["last_name"] = cleaned_data["last_name"]
            return True,data
        
        except:
            error_message = {"error":"this user is already exists as employer"}
            return False,error_message


class GetEmployerSerializer(serializers.Serializer):
    """
    getting the employer data.
    if specific so by the provided email
    or if all it will return all employers
    """

    choices = [
    ("specific","Specific"),
    ("all","All")]
    request_options = serializers.ChoiceField(choices=choices)
    email = serializers.EmailField(default="no email provided")

    def get_employer(self,cleaned_data):

        #* specific user search
        if cleaned_data["request_options"] == "specific":

            #* have to make sure that the user is exists
            try:
                specific_employer = Employer.objects.get(email=cleaned_data["email"])
                serializer = EmployerSerializer(specific_employer)
                employer_json = {"first_name":serializer.data["first_name"],"email":serializer.data["email"]}
                return True,employer_json
            
            except:
                data = {"no_data":"employer not exists"}
                return False,data
            
        #* all users search
        if cleaned_data["request_options"] == "all":
            all_employers = Employer.objects.all()
            employer_json = {}
            for employer in all_employers:
                serializer = EmployerSerializer(employer)
                repr_data = {"first_name":serializer.data["first_name"],"email":serializer.data["email"]}
                employer_json[str(employer)] = repr_data
            return True,employer_json


        error_message = {"error":"the data provided is not specific or all fields"}
        return False,error_message


class DeleteEmployerSerializer(serializers.Serializer):
    """
    deleting the employer from the database.
    """
    email = serializers.EmailField(default="no email provided")
    
    def validate_employer_exists(self,cleaned_data):

        try:
            employer = Employer.objects.get(email=cleaned_data["email"])
            serializer = EmployerSerializer(employer)
            return True,serializer.data["email"]
        
        except:
            error_message = {"error":"employer not exists"}
            return False,error_message


class UpdateEmployerSerializer(serializers.Serializer):
    email = serializers.EmailField(default="no email provided")
    required_field = serializers.DictField()

    def update_employer_fields(self,cleaned_data):
        unchangable_fields = ["id","user_id","email","created_at","job_position_id","department","groups","user","permission","permissions","admin","task","lead"]

        try:
            #getting the specific object
            employer = Employer.objects.get(email=cleaned_data["email"])

            for key,values in (cleaned_data["required_field"]).items():
                if key in unchangable_fields:
                    return False,{"error":f"unauthorized to edit this field : {key}"}
                
                setattr(employer,key,values)
            employer.save()

            serialized_employer = EmployerSerializer(employer)

            return True,serialized_employer.data

        except:
            error_message = {"error":f"the email is {cleaned_data['email']} the required_fields are {cleaned_data['required_field']}"}
            return False,error_message

