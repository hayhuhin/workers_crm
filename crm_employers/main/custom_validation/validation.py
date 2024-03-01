from rest_framework import serializers
from employer.models import Employer,Department,DepartmentTask
from finance.models import Customer
from user.models import User
from django.db.models import Q,F

#* here i will create my error messages class

class OutputMessages:

    @staticmethod
    def error_with_message(self,main_message:str,second_message:dict=None):
        if not second_message:
            error_message = {"error":main_message,}
            return False,error_message
        else:
            error_message = {"error":main_message,**second_message}
            return False,error_message

    @staticmethod
    def user_not_exsts(self,message=None):
        if not message:
            message = {"error":"user not exists"}
            return False,message
        else:
            return False,message
    @staticmethod
    def employer_not_exists(self,message=None):
        if not message:
            message = {"error":"employer not exists"}
            return False,message
        else:
            return False,message
    
    @staticmethod
    def data_not_found(self,message=None):
        if not message:
            message = {"error":"the required data not found"}
            return False,message
        else:
            return False,message
    
    
    @staticmethod
    def valid_data(self,main_message:str,second_message:dict=None):
        if not second_message:
            success_message = {"success":main_message,}
            return True,success_message
        else:
            success_message = {"success":main_message,**second_message}
            return True,success_message
        
    def success_and_object(self,main_message,output_object=None):
        if not output_object:
            success_message = {"success":main_message,}
            return True,success_message
        else:
            success_message = {"success":main_message,"object":output_object}
            return True,success_message
        

#* here i will create my general validation checks that will be used inside the serializers 

class CustomValidation(serializers.Serializer):

    def basic_validation(self,input_fields,required_fields,allowed_fields,user):
        #* check if passed empty json        
        if not input_fields.keys():
            main="passed empty jason"
            second = {"fields_required":required_fields}
            error_output = OutputMessages.error_with_message(main_message=main,second_message=second)
            return error_output
        
        #* check if passed invalid fields
        for valid_field in required_fields:
            if valid_field not in input_fields:
                main = "passed invalid field"
                second = {"required_fields":required_fields}
                output_error = OutputMessages.error_with_message(main_message=main,second_message=second)
                return output_error
        
        #* check if the user exists as user and have a company
        user_email = user["email"]
        user_exists = User.objects.filter(email=user_email).exists()
        if not user_exists:
            error_output = OutputMessages.user_not_exsts()
            return error_output
        else:
            user_object = User.objects.get(email=user_email)

        return OutputMessages
    

    def passed_valid_fields(self,input_fields,valid_fields):
        for field in input_fields.keys():
            if field not in valid_fields:
                main = "passed invalid field"
                second = {"valid_fields":valid_fields}
                output_error = OutputMessages.error_with_message(main_message=main,second_message=second)
                return output_error
            

    def exists_in_database(self,query_fields:dict,database:object):
        query = Q(**query_fields)
        query_exists = database.objects.filter(query).exists()
        if not query_exists:
            error_output = OutputMessages.error_with_message(main_message="data not found with the provided fields")
            return error_output
        else:
            database_obj = database.objects.get(query)
            success_output = OutputMessages.success_and_object(main_message="data found with the provided fields",output_object=database_obj)
            return success_output
        
