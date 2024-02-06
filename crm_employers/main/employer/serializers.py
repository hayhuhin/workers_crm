from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from .models import Employer
from user.models import User
from django.db.models import Q,F


#* each class with the name employer in it is a high previlage serializers that done by the admin,hr,managers employers
#! must re create this whole seralizers
#* general serializers

class EmployerSerializer(serializers.ModelSerializer):
    """
    main model serializer class of the Employer model.
    this needed to represent the values as json
    """
    class Meta:
        model = Employer
        fields = ["first_name","last_name","email","phone"]


class GeneralEmployerSerializer(serializers.Serializer):
    user = serializers.EmailField(default=None)
    first_name = serializers.CharField(max_length=50,default=None)
    last_name = serializers.CharField(max_length=50,default=None)
    email = serializers.EmailField(default=None)
    phone = serializers.CharField(max_length=50,default=None)
    job_position = serializers.CharField(default=None)
    # lead = serializers.IntegerField(default=None)
    # task = serializers.IntegerField(default=None)
    #! need to uncomment it after fixing the dashboard application
    # graph_permission = models.ManyToManyField(GraphPermission,default=None)
    # insights_permission = models.ManyToManyField(GraphInsights,default=None)

    def check_unique(self,cleaned_data):
        """
        this method will check if there is already existing data with the same id.

        unique fields are customer_id,email
        """

        for key in cleaned_data.keys():
            #* checking if the employer already exists under the required user 
            if key == "user":
                required_user_exists = User.objects.filter(email=cleaned_data["user"]).exists()
                if required_user_exists:
                    #* this removes the user and will be added user object instead
                    user_obj = User.objects.get(email=cleaned_data["user"])

                    #* now check if employer already exists with this user data

                    employer_exists = Employer.objects.filter(user=user_obj).exists()
                    if employer_exists:
                        message = {"error":"cant cange this employer to the required user because this user is already exists as employer"}
                        return False,message
                    
                    cleaned_data["user"] = user_obj
                    # cleaned_data["email"] = user_obj.email
                    
                else:
                    message = {"error":"this user not exists"}
                    return False,message

            #TODO job positions not exists yet
            if key == "job_position":
                job_position_exists = Employer.objects.filter(job_position=cleaned_data["job_position"]).exists()
                if job_position_exists:
                    #* this removes the assigned to email and changes it to the assigned to object
                    job_obj = Employer.objects.get(job_position=cleaned_data["job_position"])
                    cleaned_data["job_position"] = job_obj
                   
                else:
                    message = {"error","this job position not exists with the provided details"}
                    return False,message

        #* this happens only if the user object is changed so it will change the email too                
        if "user" in cleaned_data.keys():
            cleaned_data["email"] = user_obj.email

        # #* removing the unecesery data to make clean cleaned_data
        # unnecesery_data = ["customer_id"]
        # for data in unnecesery_data:
        #     if data in  cleaned_data.keys():
        #         cleaned_data.pop(data)


        #* returning cleaned data with the objects inside that can be used to update the database
        return True,cleaned_data




#* employer serializers

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

        required_fields = ["first_name","last_name","email","phone"]

        for fields in required_fields:
            if fields not in cleaned_data.keys():
                message = {"error":"invalid fields passed","required_fields":required_fields}
                return False,message
            
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
                "first_name":"john",
                "last_name":"doe",
                "email":"existing user email address",
                "phone":"the phone number"
            }}
            return False,message
        

        #*checking if the employer is already exists
        employer_exists = Employer.objects.filter(email=cleaned_data["email"]).exists()
        if employer_exists:
            message = {"this employer is already exists and cant be created again"}
            return False,message
        
        data = {}

        user_exist = User.objects.filter(email=cleaned_data["email"]).exists()
        if user_exist:
            user_instance = User.objects.get(email=cleaned_data["email"])
            cleaned_data["user"] = user_instance

        else:
            message = {"error":"user not exists with the provided email"}
            return False,message
        #TODO add the department,lead,task foreign key later


        employer_obj = Employer()
        for key,value in cleaned_data.items():
            setattr(employer_obj,key,value)

        employer_obj.save()
        employer_id = employer_obj.id
        employer_data = Employer.objects.filter(id=employer_id).values("first_name","last_name","email","phone","created_at")

        return True,employer_data
    

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
    email = serializers.EmailField(default=None)
    

    def get_info(self,cleaned_data):
        allowed_fields = ["email"]


        #* checking if passed empty json
        if not cleaned_data.keys():
            message = {"error":"passed empty json","json_example":{
                "email":"employer1@work.com"
            }}
            return False,message
        
        #* checking that the user passed only the allowed fields
        for item in cleaned_data.keys():
            if item not in allowed_fields:
                message = {"error":"passed invalid field","allowed_fields":allowed_fields}
                return False,message
            
        #* checking if employer exists the provided email
        employer_exists = Employer.objects.filter(email=cleaned_data["email"]).exists()
        if employer_exists:
            employer_data = Employer.objects.filter(email=cleaned_data["email"]).values("first_name","last_name","email","phone")

            message = {"success":"employer exists","employer_info":employer_data}
            return True,message

        message = {"error":"employer not exists or invalid"}        
        return False,message


    def delete(self,cleaned_data):
        allowed_fields = ["email"]


        #* checking if passed empty json
        if not cleaned_data.keys():
            message = {"error":"passed empty json","json_example":{
                "email":"employer1@work.com"
            }}
            return False,message
        
        #* checking that the user passed only the allowed fields
        for item in cleaned_data.keys():
            if item not in allowed_fields:
                message = {"error":"passed invalid field","allowed_fields":allowed_fields}
                return False,message
            
        #* checking if employer exists the provided email
        employer_exists = Employer.objects.filter(email=cleaned_data["email"]).exists()
        if employer_exists:
            employer_obj = Employer.objects.get(email=-cleaned_data["email"])
            employer_obj.delete()
            message = {"success":"employer deleted successfully"}
            return True,message

        message = {"error":"employer not exists or invalid"}        
        return False,message

    
