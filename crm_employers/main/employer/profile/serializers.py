from rest_framework import serializers
from employer.models import Employer



#*general profile serializer

class GeneralProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(default = None)
    last_name = serializers.CharField(default = None)
    phone = serializers.CharField(default = None)


class EmployerSerializer(serializers.ModelSerializer):
    """
    main model serializer class of the Employer model.
    this needed to represent the values as json
    """
    class Meta:
        model = Employer
        fields = ["first_name","last_name","email","phone"]


class GetProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(default="no email provided")


    def get_profile(self,cleaned_data):
        allowed_fields = ["email"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json example":{
                "email":"specific employer email"
            }}
            return False,message

        #* checking allowed fields
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"passed invalid field","the allowed fields are":allowed_fields}
                return False,message
        
        #*checking if the employer exists with this email
        employer_exists = Employer.objects.filter(email=cleaned_data["email"]).exists()
        if employer_exists:
            employer_data = Employer.objects.filter(email=cleaned_data["email"]).values("first_name","last_name","email","phone")
            message = {"success":"found the user successfully","user_profile":employer_data}
            return True,message

        message = {"error":"employer not exists with the email provided"}
        return False,message


class UpdateProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(default=None)
    update_data = serializers.DictField(default = None)


    def get_info(self,cleaned_data):
        allowed_fields = ["email"]

        
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"cant pass fields"}
                return False,message
            
        #* checking if the employer exists
        employer_exists = Employer.objects.filter(email=cleaned_data["email"]).exists()
        if employer_exists:
            employer_data = Employer.objects.filter(email=cleaned_data["email"]).values("first_name","last_name","phone","email")
            message = {"success":employer_data}
            return True,message
        
        message = {"error":"employer profile not exists with the provided email"}
        return False,message
    

    def update_profile(self,cleaned_data):
        required_fields = ["update_data","email"]
        allowed_update_fields = ["phone","first_name","last_name"]

        #checking if passed empty json
        if not cleaned_data.keys():
            message = {"error":"passed empty json","json_example":{
                "update_data":{
                    "first_name":"required new first name",
                    "last_name":"required new last name",
                    "phone":"new phone number"
                }}}
            return False,message
        
        #* checking if passed empty update_data json
        if not cleaned_data["update_data"].keys():
            message = {"error":"cant pass empty json into update_data","update_data json_example":{
                    "first_name":"required new first name",
                    "last_name":"required new last name",
                    "phone":"new phone number"
                }}
            return False,message
        

        #* checking that the user didnt pass additional fields
        for field in cleaned_data.keys():
            if field not in required_fields:
                message = {"error":"invalid field passed"}
                return False,message

        for field in cleaned_data["update_data"].keys():
            if field not in allowed_update_fields:
                message = {"error":"invalid fields passed in the update_data","example_json":{
                    "first_name":"required new first name",
                    "last_name":"required new last name",
                    "phone":"new phone number"
                }}
                return False,message
        

        #* checking if the nested dict fields are good in another serializer 
        update_data = GeneralProfileSerializer(data=cleaned_data["update_data"])
        if update_data.is_valid(raise_exception=True):
            #*checking if the profile exists
            profile_exists = Employer.objects.filter(email=cleaned_data["email"]).exists()
            if profile_exists:
                profile_obj = Employer.objects.get(email=cleaned_data["email"])
                #* updating the profile with the new data
                for item,item_value in cleaned_data["update_data"].items():
                    setattr(profile_obj,item,item_value)
                profile_obj.save()

                message = {"success":"updated successfully the profile","updated_fields":{
                    "first_name":profile_obj.first_name,
                    "last_name":profile_obj.last_name,
                    "phone":profile_obj.phone
                }}

                return True,message

            message = {"error":"profile not exists"}
            return False,message

        message = {"error":"invalid fields passed in the update_data "}
        return False,message

        
