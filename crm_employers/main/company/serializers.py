from rest_framework import serializers
from employer.models import Department
from django.db.models import Q,F
from .models import Company


class GeneralCompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50,default=None)
    description = serializers.CharField(max_length=350,default=None)
    address = serializers.CharField(max_length=150,default=None)


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
            message = {"error":"company not found with your email"}
            return False,message


        company_exists = Company.objects.filter(query).exists()
        if company_exists:
            company_data = Company.objects.filter(query).values("name","description","address","admin_email")
            message = {"success":"found company with the provided data","company_json":company_data}
            return True,message
        
        message = {"error":"company not exists with the provided fields"}
        return False,message
    

    def delete(self,cleaned_data,user):
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
            message = {"error":"company not found with your email"}
            return False,message


        company_exists = Company.objects.filter(query).exists()
        if company_exists:
            company_obj = Company.objects.get(query)
            company_obj.delete()
            message = {"success":f"required company is deleted, employers that were in this department set to Null"}
            return True,message
        

        message = {"error":"this company doesnt exists"}
        return False,message



class UpdateCompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50,default=None)
    update_data = serializers.DictField(default=None)

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
            message = {"error":"company not found with your email"}
            return False,message


        company_exists = Company.objects.filter(query).exists()
        if company_exists:
            company_data = Company.objects.filter(query).values("name","description","address","admin_email")
            message = {"success":"found company with the provided data","company_json":company_data}
            return True,message
        
        message = {"error":"company not exists with the provided fields"}
        return False,message
    

    def update(self,cleaned_data,user):
        admin_email = user["email"]

        required_fields = ["name","update_data"]
        allowed_update_fields = ["name","description","address"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass all this fields","example_json":{
                "name":"name of the company as charfield",
                "update_data":{
                    "name":"engineer",
                    "description":"123",
                    "address":"2000"
                    }}}
            
            return False,message
        
        #*checking that the user passed all fields
        for field in required_fields:
            if field not in cleaned_data.keys():
                message = {"error":"you must pass all fields","json_example":{
                "name":"name of the company as charfield",
                "update_data":{
                    "name":"engineer",
                    "description":"123",
                    "address":"2000"
                    },
                    "and you passed":cleaned_data.items()
                    }}
            
                return False,message

        #* checking that the user didnt pass additional fields and only the allowed in the update data
        for field in cleaned_data["update_data"].keys():
            if field not in allowed_update_fields:
                message = {"error":"passed invalid fields into the update_data json","json example of update_data":{
                    "name":"engineer",
                    "description":"123",
                    "address":"sasa at as 1211"
                    }}
                return False,message


        # #*checking if the department exists with the name provided
        company_exists = Company.objects.filter(name=cleaned_data["name"]).exists()
        if not company_exists:
            message = {"error":"this company is not exist with this name"}
            return False,message


        #* checking if this user is admin_email and its hes company
        admin_email_exists = Company.objects.filter(admin_email=admin_email,name=cleaned_data["name"]).exists()
        if not admin_email_exists:
            message = {"error":"this user not a admin or the company not exists"}
            return False,message


        #* checking that the user didnt pass empty update data dict
        if not cleaned_data["update_data"]:
            message = {"error":"you cant pass empty udpate_data ","json_example for updata_data":{
                    "name":"engineer",
                    "description":"123",
                    "address":"2000"
                    }}
            return False,message
        


        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralCompanySerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=True):

            check_unique_fields = update_data_serializer.check_unique(cleaned_data=cleaned_data["update_data"])
            if all(check_unique_fields):
                update_obj = Company.objects.get(name=cleaned_data["name"],admin_email=admin_email)
                update_data = check_unique_fields[1]
                for key,value in update_data.items():
                    setattr(update_obj,key,value)

                update_obj.save()
                message = {"success":"updated the required fields","updated_data":{
                    "name":update_obj.name,
                    "description":update_obj.description,
                    "address":update_obj.address
                }}
                return True,message
            
            return False,check_unique_fields[1]

        message = {"error":"invalid update_data fields"}
        return False,message



class GetCompanySerializer(serializers.ModelSerializer):
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
            message = {"error":"company not found with your email"}
            return False,message


        company_exists = Company.objects.filter(query).exists()
        if company_exists:
            company_data = Company.objects.filter(query).values("name","description","address","admin_email")
            message = {"success":"found company with the provided data","company_json":company_data}
            return True,message
        
        message = {"error":"company not exists with the provided fields"}
        return False,message
    
