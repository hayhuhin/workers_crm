from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from .models import Employer,Department
from company.models import Company
from user.models import User
from django.db.models import Q,F
from custom_validation.validation import CustomValidation,OutputMessages


#* each class with the name employer in it is a high previlage serializers that done by the admin,hr,managers employers
#! must re create this whole seralizers
#* general serializers


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email","username","password"]



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
    phone = serializers.CharField(max_length=50,default=None)
    department = serializers.CharField(default=None)
    # lead = serializers.IntegerField(default=None)
    # task = serializers.IntegerField(default=None)
    #! need to uncomment it after fixing the dashboard application
    # graph_permission = models.ManyToManyField(GraphPermission,default=None)
    # insights_permission = models.ManyToManyField(GraphInsights,default=None)

    def check_unique(self,cleaned_data,user_object):
        """
        this method will check if there is already existing data with the same id.

        unique fields are customer_id,email
        """
        #* this class will handle the validation 
        cv = CustomValidation()


        for key in cleaned_data.keys():
            #* checking if the employer already exists under the required user 
            if key == "user":
                # check if this user is exists and if he already have employer 

                targeted_user = user_object.company.user_set.filter(email=cleaned_data["user"]).exists()
                if not targeted_user:
                    main = "this user not exists"
                    error_message = OutputMessages.error_with_message(main_message=main)
                    return error_message
                else:
                    targeted_user = user_object.company.user_set.get(email=cleaned_data["user"])



                #check if this user already have employer
                targeted_user_is_employer = user_object.company.employer_set.filter(email=targeted_user.email).exists()
                if targeted_user_is_employer :
                    main = "cant change this employer to the required user because this user is already exists as employer"
                    error_message = OutputMessages.error_with_message(main_message=main)
                    return error_message

                else:
                    cleaned_data["user"] = targeted_user


            if key == "department":
                department_exists = user_object.company.department_set.filter(name=cleaned_data["department"]).exists()
                if department_exists:
                    #* this removes the assigned to email and changes it to the assigned to object
                    department_obj = user_object.company.department_set.get(name=cleaned_data["department"])
                    cleaned_data["department"] = department_obj
                else:
                    main = "this department not exists with the provided details"
                    error_message = OutputMessages.error_with_message(main_message=main)
                    return error_message


        #* adding user object into the cleaned_data if the user not going to be modified
        if "user" not in cleaned_data.keys():
            cleaned_data["user"] = user_object
        
        
        #* updating automaticly the employer email to the user's email
        cleaned_data["email"] = cleaned_data["user"].email
                



        #* returning cleaned data with the objects inside that can be used to update the database
        return True,cleaned_data




#* employer serializers

class CreateEmployerSerializer(serializers.Serializer):
    """
    creating the Employer
    """
    first_name = serializers.CharField(default=None,max_length=50)
    last_name = serializers.CharField(default=None,max_length=50)
    email = serializers.EmailField(default=None)
    phone = serializers.CharField(default=None,max_length=50)
    department = serializers.CharField(default=None,max_length=50)



    def create(self,cleaned_data,user):
        """
        creating the employer object if the email is already exists in the User model.
        the User model can be modified or created only by IT or System Admin
        """

        required_fields = ["first_name","last_name","email","phone","department"]

        custom_validation = CustomValidation()
        basic_validation = custom_validation.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(basic_validation):
            return basic_validation



        #*checking if the employer is already exists
        query_field = {"email":cleaned_data["email"]}
        employer_exists = custom_validation.exists_in_database(query_fields=query_field,database=Employer)
        if all(employer_exists):
            main_message = "this employer is already exists"
            error_message = OutputMessages.error_with_message(main_message=main_message)
            return error_message

        
        #* checking if the user  exists with this email
        query_field = {"email":cleaned_data["email"]}
        user_exists = custom_validation.exists_in_database(query_fields=query_field,database=User)
        if not all(user_exists):
            return user_exists
        else:
            user_obj = user_exists[1]["object"]

        #* this is adding new key value of the user for later usage
        cleaned_data["user"] = user_obj
        

        #*checking if the user is already in a company
        if not user_obj.company:
            main_message = "this user doesnt have company"
            error_message = OutputMessages.error_with_message(main_message=main_message)
            return error_message
        else:
            company_obj = user_obj.company
            cleaned_data["company"] = company_obj

        #* if no department exists returns error message
        if not company_obj.department_set.filter(name=cleaned_data["department"]).exists():
            main_message = "this department not exists"
            error_message = OutputMessages.error_with_message(main_message=main_message)
            return error_message
        
        else:
            department_obj = company_obj.department_set.get(name=cleaned_data["department"])
            cleaned_data["department"]=department_obj


        #* here im adding all fields of the employer from user data into our employer model and saving it
        employer_obj = Employer()
        for key,value in cleaned_data.items():
            setattr(employer_obj,key,value)

        employer_obj.save()
        main_message = "employer created successfully"
        second_message = {"employer_data":{
            "first_name":employer_obj.first_name,
            "last_name":employer_obj.last_name,
            "email":employer_obj.email,
            "created_at":employer_obj.created_at,
        }}
        success_message = OutputMessages.success_with_message(main_message=main_message,second_message=second_message)
        return success_message
    

