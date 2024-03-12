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
        
        
        #* getting the company object of the user
        user_obj = User.objects.get(email=user_email)

        if not user_obj.company:
            message = {"error":"user doesnt have company"}
            return False,message
        
        company_obj = user_obj.company

        #* checking if passed all_department first
        if "all_departments" in cleaned_data.keys():
            departments = company_obj.department_set.all().values("id","name")
            message = {"success":"all_departments field passed successfully","all_departments":departments}
            return True,message
        
        #* this section is trying to query the database with the provided fields
        query = Q()

        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                #*checking if something found with this name
                name_exists = Department.objects.filter(name=value).exists()
                if name_exists:
                    query &= Q(name=value)

                else:
                    message = {"error":"department with this name not found"}
                    return False,message
            if key == "department_id" and value != None:
                #* checking if department exists with the provided id
                department_exists = Department.objects.filter(id=value).exists()
                if department_exists:
                    query &= Q(id=value)
                else:
                    message = {"error":"department not found with this id"}
                    return False,message
            
        department_exists = Department.objects.filter(query).exists()
        if department_exists:
            department_data = Department.objects.filter(query).values("name","id")
            message = {"success":"found department with the provided data","department_json":department_data}
            return True,message
        message = {"error","department not exists with the provided fields"}
        return False,message
    

    def delete(self,cleaned_data,user):
        user_email = user["email"]
        required_fields = ["department_id"]

        for fields in cleaned_data.keys():
            if fields not in required_fields:
                message = {"error":"passed invalid fields","required_fields":required_fields}
                return False,message
            
        #* checking if the user passed empty json
        if not cleaned_data.items():
            message = {"error":"you passed empty json","example_json":{
            "department_id":"2",
            }}
            return False,message
        
        #* first im checking if the user exists
        user_exists = User.objects.filter(email=user_email).exists()
        if not user_exists:
            message = {"error":"user not exists"}
            return False,message
        else:
            user_obj = User.objects.get(email=user_email)
        
        #* checking that the user have company 
        if not user_obj.company:
            message = {"error":"this user doesnt have company"}
            return False,message
        


        #* checking if department exists 
        company_obj = user_obj.company
        department_exists = company_obj.department_set.filter(id=cleaned_data["department_id"]).exists()
        if department_exists:
            department_obj = Department.objects.get(id=cleaned_data["department_id"])
            department_obj.delete()

            message = {"success":f"required department is deleted, employers that were in this department set to Null"}
            return True,message
        

        message = {"error":"this department doesnt exists"}
        return False,message



class UpdateDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20,default = None)
    department_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default = None)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["name","department_id"]
        user_email = user["email"]
        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass at least one of the fields","example_json":{
                "name":"engineer",
                "department_id":"12"
            }}
            return False,message
        
        #*checking for allowed fields
        for key in cleaned_data.keys():
            if key not in allowed_fields:
                message = {"error":f"passed invalid field -{key}-"}
                return False,message
            

        #* first im checking if the user exists
        user_exists = User.objects.filter(email=user_email).exists()
        if not user_exists:
            message = {"error":"user not exists"}
            return False,message
        else:
            user_obj = User.objects.get(email=user_email)
        

        #* checking that the user have company 
        if not user_obj.company:
            message = {"error":"this user doesnt have company"}
            return False,message
        

        #this will have my query that will be passed later
        query = Q()

        #* this whole section is checking if the passed data is valid and returning error message or proccedes to the next stage
        company_obj = user_obj.company
        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                name_exists = company_obj.department_set.filter(name=value).exists()
                if name_exists: 
                    query &= Q(name=value)
                else:
                    message = {"error":"name not exist. try another field or check if you miss typed"}
                    return False,message
                
            if key == "department_id" and value != None:
                department_exists = company_obj.department_set.filter(id=value).exists()
                if department_exists:
                    query &= Q(id=value)
                else:
                    message = {"error":"department with this id not exist. try another field or check if you miss typed"}
                    return False,message


        query_data = company_obj.department_set.filter(query).values("id","name")
        message = {"success":query_data}
        return True,message


    def update(self,cleaned_data,user):
        user_email = user["email"]
        required_fields = ["department_id","update_data"]
        allowed_update_fields = ["name","rank","salary"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass all this fields","example_json":{
                "department_id":"id of the department as integer",
                "update_data":{
                    "name":"engineer",
                    "rank":"123",
                    "salary":"2000"
                    }}}
            
            return False,message
        
        #*checking that the user passed all fields
        for field in required_fields:
            if field not in cleaned_data.keys():
                message = {"error":"you must pass all fields","json_example":{
                "department_id":"id of the department as integer",
                "update_data":{
                    "name":"engineer",
                    "rank":"123",
                    "salary":"2000"
                    },
                    "and you passed":cleaned_data.items()
                    }}
            
                return False,message

        #* checking that the user didnt pass additional fields and only the allowed in the update data
        for field in cleaned_data["update_data"].keys():
            if field not in allowed_update_fields:
                message = {"error":"passed invalid fields into the update_data json","json example of update_data":{
                    "name":"engineer",
                    "rank":"123",
                    "salary":"2000"
                    }}
                return False,message


        #* first im checking if the user exists
        user_exists = User.objects.filter(email=user_email).exists()
        if not user_exists:
            message = {"error":"user not exists"}
            return False,message
        else:
            user_obj = User.objects.get(email=user_email)
        

        #* checking that the user have company 
        if not user_obj.company:
            message = {"error":"this user doesnt have company"}
            return False,message
        
        
        # #*checking if the department exists with the id provided
        company_obj = user_obj.company
        department_exists = company_obj.department_set.filter(id = cleaned_data["department_id"]).exists()
        if not department_exists:
            message = {"error":"this department is not exist with this id"}
            return False,message



        #* checking that the user didnt pass empty update data dict
        if not cleaned_data["update_data"]:
            message = {"error":"you cant pass empty udpate_data ","json_example for updata_data":{
                    "name":"engineer",
                    "rank":"123",
                    "salary":"2000"
                    }}
            return False,message
        


        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralDepartmentSerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=True):

            check_unique_fields = update_data_serializer.check_unique(cleaned_data=cleaned_data["update_data"])
            if all(check_unique_fields):
                update_obj = company_obj.department_set.get(id=cleaned_data["department_id"])
                update_data = check_unique_fields[1]
                
                for key,value in update_data.items():
                    setattr(update_obj,key,value)

                update_obj.save()
                message = {"success":"updated the required fields","updated_data":{
                    "name":update_obj.name,
                    "rank":update_obj.rank,
                    "salary":update_obj.salary
                }}
                return True,message
            
            return False,check_unique_fields[1]

        message = {"error":"invalid update_data fields"}
        return False,message



class GetDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50,default=None)
    department_id = serializers.IntegerField(default=None)
    all_departments = serializers.BooleanField(default=False)


    def get_info(self,cleaned_data,user):
        user_email = user["email"]
        required_fields = ["name","department_id","all_departments"]
        for fields in cleaned_data.keys():
            if fields not in required_fields:
                message = {"error":"passed invalid fields","required_fields":required_fields}
                return False,message
            
        #* checking if the user passed empty json
        if not cleaned_data.items():
            message = {"error":"you passed empty json","example_json":{
            "name":"engineer",
            "department_id":"2",
            "all_departments":"boolean field"
            }}
            return False,message

        #* checking if company exists in user model
        user_exists = User.objects.filter(email=user_email)
        if not user_exists:
            message = {"error":"the user not exists"}
            return False,message
        else:
            user_obj = User.objects.get(email=user_email)

        
        #* checking if user have company field
        if not user_obj.company:
            message = {"error":"this user doesnt have company field"}
            return False,message

        #* getting company object
        company_id = user_obj.company.id
        company_obj = Company.objects.get(id=company_id)


        #* checking if passed all_department first
        if "all_departments" in cleaned_data.keys():
            departments = company_obj.department_set.all()
            # departments = Department.objects.get(company=company)
            message = {"success":"all_departments field passed successfully","departments":departments.values("id","name","rank","salary")}
            return True,message
        
        #* this section is trying to query the database with the provided fields
        query = Q()

        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                #*checking if something found with this name
                name_exists = company_obj.department_set.filter(name=value).exists()
                if name_exists:
                    query &= Q(name=value)

                else:
                    message = {"error":"department with this name not found"}
                    return False,message
            if key == "department_id" and value != None:
                #* checking if department exists with the provided id
                department_exists = company_obj.department_set.filter(id=value).exists()
                if department_exists:
                    query &= Q(id=value)
                else:
                    message = {"error":"department not found with this id"}
                    return False,message
            
        department_exists = company_obj.department_set.filter(query).exists()
        if department_exists:
            department_data = company_obj.department_set.filter(query).values("name","id")
            message = {"success":"found department with the provided data","department_json":department_data}
            return True,message
        message = {"error","department not exists with the provided fields"}
        return False,message