class UpdateEmployerSerializer(serializers.Serializer):
    email = serializers.EmailField(default=None)
    update_data = serializers.DictField(default=None)

    def get_info(self,cleaned_data):
        allowed_fields = ["email"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass email field","example_json":{
                "email":"customer@customer.com",
            }}
            return False,message
        
        #*checking for allowed fields
        for key in cleaned_data.keys():
            if key not in allowed_fields:
                message = {"error":f"passed invalid field -{key}-"}
                return False,message

        #this will have my query that will be passed later
        query = Q()

        #* this whole section is checking if the passed data is valid and returning error message or proccedes to the next stage
        for key,value in self.__getattribute__("data").items():
            if key == "email" and value != None:
                email_exists = Employer.objects.filter(email=value).exists()
                if email_exists: 
                    query &= Q(email=value)
                else:
                    message = {"error":"email not exist. try another field or check if you miss typed"}
                    return False,message

        query_data = Employer.objects.filter(query).values("first_name","last_name","email","phone","job_position")
        message = {"success":query_data}
        return True,message


    def update(self,cleaned_data):
        required_fields = ["email","update_data"]
        allowed_update_fields = ["user","first_name","last_name","email","phone","job_position"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass all this fields","example_json":{
                "lead_id":"id of the lead as integer",
                "update_data":{
                    "user":"user email",
                    "first_name":"john",
                    "last_name":"doe",
                    "email":"john_doe@electric.com",
                    "phone":"phone number",
                    "job_position":"engineer department"
                    }}}
            
            return False,message
        
        #*checking that the user passed all fields
        for field in required_fields:
            if field not in cleaned_data.keys():
                message = {"error":"you must pass all fields","json_example":{
                "email":"employer email",
                "update_data":{
                    "user":"user email",
                    "first_name":"john",
                    "last_name":"doe",
                    "email":"john_doe@electric.com",
                    "phone":"phone number",
                    "job_position":"engineer department"
                    },
                    "and you passed":cleaned_data.items()
                    }}
            
                return False,message

        #* checking that the user didnt pass additional fields and only the allowed in the update data
        for field in cleaned_data["update_data"].keys():
            if field not in allowed_update_fields:
                message = {"error":"passed invalid fields into the update_data json","json example of update_data":{
                    "user":"user email",
                    "first_name":"john",
                    "last_name":"doe",
                    "email":"john_doe@electric.com",
                    "phone":"phone number",
                    "job_position":"engineer department"
                    }}
                return False,message


        # #*checking if the user exists with the email provided
        user_exists = User.objects.filter(email=cleaned_data["email"]).exists()
        if not user_exists:
            message = {"error":"this user is not exist with this email"}
            return False,message


        #* checking that the user didnt pass empty update data dict
        if not cleaned_data["update_data"]:
            message = {"error":"you cant pass empty udpate_data ","json_example for updata_data":{
                    "user":"user email",
                    "first_name":"john",
                    "last_name":"doe",
                    "email":"john_doe@electric.com",
                    "phone":"phone number",
                    "job_position":"engineer department"
                    }}
            return False,message
        


        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralEmployerSerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=True):

            check_unique_fields = update_data_serializer.check_unique(cleaned_data=cleaned_data["update_data"])
            if all(check_unique_fields):
                update_obj = Employer.objects.get(email=cleaned_data["email"])

                update_data = check_unique_fields[1]

                for key,value in update_data.items():
                    setattr(update_obj,key,value)

                update_obj.save()
                message = {"success":"updated the required fields","updated_data":{
                    "first_name":update_obj.first_name,
                    "last_name":update_obj.last_name,
                    "email":update_obj.email,
                    "phone":update_obj.phone,
                    "email":update_obj.email,
                    "job_position":update_obj.job_position
                }}
                return True,message
            
            return False,check_unique_fields[1]

        message = {"error":"invalid update_data fields"}
        return False,message
