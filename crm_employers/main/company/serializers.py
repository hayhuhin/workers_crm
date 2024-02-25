from rest_framework import serializers
from employer.models import Department
from django.db.models import Q,F
from .models import Company


class GeneralCompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50,default=None)
    rank = serializers.IntegerField(default=None)
    salary = serializers.IntegerField(default=None)

    def check_unique(self,cleaned_data):
        """
        later this method will handle the FK fields 
        that will be needed to update
        """
        return True,cleaned_data

class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name","description","address"]

    def get_info(self,cleaned_data):
        message = {"success":{"example json":self.fields.keys()}}
        return True,message


    def create(self,cleaned_data,user):
        admin_email = user["email"]

        # #* check if passed empty json
        # if not cleaned_data.keys():
        #     message = {"error":"passed empty json","json_example":{
        #         "name":"department name",
        #         "rank":"department rank",
        #         "salary":"department salary"
        #     }}
        #     return False,message
        
        # #* check if passed invalid fields
        # for key in cleaned_data.keys():
        #     if key not in required_fields:
        #         message = {"error":"passed invalid fields","allowed_fields":required_fields}
        #         return False,message
            

        #* check if the company exists
        company_exists = Company.objects.filter(name=cleaned_data["name"]).exists()
        if company_exists:
            message = {"error":"this department is already exists"}
            return False,message
        

        #* check if the user is already created company
        user_already_created = Company.objects.filter(admin_email=admin_email).exists()
        if user_already_created:
            message = {"error":"this user is already created a company"}
            return False,message

        obj_instance = Company.objects.create(
            name=cleaned_data["name"],
            description=cleaned_data["description"],
            address=cleaned_data["address"],
            admin_email=admin_email
        )
        obj_instance.save()
        message = {"success":f"company {obj_instance.name} created. admin email is {admin_email}"}
        return True,message


class DeleteCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name"]

    def get_info(self,cleaned_data,user):
        admin_email = user["email"]

        #* this section is trying to query the database with the provided fields
        query = Q()

        for key,value in cleaned_data.items():
            if key == "name" and value != None:
                #*checking if something found with this name
                name_exists = Company.objects.filter(name=value).exists()
                if name_exists:
                    query &= Q(name=value)

                else:
                    message = {"error":"company with this name not found"}
                    return False,message
            

        #* checking if company exists with the provided admin email
        admin_email_exists = Company.objects.filter(admin_email=admin_email).exists()
        if admin_email_exists:
            query &= Q(admin_email=admin_email)
        else:
            message = {"error":"company not found with you email"}
            return False,message


        company_exists = Department.objects.filter(query).exists()
        if company_exists:
            company_data = Company.objects.filter(query).values("name","description")
            message = {"success":"found company with the provided data","company_json":company_data}
            return True,message
        
        message = {"error","company not exists with the provided fields"}
        return False,message
    

    def delete(self,cleaned_data):
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


        #check if the department exists
        department_exists = Department.objects.filter(id=cleaned_data["department_id"]).exists()
        if department_exists:
            department_obj = Department.objects.get(id=cleaned_data["department_id"])
            department_obj.delete()

            message = {"success":f"required department is deleted, employers that were in this department set to Null"}
            return True,message
        

        message = {"error":"this department doesnt exists"}
        return False,message



class UpdateCompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20,default = None)
    department_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default = None)

    def get_info(self,cleaned_data):
        allowed_fields = ["name","department_id"]

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

        #this will have my query that will be passed later
        query = Q()

        #* this whole section is checking if the passed data is valid and returning error message or proccedes to the next stage
        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                name_exists = Department.objects.filter(name=value).exists()
                if name_exists: 
                    query &= Q(name=value)
                else:
                    message = {"error":"name not exist. try another field or check if you miss typed"}
                    return False,message
                
            if key == "department_id" and value != None:
                department_exists = Department.objects.filter(id=value).exists()
                if department_exists:
                    query &= Q(id=value)
                else:
                    message = {"error":"department with this id not exist. try another field or check if you miss typed"}
                    return False,message


        query_data = Department.objects.filter(query).values("id","name")
        message = {"success":query_data}
        return True,message


    def update(self,cleaned_data):
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


        # #*checking if the department exists with the id provided
        department_exists = Department.objects.filter(id = cleaned_data["department_id"]).exists()
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
        update_data_serializer = GeneralCompanySerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=True):

            check_unique_fields = update_data_serializer.check_unique(cleaned_data=cleaned_data["update_data"])
            if all(check_unique_fields):
                update_obj = Department.objects.get(id=cleaned_data["department_id"])
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



class GetCompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50,default=None)
    department_id = serializers.IntegerField(default=None)
    all_departments = serializers.BooleanField(default=False)


    def get(self,cleaned_data):
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


        #* checking if passed all_department first
        if "all_departments" in cleaned_data.keys():
            departments = Department.objects.all().values("id","name")
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
