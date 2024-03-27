from rest_framework import serializers
from employer.models import Employer,Department,DepartmentTask
from finance.models import Customer
from user.models import User
from django.db.models import Q,F

#* here i will create my error messages class

class OutputMessages:

    @staticmethod
    def error_with_message(main_message:str,second_message:dict=None):
        if not second_message:
            error_message = {"error":main_message,}
            return False,error_message
        else:
            error_message = {"error":main_message,**second_message}
            return False,error_message

    @staticmethod
    def user_not_exsts(message=None):
        if not message:
            message = {"error":"user not exists"}
            return False,message
        else:
            return False,message
    @staticmethod
    def employer_not_exists(message=None):
        if not message:
            message = {"error":"employer not exists"}
            return False,message
        else:
            return False,message
    
    @staticmethod
    def data_not_found(message=None):
        if not message:
            message = {"error":"the required data not found"}
            return False,message
        else:
            return False,message
    
    
    @staticmethod
    def success_with_message(main_message:str,second_message:dict=None):
        if not second_message:
            success_message = {"success":main_message}
            return True,success_message
        else:
            success_message = {"success":main_message,**second_message}
            return True,success_message
        
    def success_and_object(main_message,output_object):

        success_message = {"success":main_message,"object":output_object}
        return True,success_message
        

#* here i will create my general validation checks that will be used inside the serializers 

class CustomValidation:

    def basic_validation(self,user:dict=True,input_fields:dict = None,required_fields:list=None,allowed_fields:list=None,empty_json:bool=False,check_company=True):
        #* check if passed empty json
        if not empty_json:
            if not input_fields or not input_fields.keys():
                # if not input_fields.keys():
                    main="passed empty json"
                    second = {"required_fields":required_fields or allowed_fields}
                    error_output = OutputMessages.error_with_message(main_message=main,second_message=second)
                    return error_output
            # else:
            #     main="passed empty json"
            #     second = {"required_fields":required_fields or allowed_fields}
            #     error_output = OutputMessages.error_with_message(main_message=main,second_message=second)
            #     return error_output
            

        if required_fields:
            #* check that all the required fields are filled in
            for valid_field in required_fields:
                if valid_field not in input_fields:
                    main = "passed invalid field"
                    second = {"required_fields":required_fields}
                    output_error = OutputMessages.error_with_message(main_message=main,second_message=second)
                    return output_error
            #* check that all the input keys are same as the required fields
            for input_field in input_fields.keys():
                if input_field not in required_fields:
                    main = "passed invalid field"
                    second = {"required_fields":required_fields}
                    output_error = OutputMessages.error_with_message(main_message=main,second_message=second)
                    return output_error
        


        if allowed_fields:
            for key in input_fields.keys():
                if key not in allowed_fields:
                    main = "passed invalid field"
                    second = {"required_fields":required_fields}
                    output_error = OutputMessages.error_with_message(main_message=main,second_message=second)
                    return output_error

        if user:
            #* check if the user exists as user and have a company
            user_email = user["email"]
            user_exists = User.objects.filter(email=user_email).exists()
            if not user_exists:
                error_output = OutputMessages.user_not_exsts()
                return error_output
            else:
                user_obj = User.objects.get(email=user_email)

            if check_company:
                if not user_obj.companies:
                    main = "this user dont have company"
                    return OutputMessages.error_with_message(main)


            if user_obj.selected_company in user_obj.blocked_by.all():
                user_obj.selected_company = None
                main = "cant select this company because you  blocked"
                err_msg = OutputMessages.error_with_message(main)
                return err_msg

            main = "user exists"
            return OutputMessages.success_and_object(main_message=main,output_object=user_obj)

        main = "passed valid data"
        return OutputMessages.success_with_message(main)

    def passed_valid_fields(self,input_fields,valid_fields):
        #* check if passed empty json    

        if not input_fields.keys():
            main="passed empty json"
            second = {"required_fields":valid_fields}
            error_output = OutputMessages.error_with_message(main_message=main,second_message=second)
            return error_output
        
        for field in input_fields.keys():
            if field not in valid_fields:
                main = "passed invalid field"
                second = {"required_fields":valid_fields}
                output_error = OutputMessages.error_with_message(main_message=main,second_message=second)
                return output_error
        main = "all fields are valid"
        return OutputMessages.success_with_message(main_message=main)
            

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
        
