from rest_framework import serializers
from custom_validation.validation import CustomValidation,OutputMessages
from employer.models import Department
from django.db.models import Q,F
from user.models import User,Company
from employer.models import Employer


class GeneralDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50,default=None)
    rank = serializers.IntegerField(default=None)
    salary = serializers.IntegerField(default=None)

    def check_unique(self,cleaned_data):
        """
        later this method will handle the FK fields 
        that will be needed to update
        """
        return True,cleaned_data

class CreateDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50,default=None)
    rank = serializers.IntegerField(default=None)
    salary = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data,user):

        main = "to perform this you need to use post request"
        second = {"example_json":{
            "name":"name of the department (engineer ...)",
            "rank":"rank of the department",
            "salary":"integer of the salary of the mployer"
        }}

        success_message = OutputMessages.success_with_message(main_message=main,second_message=second)
        return success_message


    def create(self,cleaned_data,user):
        required_fields = ["name","rank","salary"]
        cv = CustomValidation()
        basic_validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(basic_validation):
            return basic_validation


        #* check if the user already have company
        query_fields = {"email":user["email"]}
        company_exists = cv.exists_in_database(query_fields=query_fields,database=User)
        if not all(company_exists):
            main = "you cant create department without creating the company first"
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message
        
        else:
            #*company object
            company_obj = company_exists[1]["object"]


        #* check if the department exists
        department_exists = company_obj.department_set.filter(name=cleaned_data["name"]).exists()
        if department_exists:
            main = "this department is already exists"
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message

        #*creating the new department
        new_department = Department.objects.create(
            name=cleaned_data["name"],
            salary=cleaned_data["salary"],
            rank=cleaned_data["rank"],
            company=company_obj
        )

        new_department.save()
        main = "created successfully"
        second = {"department_json":{
            "name":new_department.name,
            "salary":new_department.salary,
            "rank":new_department.rank,
            "company":new_department.company.name
            }}
    
        success_message = OutputMessages.success_with_message(main_message=main,second_message=second)
        return success_message
    


class DeleteDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50,default=None)
    all_departments = serializers.BooleanField(default=False)


    def get_info(self,cleaned_data,user):
        allowed_fields = ["name","all_departments"]
        cv = CustomValidation()
        basic_validation = cv.passed_valid_fields(input_fields=cleaned_data,valid_fields=allowed_fields)
        if not all(basic_validation):
            return basic_validation
        else:
            user_obj = basic_validation[1]["object"]
        
        
        #* getting the company object of the user
        if not user_obj.company:
            message = {"error":"user doesnt have company"}
            return False,message
        
        company_obj = user_obj.company

        #* checking if passed all_department first
        if "all_departments" in cleaned_data.keys():
            departments = company_obj.department_set.all().values("name")
            main = "all_departments field passed successfully"
            second = {"department_json":departments}
            success_message = OutputMessages.success_with_message(main,second)
            return success_message
        
        #* this section is trying to query the database with the provided fields
        query = Q()

        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                #*checking if something found with this name
                name_exists = company_obj.department_set.filter(name=value).exists()
                if not name_exists:
                    main = "department with this name not found"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    department_query_dict = company_obj.department_set.filter(name=value).values("name")
                    main = "found department with the provided data"
                    second = {"department_json":department_query_dict}
                    success_message = OutputMessages.success_with_message(main,second)
                    return success_message

    

    def delete(self,cleaned_data,user):
        required_fields = ["department_name"]

        cv = CustomValidation()
        basic_validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not basic_validation:
            return basic_validation

        else:
            user_obj = basic_validation[1]["object"]        


        #* checking that the user have company 
        if not user_obj.company:
            main = "this user doesnt have company"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        


        #* checking if department exists 
        company_obj = user_obj.company
        department_exists = company_obj.department_set.filter(name=cleaned_data["name"]).exists()
        if not department_exists:
            main = "this department doesnt exists"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        
        else:
            department_obj = company_obj.department_set.get(name=cleaned_data["name"])
            department_obj.delete()
            main = {"required department is deleted, employers that were in this department set to Null"}
            success_message = OutputMessages.success_with_message(main)
            return success_message
        


class UpdateDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20,default = None)
    update_data = serializers.DictField(default = None)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["name"]
        cv = CustomValidation()
        basic_validation = cv.basic_validation(input_fields=cleaned_data,required_fields=allowed_fields,user=user)
        if not basic_validation:
            return basic_validation
        else:
            user_obj = basic_validation[1]["object"]
        

        #* checking that the user have company 
        if not user_obj.company:
            main = "this user doesnt have company"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        


        company_obj = user_obj.company
        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                name_exists = company_obj.department_set.filter(name=value).exists()
                if not name_exists: 
                    main = {"name not exist. try another field or check if you miss typed"}
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    department_query_dict = company_obj.department_set.filter(name=value).values("name","rank","salary")
                    main = "successfully found data"
                    second = {"department_json":department_query_dict}
                    success_messsage = OutputMessages.success_with_message(main,second)
                    return success_messsage


    def update(self,cleaned_data,user):
        required_fields = ["name","update_data"]
        allowed_update_fields = ["name","rank","salary"]

        cv = CustomValidation()
        basic_validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not basic_validation:
            return basic_validation
        else:
            user_obj = basic_validation[1]["object"]
        
        valid_update_data = cv.passed_valid_fields(input_fields=cleaned_data["update_data"],valid_fields=allowed_update_fields)
        if not valid_update_data:
            main = "passed invalid fields into the update_data json"
            second = {"json_example":{
                    "name":"engineer",
                    "rank":"123",
                    "salary":"2000"
                    }}
            error_message = OutputMessages.error_with_message(main,second)
            return error_message
        
        

        #* checking that the user have company 
        if not user_obj.company:
            main = "this user doesnt have company"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        
        
        # #*checking if the department exists with the id provided
        company_obj = user_obj.company
        department_exists = company_obj.department_set.filter(name = cleaned_data["name"]).exists()
        if not department_exists:
            main = "this department is not exist with this id"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        else:
            department_obj = company_obj.department_set.get(name = cleaned_data["name"])


        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralDepartmentSerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=False):

            update_data = cleaned_data["update_data"]    
            for key,value in update_data.items():
                setattr(department_obj,key,value)

            department_obj.save()
            main = "updated the required fields"
            second = {"updated_data":{
                "name":department_obj.name,
                "rank":department_obj.rank,
                "salary":department_obj.salary
                }}
            success_message = OutputMessages.success_with_message(main,second)
            return success_message
            

        main = "invalid update_data fields"
        error_message = OutputMessages.error_with_message(main)
        return error_message



class GetDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50,default=None)
    all_departments = serializers.BooleanField(default=False)


    def get_info(self,cleaned_data,user):
        required_fields = ["name","all_departments"]

        cv = CustomValidation()
        basic_validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not basic_validation:
            return basic_validation
        else:
            user_obj = basic_validation[1]["object"]
            
        
        #* checking if user have company field
        if not user_obj.company:
            main = "this user doesnt have company field"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        else:
            company_obj = user_obj.company


        #* checking if passed all_department first
        if "all_departments" in cleaned_data.keys():
            department_exists = company_obj.department_set.all().exists()
            if not department_exists:
                main = "no departments exists"
                error_message = OutputMessages.error_with_message(main)
                return error_message
            else:
                departments = company_obj.department_set.all().values("name","rank","salary")
                main = "all_departments field passed successfully"
                second = {"departments":departments}
                success_message = OutputMessages.success_with_message(main,second)
                return success_message
        
        if "name" in cleaned_data.keys():
            for key,value in self.__getattribute__("data").items():
                if key == "name" and value != None:
                    #*checking if something found with this name
                    name_exists = company_obj.department_set.filter(name=value).exists()
                    if not name_exists:
                        main = "department with this name not found"
                        error_message = OutputMessages.error_with_message(main)
                        return error_message
                    else:
                        departments_query_dict = company_obj.department_set.filter(name=value).values("name","rank","salary")
                        main = "successfully found departments"
                        second = {"department_json":departments_query_dict}
                        success_message = OutputMessages.success_with_message(main,second)
                        return success_message
            