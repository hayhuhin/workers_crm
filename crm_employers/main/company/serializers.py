from rest_framework import serializers
from employer.models import Department
from django.db.models import Q,F
from .models import Company
from user.models import User
from custom_validation.validation import CustomValidation,OutputMessages


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
        required_fields = ["name","description","address"]
        admin_email = user["email"]
        custom_validation = CustomValidation()


        #* check if any company is exists with this exact name
        query_fields = {"name":cleaned_data["name"]}
        company_exists = custom_validation.exists_in_database(query_fields,Company)
        if all(company_exists):
            main = {"this company is already exists with this exact name"}
            message = OutputMessages.error_with_message(main_message=main)
            return message
        

        wrong_fields_exists = custom_validation.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(wrong_fields_exists):
            return wrong_fields_exists
        else:
        #* check if the user is already created company
            query_fields = {"admin_email":admin_email}
            database_validation = custom_validation.exists_in_database(query_fields=query_fields,database=Company)
            if all(database_validation):
                return database_validation
            
        
        company_obj = Company.objects.create(
            name=cleaned_data["name"],
            description=cleaned_data["description"],
            address=cleaned_data["address"],
            admin_email=admin_email
        )
        company_obj.save()
        
        
        #* as we creating the company we must add this user to the company in the user model        
        user_obj = User.objects.get(email=admin_email)
        user_obj.company = company_obj
        user_obj.save()

        main = f"company {company_obj.name} created. admin email is {admin_email}"
        message = OutputMessages.success_with_message(main_message=main)
        return message



class DeleteCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name"]

    def get_info(self,cleaned_data,user):
        admin_email = user["email"]
        allowed_fields = ["name"]
        #* this section is trying to query the database with the provided fields


        custom_validation = CustomValidation()

        fields_validated = custom_validation.basic_validation(input_fields=cleaned_data,required_fields=allowed_fields,user=user)
        if not all(fields_validated):
            return fields_validated

        user_obj = fields_validated[1]["object"]

        #* checking that the delete company name is one of this users companies
        company_exists = user_obj.company
        if not company_exists:
            main = "this user doesnt created this companies"
            return OutputMessages.error_with_message(main_message=main)


        #* now checking that this user is the admin of this companies        
        query_fields = {"name":cleaned_data["name"]}
        company_exist = custom_validation.exists_in_database(query_fields=query_fields,database=Company)
        if not all(company_exist):
            return company_exist
        company_obj = company_exist[1]["object"]
        if not company_obj.admin_email == admin_email:
            main = "this user is not the owner of this company"
            return OutputMessages.error_with_message(main_message=main)


        main = {"success":"found company with the provided data"}
        second = {"company_data":{
                    "name":company_obj.name,
                    "description":company_obj.description,
                    "address":company_obj.address,
                    "company_owner":company_obj.admin_email
            }}
        return OutputMessages.success_with_message(main_message=main,second_message=second)
    


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
        # print(cleaned_data)
        admin_email = user["email"]
        allowed_fields = ["name"]

        #* custom validation class
        custom_validation = CustomValidation()
        validated_data = custom_validation.passed_valid_fields(input_fields=cleaned_data,valid_fields=allowed_fields)
        #* checking that passed valid fields

        if not all(validated_data):
            return validated_data

        #* checking if the user have company
        query_fields = {"email":admin_email}
        user_exists = custom_validation.exists_in_database(query_fields=query_fields,database=User)
        if not all(user_exists):
            return user_exists
        
        user_obj = user_exists[1]["object"]


        required_company = Company.objects.filter(admin_email=user_obj.email,name=cleaned_data["name"]).exists()
        if not required_company:
            main = "this user doesnt have company or the company is invalid"
            return OutputMessages.error_with_message(main_message=main)

        company_obj = Company.objects.get(admin_email=user_obj.email,name=cleaned_data["name"])
        main = "found company with the provided data",
        second = {"company_json":{
            "name":company_obj.name,
            "description":company_obj.description,
            "address":company_obj.address,
            "admin_email":company_obj.admin_email
        }}
        return OutputMessages.success_with_message(main_message=main,second_message=second)
        

    def update(self,cleaned_data,user):
        admin_email = user["email"]

        required_fields = ["name","update_data"]
        allowed_update_fields = ["name","description","address"]

        custom_validation = CustomValidation()

        basic_validation = custom_validation.basic_validation(input_fields=cleaned_data,user=user,required_fields=required_fields)

        if not all(basic_validation):
            return basic_validation


        #* checking that the user didnt pass additional fields and only the allowed in the update data
        update_data_validation = custom_validation.passed_valid_fields(input_fields=cleaned_data["update_data"],valid_fields=allowed_update_fields)
        if not all(update_data_validation):
            return update_data_validation

        # #*checking if the company exists with the name provided
        query_fields = {"name":cleaned_data["name"]}
        company_exists = custom_validation.exists_in_database(query_fields=query_fields,database=Company)
        if not all(company_exists):
            main = {"error":"this user not a admin or the company not exists"}
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message
        else:
            company_obj = company_exists[1]["object"]


        #* checking if this user is admin_email and its hes company
        if not company_obj.admin_email == admin_email:
            main = {"error":"this user not a admin or the company not exists"}
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message



        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralCompanySerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=False):

            check_unique_fields = update_data_serializer.check_unique(cleaned_data=cleaned_data["update_data"])
            if all(check_unique_fields):
                update_data = check_unique_fields[1]
                for key,value in update_data.items():
                    setattr(company_obj,key,value)

                company_obj.save()
                message = "updated the required fields"
                second = {"updated_data":{
                    "name":company_obj.name,
                    "description":company_obj.description,
                    "address":company_obj.address
                }}
                success_message = OutputMessages.success_with_message(main_message=message,second_message=second)
                return success_message
            
            error_message = OutputMessages.error_with_message(main_message=check_unique_fields[1])
            return error_message

        main = {"error":"invalid update_data fields"}
        error_message = OutputMessages.error_with_message(main_message=main)
        return error_message



class GetCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name"]

    def get_info(self,cleaned_data,user):
        admin_email = user["email"]
        required_fields = ["name"]

        custom_validation = CustomValidation()
        basic_validation = custom_validation.basic_validation(input_fields=cleaned_data,user=user,required_fields=required_fields)
        if not all(basic_validation):
            return basic_validation

        #*checking if the company exists with the name provided
        query_fields = {"name":cleaned_data["name"]}
        company_exists = custom_validation.exists_in_database(query_fields=query_fields,database=Company)
        if not all(company_exists):
            main = {"error":"this user is not an admin or the company not exists"}
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message
        else:
            company_obj = company_exists[1]["object"]


        #* checking if this user is admin_email and its hes company
        if not company_obj.admin_email == admin_email:
            main = {"error":"this is user not an admin or the company not exists"}
            error_message = OutputMessages.error_with_message(main_message=main)
            return error_message


        company_json = {
            "name":company_obj.name,
            "description":company_obj.description,
            "address":company_obj.address,
            "admin_email":company_obj.admin_email
        }
        main = {"success":"found company with the provided data"}
        success_message = OutputMessages.success_with_message(main_message=main,second_message={"company_json":company_json})
        return success_message
            