class GetEmployerSerializer(serializers.Serializer):
    """
    getting the employer data.
    if specific so by the provided email
    or if all it will return all employers
    """

    all_employers = serializers.BooleanField(default=False)
    email = serializers.EmailField(default=None)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["all_employers","email"]
        custom_validation = CustomValidation()
        valid_fields = custom_validation.passed_valid_fields(input_fields=cleaned_data,valid_fields=allowed_fields)
        if not all(valid_fields):
            return valid_fields
        
        #* getting the user's company first
        query_fields = {"email":user["email"]}
        user_exists = custom_validation.exists_in_database(query_fields=query_fields,database=User)
        if not all(user_exists):
            return user_exists
        else:
            creater_user_obj = user_exists[1]["object"]

        #* checking that the user that creating the employer have company 
        if not creater_user_obj.company:
            main_message = "first you need to be a part of a company"
            error_message = OutputMessages.error_with_message(main_message = main_message)
            return error_message

        else:
            company_obj = creater_user_obj.company

        #* first option
        if "all_employers" in cleaned_data.keys():
            main_message = "successfully found employers"

            second_message = {"employer_json":company_obj.employer_set.all().values("first_name","email")}
            success_message = OutputMessages.success_with_message(main_message=main_message,second_message=second_message)
            return success_message
        
        #* second option
        if "email" in cleaned_data.keys():
            #* trying to find this employer
            employer_exists = company_obj.employer_set.filter(email=cleaned_data["email"]).exists()
            if not employer_exists:
                main_message = f"employer not exists with the email:{cleaned_data['email']}"
                error_message = OutputMessages.error_with_message(main_message=main_message)
                return error_message
            else:
                employer_obj = company_obj.employer_set.all().get(email=cleaned_data["email"])
                employer_json = {
                    "first_name":employer_obj.first_name,
                    "email":employer_obj.email,
                    "phone":employer_obj.phone,
                    "company":employer_obj.company.name ,
                    }
                main_message = "employer found successfully"
                sc_msg = {"employer_json":employer_json}
                success_message = OutputMessages.success_with_message(main_message=main_message,second_message=sc_msg)
                return success_message
            


