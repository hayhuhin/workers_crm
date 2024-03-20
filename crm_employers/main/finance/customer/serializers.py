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







class GeneralClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(max_length=15,default=None)
    address = serializers.CharField(max_length=350,default=None)
    notes = serializers.CharField(max_length=350,default=None)
    customer_id = serializers.IntegerField(default=None)

    def check_unique(self,cleaned_data):

        for key in cleaned_data.keys():
            #* checking if the email exists
            if key == "email":
                email_exists = Customer.objects.filter(email=cleaned_data["email"]).exists()
                if email_exists:
                    message = {"error":"this email is already exist and cant be used"}
                    return False,message
                
            if key == "customer_id":
                customer_id_exists = Customer.objects.filter(customer_id=cleaned_data["customer_id"]).exists()
                if customer_id_exists:
                    message = {"error","this customer id is already exist and cant be used"}
                    return False,message


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
            #!!! have to fix the customer_obj.values() not working it has to be query dict
            second = {"customer_json":customer_obj.values("name","email","phone_number","address",)}
            success_msg = OutputMessages.success_with_message(main,second)
            return success_msg



class UpdateClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    customer_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default=None)

    def get_info(self,cleaned_data):
        allowed_fields = ["name","email","phone_number","address","notes","customer_id"]
        required_fields = [""]
        

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass at least one of the fields","example_json":{
                "name":"test ltd",
                "email":"test@test-ltd.com",
                "customer_id":123456789
            }}
            return False,message
        
        #*checking fort allowed fields
        for key in cleaned_data.keys():
            if key not in allowed_fields:
                message = {"error":f"passed invalid field -{key}-"}
                return False,message

        #this will have my query that will be passed later
        query = Q()

        #* this whole section is checking if the passed data is valid and returning error message or proccedes to the next stage
        for key,value in self.__getattribute__("data").items():
            if key == "name" and value != None:
                name_exists = Customer.objects.filter(name=value).exists()
                if name_exists: 
                    query &= Q(name=value)
                else:
                    message = {"error":"name not exist. try another field or check if you miss typed"}
                    return False,message
                
            if key == "email" and value != None:
                email_exists = Customer.objects.filter(email=value).exists()
                if email_exists:
                    query &= Q(email=value)
                else:
                    message = {"error":"email not exist. try another field or check if you miss typed"}
                    return False,message

            if key == "customer_id" and value != None:
                customer_id_exists = Customer.objects.filter(customer_id=value).exists()
                if customer_id_exists:
                    query &= Q(customer_id=value)
                else:
                    message = {"error":"customer_id not exist. try another field or check if you miss typed"}
                    return False,message
        
        query_data = Customer.objects.filter(query).values("name","email","phone_number","address","notes","customer_id")
        message = {"success":query_data}
        return True,message

    def update(self,cleaned_data):
        required_fields = ["email","customer_id","update_data"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass all this fields","example_json":{
                "email":"rechard@rechard-ltd.com",
                "customer_id":123456789,
                "update_data":{
                    "name":"new name",
                    "email":"new@new.com",
                    "phone_number":"111222333444",
                    "address":"alfred kakoi 1122",
                    "notes":"some new notes",
                    "customer_id":11223344
                    }}}
            return False,message
        
        #*checking that the user passed all fields
        for field in required_fields:
            if field not in cleaned_data.keys():
                message = {"error":"you must pass all fields","json_example":{
                "email":"rechard@rechard-ltd.com",
                "customer_id":123456789,
                "update_data":{
                    "name":"new name",
                    "email":"new@new.com",
                    "phone_number":"111222333444",
                    "address":"alfred kakoi 1122",
                    "notes":"some new notes",
                    "customer_id":11223344
                    }},"and you passed":cleaned_data.items()}
            
                return False,message


        #*checking if the customer is already exists 
        customer_exists = Customer.objects.filter(customer_id = cleaned_data["customer_id"]).exists()
        if not customer_exists:
            message = {"error":"this customer is not exist with this id"}
            return False,message


        #*checking that the email of the customer is not already existing
        customer_email_exist = Customer.objects.filter(email=cleaned_data["email"]).exists()
        if not customer_email_exist:
            message = {"error":"this customer not exist with this email"}
            return False,message


        #* checkiing that the user didnt pass empty update data dict
        if not cleaned_data["update_data"]:
            message = {"error":"you cant pass empty udpate_data ","json_example for updata_data":{
                    "name":"new name",
                    "email":"new@new.com",
                    "phone_number":"111222333444",
                    "address":"alfred kakoi 1122",
                    "notes":"some new notes",
                    "customer_id":11223344
                    }}
            return False,message
        

        #* checking that bothg fields are matching the quiery
        update_obj_exist = Customer.objects.filter(email=cleaned_data["email"],customer_id=cleaned_data["customer_id"]).exists()
        if not update_obj_exist:
            message = {"error":"customer not exist with both data provided. or there is a mismatch with the fields or miss typed them"}
            return False,message


        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralClientSerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=True):

            check_unique_fields = update_data_serializer.check_unique(cleaned_data=cleaned_data["update_data"])
            if all(check_unique_fields):
                update_obj = Customer.objects.get(email=cleaned_data["email"],customer_id=cleaned_data["customer_id"])

                for key,value in cleaned_data["update_data"].items():
                    setattr(update_obj,key,value)

                update_obj.save()
                message = {"success":"updated the required fields","updated_data":{
                    "name":update_obj.name,
                    "email":update_obj.email,
                    "phone_nomber":update_obj.phone_number,
                    "address":update_obj.address,
                    "notes":update_obj.notes,
                    "customer_id":update_obj.customer_id
                }}
                return True,message
            
            return False,check_unique_fields[1]

        message = {"error":"invalid update_data fields"}
        return False,message



class GetClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    customer_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data):
        allowed_fields = ["name","email","customer_id"]
        required_fields = [""]
        

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass at least one of the fields","example_json":{
                "name":"rechard ltd",
                "email":"rechard@rechard-ltd.com",
                "customer_id":123456789
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
                name_exists = Customer.objects.filter(name=value).exists()
                if name_exists: 
                    query &= Q(name=value)
                else:
                    message = {"error":"name not exist. try another field or check if you miss typed"}
                    return False,message
                
            if key == "email" and value != None:
                email_exists = Customer.objects.filter(email=value).exists()
                if email_exists:
                    query &= Q(email=value)
                else:
                    message = {"error":"email not exist. try another field or check if you miss typed"}
                    return False,message

            if key == "customer_id" and value != None:
                customer_id_exists = Customer.objects.filter(customer_id=value).exists()
                if customer_id_exists:
                    query &= Q(customer_id=value)
                else:
                    message = {"error":"customer_id not exist. try another field or check if you miss typed"}
                    return False,message
        
        query_data = Customer.objects.filter(query).values("name","email","phone_number","address","notes","customer_id")
        message = {"success":query_data}
        return True,message



    


