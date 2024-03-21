from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from finance.models import Income,Outcome,Customer
from user.models import User
from django.db.models import Q,F
from custom_validation.validation import CustomValidation,OutputMessages


#* customer table fields
    # name = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    # address = models.TextField(blank=True, null=True)
    # notes = models.TextField(blank=True, null=True)
    # customer_id = models.IntegerField()




# class UpdateSerializer(object):
#     main_fields = serializers.DictField()
#     nested_fields = serializers.DictField()


#     def get_info(self,required_main_fields,required_nested_fields,cleaned_data):
#         #* check the main fields first
#         for field in cleaned_data:
#             if field not in required_main_fields:
#                 message = {"error":"invalid field passed"}
#                 return False,message
            
#         #* checking the nested dicts
#         for 







class GeneralCustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(max_length=15,default=None)
    address = serializers.CharField(max_length=350,default=None)
    notes = serializers.CharField(max_length=350,default=None)
    customer_id = serializers.IntegerField(default=None)

    def check_unique(self,cleaned_data,company_object):

        for key in cleaned_data.keys():
            #* checking if the email exists
            if key == "email":
                email_exists = company_object.customer_set.filter(email=cleaned_data["email"]).exists()
                if email_exists:
                    main = "this email is already exist and cant be used in a different customer"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg
                
            if key == "customer_id":
                customer_id_exists = company_object.customer_set.filter(customer_id=cleaned_data["customer_id"]).exists()
                if customer_id_exists:
                    main = "this customer id is already exist and cant be used in a different customer"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg


        return True,cleaned_data





class CreateCustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(max_length=15,default=None)
    address = serializers.CharField(max_length=350,default=None)
    notes = serializers.CharField(max_length=350,default=None)
    customer_id = serializers.IntegerField(default=None)
    
    def get_info(self,cleaned_data,user):
        required_fields = ["name","email","phone_number","address","notes","customer_id"]

        cv = CustomValidation()
        user_valid = cv.basic_validation(user=user,empty_json=True)
        if not all(user_valid):
            return user_valid
        else:
            user_obj = user_valid[1]["object"]
            company_obj = user_obj.company

        main = "to create you need to pass the fields as post method"
        second = {"json_example":{
            "name":"name of the customer company",
            "email":"email of the customer contact person",
            "phone_number":"phone number of the client",
            "address":"physical address of the client",
            "notes":"notes can be up to 350 characters",
            "customer_id":"customer's id that must be unique"
        }}
        success_msg = OutputMessages.success_with_message(main,second)
        return success_msg


    def create(self,cleaned_data,user):
        required_fields = ["name","email","phone_number","address","notes","customer_id"]

        cv = CustomValidation()
        validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(validation):
            return validation
        
        else:
            user_obj = validation[1]["object"]
            company_obj = user_obj.company


        #*checking if the customer is already exists 
        customer_exists = company_obj.customer_set.filter(customer_id=cleaned_data["customer_id"]).exists()
        if customer_exists:
            main = "cant create new customer because this customer is already exists with this data"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg


        #*checking that the email of the customer is not already existing
        customer_email_exists = company_obj.customer_set.filter(email=cleaned_data["email"]).exists()
        if customer_email_exists:
            main = "this email is already registered and you cant create this customer with this email"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg


        customer_obj = Customer.objects.create(
            name=cleaned_data["name"],
            email=cleaned_data["email"],
            phone_number=cleaned_data["phone_number"],
            address=cleaned_data["address"],
            notes=cleaned_data["notes"],
            customer_id=cleaned_data["customer_id"],
            company=company_obj
        )

        customer_obj.save()
        
        main = "created new customer successfully"
        second = {"customer_json":{
            "name":cleaned_data["name"],
            "email":cleaned_data["email"],
            "phone_number":cleaned_data["phone_number"],
            "address":cleaned_data["address"],
            "notes":cleaned_data["notes"],
            "customer_id":cleaned_data["customer_id"],
            "company":company_obj.name
        }}
        success_msg = OutputMessages.success_with_message(main,second)
        return success_msg


class DeleteCustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(default=None)
    address = serializers.CharField(default=None)
    customer_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data,user):

        allowed_fields = ["name","email","phone_number","address","customer_id"]

        
        cv = CustomValidation()
        validation = cv.basic_validation(user=user,empty_json=True)
        if not all(validation):
            print("its here")
            return validation

        else:
            user_obj = validation[1]["object"]
            company_obj = user_obj.company
        
        field_validation = cv.passed_valid_fields(input_fields=cleaned_data,valid_fields=allowed_fields)
        if not all(field_validation):
            return field_validation
        
        #this will have my query that will be passed later
        query = Q()
        #* this whole section is checking if the passed data is valid and returning error message or proccedes to the next stage
        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                name_exists = company_obj.customer_set.filter(name=value).exists()
                if name_exists: 
                    query &= Q(name=value)
                else:
                    main = "name not exist. try another field or check if you miss typed"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg
            
            if key == "email" and value != None:
                email_exists = company_obj.customer_set.filter(email=value).exists()
                if email_exists:
                    query &= Q(email=value)
                else:
                    main = "email not exist. try another field or check if you miss typed"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg

            if key == "customer_id" and value != None:
                customer_id_exists = company_obj.customer_set.filter(customer_id=value).exists()
                if customer_id_exists:
                    query &= Q(customer_id=value)
                else:
                    main = "customer_id not exist. try another field or check if you miss typed"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg
        
        customer_exists = company_obj.customer_set.filter(query).exists()
        if not customer_exists:
            main = "no customer found"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg
        else:
            customer_query_dict = company_obj.customer_set.filter(query).values("name","email","phone_number","address","notes","customer_id")
            main = "successfully found the data"
            second = {"customer_json":customer_query_dict}
            success_msg = OutputMessages.success_with_message(main,second)
            return success_msg


    def delete(self,cleaned_data,user):
        required_fields = ["email","customer_id"]

        cv = CustomValidation()
        validation = cv.basic_validation(user=user,input_fields=cleaned_data,required_fields=required_fields)
        if not all(validation):
            return validation
        else:
            user_obj = validation[1]["object"]
            company_obj = user_obj.company

        
        #*checking if the customer is already exists
        customer_id_exists = company_obj.customer_set.filter(customer_id = cleaned_data["customer_id"]).exists()
        if not customer_id_exists:
            main = "cant delete this customer because the customer not exist with this id"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg

        
        #*checking that the email of the customer is not already existing
        customer_email_exist = company_obj.customer_set.filter(email=cleaned_data["email"]).exists()
        if not customer_email_exist:
            main = "cant delete this customer because the customer not exists with this email"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg


        #*querying with the provided information to search for the customer and delete 

        customer_exists = company_obj.customer_set.filter(email=cleaned_data["email"],customer_id=cleaned_data["customer_id"]).exists()
        if not customer_exists:
            main = "this customer not exists with the data provided"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg
        
        else:
            customer_obj = company_obj.customer_set.get(email=cleaned_data["email"],customer_id=cleaned_data["customer_id"])
            customer_obj.delete()
            main = "deleted the customer successfully"
            second = {"customer_json":{
                "name":customer_obj.name,
                "email":customer_obj.email,
                "phone_number":customer_obj.phone_number,
                "address":customer_obj.address,
                "customer_id":customer_obj.customer_id
            }}
            success_msg = OutputMessages.success_with_message(main,second)
            return success_msg



class UpdateCustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    customer_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default=None)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["name","email","phone_number","address","customer_id"]

        
        cv = CustomValidation()
        validation = cv.basic_validation(user=user,empty_json=True)
        if not all(validation):
            print("its here")
            return validation

        else:
            user_obj = validation[1]["object"]
            company_obj = user_obj.company
        
        field_validation = cv.passed_valid_fields(input_fields=cleaned_data,valid_fields=allowed_fields)
        if not all(field_validation):
            return field_validation
        
        #this will have my query that will be passed later
        query = Q()
        #* this whole section is checking if the passed data is valid and returning error message or proceeds to the next stage
        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                name_exists = company_obj.customer_set.filter(name=value).exists()
                if name_exists: 
                    query &= Q(name=value)
                else:
                    main = "name not exist. try another field or check if you miss typed"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg
            
            if key == "email" and value != None:
                email_exists = company_obj.customer_set.filter(email=value).exists()
                if email_exists:
                    query &= Q(email=value)
                else:
                    main = "email not exist. try another field or check if you miss typed"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg

            if key == "customer_id" and value != None:
                customer_id_exists = company_obj.customer_set.filter(customer_id=value).exists()
                if customer_id_exists:
                    query &= Q(customer_id=value)
                else:
                    main = "customer_id not exist. try another field or check if you miss typed"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg
        
        customer_exists = company_obj.customer_set.filter(query).exists()
        if not customer_exists:
            main = "no customer found"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg
        else:
            customer_query_dict = company_obj.customer_set.filter(query).values("name","email","phone_number","address","notes","customer_id")
            main = "successfully found the data"
            second = {"customer_json":customer_query_dict}
            success_msg = OutputMessages.success_with_message(main,second)
            return success_msg


    def update(self,cleaned_data,user):
        required_fields = ["email","customer_id","update_data"]
        allowed_update_fields = ["name","email","phone_number","address","notes","customer_id"]
        

        cv = CustomValidation()
        validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(validation):
            return validation
        else:
            user_obj = validation[1]["object"]
            company_obj = user_obj.company

        #*checking that this customer is exists
        customer_exists =  company_obj.customer_set.filter(email=cleaned_data["email"],customer_id=cleaned_data["customer_id"]).exists()
        if not customer_exists:
            main = "this customer not exist with this email or the customer id"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg


        #*checking the update data fields
        update_data_validation = cv.passed_valid_fields(input_fields=cleaned_data["update_data"],valid_fields=allowed_update_fields)
        if not all(update_data_validation):
            main = "error in the update data fields"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg
        

        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralCustomerSerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid():

            check_unique_fields = update_data_serializer.check_unique(cleaned_data=cleaned_data["update_data"],company_object=company_obj)
            if all(check_unique_fields):
                update_obj = company_obj.customer_set.get(email=cleaned_data["email"],customer_id=cleaned_data["customer_id"])

                for key,value in cleaned_data["update_data"].items():
                    setattr(update_obj,key,value)

                update_obj.save()
                main = "updated the required fields"
                second = {"customer_json":{
                    "name":update_obj.name,
                    "email":update_obj.email,
                    "phone_number":update_obj.phone_number,
                    "address":update_obj.address,
                    "notes":update_obj.notes,
                    "customer_id":update_obj.customer_id,
                }}
                success_msg = OutputMessages.success_with_message(main,second)
                return success_msg
            
            err_msg = OutputMessages.error_with_message(check_unique_fields[1])
            return err_msg

        main = "invalid update_data fields"
        err_msg = OutputMessages.error_with_message(main)
        return err_msg



class GetCustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(default=None)
    address = serializers.CharField(default=None)
    customer_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data,user):

        allowed_fields = ["name","email","phone_number","address","customer_id"]

        
        cv = CustomValidation()
        validation = cv.basic_validation(user=user,empty_json=True)
        if not all(validation):
            print("its here")
            return validation

        else:
            user_obj = validation[1]["object"]
            company_obj = user_obj.company
        
        field_validation = cv.passed_valid_fields(input_fields=cleaned_data,valid_fields=allowed_fields)
        if not all(field_validation):
            return field_validation
        
        #this will have my query that will be passed later
        query = Q()
        #* this whole section is checking if the passed data is valid and returning error message or proccedes to the next stage
        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                name_exists = company_obj.customer_set.filter(name=value).exists()
                if name_exists: 
                    query &= Q(name=value)
                else:
                    main = "name not exist. try another field or check if you miss typed"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg
            
            if key == "email" and value != None:
                email_exists = company_obj.customer_set.filter(email=value).exists()
                if email_exists:
                    query &= Q(email=value)
                else:
                    main = "email not exist. try another field or check if you miss typed"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg

            if key == "customer_id" and value != None:
                customer_id_exists = company_obj.customer_set.filter(customer_id=value).exists()
                if customer_id_exists:
                    query &= Q(customer_id=value)
                else:
                    main = "customer_id not exist. try another field or check if you miss typed"
                    err_msg = OutputMessages.error_with_message(main)
                    return err_msg
        
        customer_exists = company_obj.customer_set.filter(query).exists()
        if not customer_exists:
            main = "no customer found"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg
        else:
            customer_query_dict = company_obj.customer_set.filter(query).values("name","email","phone_number","address","notes","customer_id")
            main = "successfully found the data"
            second = {"customer_json":customer_query_dict}
            success_msg = OutputMessages.success_with_message(main,second)
            return success_msg




    