class DeleteEmployerSerializer(serializers.Serializer):
    email = serializers.EmailField(default=None)
    

    def get_info(self,cleaned_data,user):
        required_fields = ["email"]

        cv = CustomValidation()
        basic_validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(basic_validation):
            return basic_validation
        else:
            user_obj = basic_validation[1]["object"]        
            
        #* checking if employer exists the provided email
        company_obj = user_obj.company

        employer_exists = company_obj.employer_set.filter(email=cleaned_data["email"]).exists()
        if not employer_exists:
            main = "employer not exists"
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message
        else:
            employer_dict = company_obj.employer_set.filter(email=cleaned_data["email"]).values("first_name","last_name","email","phone","company__name","department__name")
            main = "successfully employer found"
            second = {"employer_json":employer_dict}
            success_message = OutputMessages.success_with_message(main_message=main,second_message=second)
            return success_message




    def delete(self,cleaned_data,user):
        required_fields = ["email"]


        cv = CustomValidation()
        basic_validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(basic_validation):
            return basic_validation
        else:
            user_obj = basic_validation[1]["object"]        
            
        #* checking if employer exists the provided email
        company_obj = user_obj.company

        employer_exists = company_obj.employer_set.filter(email=cleaned_data["email"]).exists()
        if not employer_exists:
            main = "employer not exists"
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message
        else:
            employer_obj = company_obj.employer_set.get(email=cleaned_data["email"])
            employer_obj.delete()
            main = f"successfully deleted employer {cleaned_data['email']}"
            success_message = OutputMessages.success_with_message(main_message=main)
            return success_message


    
class UpdateEmployerSerializer(serializers.Serializer):
    email = serializers.EmailField(default=None)
    update_data = serializers.DictField(default=None)

    def get_info(self,cleaned_data,user):
        required_fields = ["email"]

        cv = CustomValidation()
        basic_validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(basic_validation):
            return basic_validation
        else:
            user_obj = basic_validation[1]["object"]        
            
        #* checking if employer exists the provided email
        company_obj = user_obj.company

        employer_exists = company_obj.employer_set.filter(email=cleaned_data["email"]).exists()
        if not employer_exists:
            main = "employer not exists"
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message
        else:
            employer_dict = company_obj.employer_set.filter(email=cleaned_data["email"]).values("first_name","last_name","email","phone","company__name","department__name")
            main = "successfully employer found"
            second = {"employer_json":employer_dict}
            success_message = OutputMessages.success_with_message(main_message=main,second_message=second)
            return success_message



    def update(self,cleaned_data,user):
        required_fields = ["email","update_data"]
        allowed_update_fields = ["user","first_name","last_name","phone","department"]


        cv = CustomValidation()
        basic_validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(basic_validation):
            return basic_validation
        else:
            creator_user = basic_validation[1]["object"]
            company_obj = creator_user.company

        
        valid_fields = cv.passed_valid_fields(input_fields=cleaned_data["update_data"],valid_fields=allowed_update_fields)
        if not all(valid_fields):
            main = "passed invalid field in the update_data"
            second = {"json_example":{
                    "user":"user email",
                    "first_name":"john",
                    "last_name":"doe",
                    "phone":"phone number",
                    "department":"engineer department"
                    }}
            error_message = OutputMessages.error_with_message(main_message=main,second_message=second)
            return error_message
        

        # #*checking if the user exists with the email provided
        user_exists = company_obj.user_set.filter(email=cleaned_data["email"]).exists()
        if not user_exists:
            main = "user not exists"
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message
        else:
            user_obj = company_obj.user_set.get(email=cleaned_data["email"])



        #* cheking if the user exists as employer 
        if not user_obj.employer:
            main = "cant update this user if the user not exists as employer"
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message        


        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralEmployerSerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=False):
            check_unique_fields = update_data_serializer.check_unique(cleaned_data=cleaned_data["update_data"],user_object=user_obj)
            if all(check_unique_fields):
                employer_obj = user_obj.employer
                update_data = check_unique_fields[1]

                for key,value in update_data.items():
                    setattr(employer_obj,key,value)

                employer_obj.save()
                main = "updated the required fields"
                second = {"employer_json":{
                    "first_name":employer_obj.first_name,
                    "last_name":employer_obj.last_name,
                    "email":employer_obj.email,
                    "phone":employer_obj.phone,
                    "email":employer_obj.email,
                    "department":employer_obj.department.name
                }}
                success_message = OutputMessages.success_with_message(main_message=main,second_message=second)
                return success_message
            
            
            error_message = OutputMessages.error_with_message(main_message=check_unique_fields[1]["error"])
            return error_message

        main = "invalid update_data fields"
        error_message = OutputMessages.error_with_message(main_message=main)
        return error_message
