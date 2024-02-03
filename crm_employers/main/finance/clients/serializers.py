from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from finance.models import Income,Outcome,Customer
from user.models import User
from django.db.models import Q,F


#* customer table fields
    # name = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    # address = models.TextField(blank=True, null=True)
    # notes = models.TextField(blank=True, null=True)
    # customer_id = models.IntegerField()


class GeneralClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(max_length=15,default=None)
    address = serializers.CharField(max_length=350,default=None)
    notes = serializers.CharField(max_length=350,default=None)
    customer_id = serializers.IntegerField(default=None)

    def check_unique(self,cleaned_data):
        """
        this method will check if there is already existing data with the same id.

        unique fields are customer_id,email
        """

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





class CreateClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(max_length=15,default=None)
    address = serializers.CharField(max_length=350,default=None)
    notes = serializers.CharField(max_length=350,default=None)
    customer_id = serializers.IntegerField(default=None)
    
    def get_info(self,cleaned_data):
        allowed_fields = ["name","email","phone_number","address","notes","customer_id"]
        required_fields = [""]
        

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass at least one of the fields","example_json":{
                "name":"rechard ltd",
                "email":"rechard@rechard-ltd.com",
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


    def create(self,cleaned_data):
        required_fields = ["name","email","phone_number","address","notes","customer_id"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass all this fields","example_json":{
                "name":"rechard ltd",
                "email":"rechard@rechard-ltd.com",
                "phone_number":"0101010101",
                "address":"albert ainstein 3344 New York",
                "notes":"this customer is very important",
                "customer_id":123456789                
            }}
            return False,message
        
        #*checking that the user passed all fields
        for field in required_fields:
            if field not in cleaned_data.keys():
                message = {"error":"you must pass all fields","json_example":{
                "name":"rechard ltd",
                "email":"rechard@rechard-ltd.com",
                "phone_number":"0101010101",
                "address":"albert ainstein 3344 New York",
                "notes":"this customer is very important",
                "customer_id":123456789                
            },"and you passed":cleaned_data.keys()}
            
                return False,message


        #*checking if the customer is already exists 
        customer_exists = Customer.objects.filter(customer_id = cleaned_data["customer_id"]).exists()
        if customer_exists:
            message = {"error":"cant create new customer because this customer is already exists with this data"}
            return False,message


        #*checking that the email of the customer is not already existing
        customer_email_exist = Customer.objects.filter(email=cleaned_data["email"]).exists()
        if customer_email_exist:
            message = {"error":"this email is already registered and you cant create this customer with this email"}
            return False,message


        customer_obj = Customer.objects.create(
            name=cleaned_data["name"],
            email=cleaned_data["email"],
            phone_number=cleaned_data["phone_number"],
            address=cleaned_data["address"],
            notes=cleaned_data["notes"],
            customer_id=cleaned_data["customer_id"]
        )
        customer_obj.save()
        
        
        message = {"success":"created new customer successfully","created_data":{
            "name":cleaned_data["name"],
            "email":cleaned_data["email"],
            "phone_number":cleaned_data["phone_number"],
            "address":cleaned_data["address"],
            "notes":cleaned_data["notes"],
            "customer_id":cleaned_data["customer_id"]
        }}
        return True,message


class DeleteClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    customer_id = serializers.IntegerField(default=None)

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


    def delete(self,cleaned_data):
        required_fields = ["email","customer_id"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass all this fields","example_json":{
                "email":"test@test-ltd.com",
                "customer_id":123456789                
            }}
            return False,message
        
        #*checking that the user passed all fields
        for field in required_fields:
            if field not in cleaned_data.keys():
                message = {"error":"you must pass all fields","json_example":{
                "email":"test@test-ltd.com",
                "customer_id":123456789},"and you passed":cleaned_data.keys()}
            
                return False,message


        #*checking if the customer is already exists 
        customer_exists = Customer.objects.filter(customer_id = cleaned_data["customer_id"]).exists()
        if not customer_exists:
            message = {"error":"cant delete this customer because the customer not exist with this id"}
            return False,message


        #*checking that the email of the customer is not already existing
        customer_email_exist = Customer.objects.filter(email=cleaned_data["email"]).exists()
        if not customer_email_exist:
            message = {"error":"cant delete this customer because the customer not exists with this email"}
            return False,message


        customer_obj = Customer.objects.get(email=cleaned_data["email"],customer_id=cleaned_data["customer_id"])
        customer_obj.delete()
        
        message = {"success":"deleted the customer successfully"}
        return True,message



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



    


