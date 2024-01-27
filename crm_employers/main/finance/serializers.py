from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from .models import Income,Outcome,Customer
from user.models import User
from django.db.models import Q,F





allowed_update_fields = ["user","amount","description","payment_method","customer","date_recieved"]


#*general serailizers 

class GeneralIncomeSerializer(serializers.Serializer):
    """
    purpose of this class is basicly to have field validation when updating existing data
    and the data is passed to us from the user input and we dont trust it
    """
    user_email = serializers.EmailField(default=None)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2,default=None)
    date_received = serializers.DateField(default=None)
    description = serializers.CharField(max_length=300,default=None)
    payment_method = serializers.ChoiceField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer')],default=None)
    customer_id = serializers.IntegerField(default=None)


    def fk_check(self,cleaned_data):
        """
        main reason for this method is if the required fields to change are user or customer
        that represented in the database as a foreign key 

        Returns:
            dict of the fields 
            if user or customer are required to change then it will get their object and pass it in as a value.
        """

        if "user_email" in cleaned_data["update_data"].keys():
            user_obj_exists = User.objects.filter(email=cleaned_data["update_data"]["user_email"]).exists()
            if user_obj_exists:
                cleaned_data["update_data"]["user"] = User.objects.get(email=cleaned_data["update_data"]["user_email"])
                cleaned_data["update_data"].pop("user_email")

            else:
                message = {"error":"this user is not exists"}
                return False,message



        if "customer_id" in cleaned_data["update_data"].keys():
            
            customer_obj_exists = Customer.objects.filter(customer_id=cleaned_data["update_data"]["customer_id"]).exists()
            if customer_obj_exists:
                cleaned_data["update_data"]["customer"] =  Customer.objects.get(customer_id=cleaned_data["update_data"]["customer_id"])
                cleaned_data["update_data"].pop("customer_id")

            else:
                message = {"error":"this customer is not exists"}
                return False,message


        return True,cleaned_data



#* income CRUD serializers

class CreateIncomeSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10,decimal_places=2)
    date_received = serializers.DateField()
    description = serializers.CharField(max_length=300)
    payment_method = serializers.CharField(max_length=30)
    customer_id = serializers.IntegerField()


    def create(self,cleaned_data):
        #checking if the user exists
        user_exists = User.objects.filter(email=cleaned_data["user_email"]).exists()
        if user_exists:
            user_obj = User.objects.get(email=cleaned_data["user_email"])


            #checking if the customer exists
            customer_exists = Customer.objects.filter(customer_id=cleaned_data["customer_id"])
            if customer_exists:
                customer_obj = Customer.objects.get(customer_id=cleaned_data["customer_id"])

                income_obj = Income.objects.create(
                    user=user_obj,
                    amount=cleaned_data["amount"],
                    date_received=cleaned_data["date_received"],
                    description=cleaned_data["description"],
                    payment_method=cleaned_data["payment_method"],
                    customer=customer_obj
                    )
                #saving the created object
                income_obj.save()

                message = {"success":f"created income by {user_obj.username}. amount : {income_obj.amount} . with payment method : {income_obj.payment_method} in {income_obj.date_received}"}
                return True,message
            
            message = {"error":"this customer doesnt exists"}
            return False,message

        message = {"error":"user not exists"}
        return False,message


class DeleteIncomeSerializer(serializers.Serializer):
    date_received = serializers.DateField(default=None)
    income_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data):
        allowed_fields = ["date_received","income_id"]

        #checking that the user didnt pass both fields
        if len(cleaned_data.keys()) >= 2:
            message = {"error":"cant pass two fields and must choose one"}
            return False,message
            

        #checking that the fields are in the allowed list
        for keys in cleaned_data.keys():
            if keys not in allowed_fields:
                message = {"error":"invalid fields passed"}
                return False,message
            
        

        if "income_id" in cleaned_data.keys():
            required_id = cleaned_data["income_id"]
            income_exists = Income.objects.filter(id=required_id).exists()
            if income_exists:
                income_dict = {}
                income_list = Income.objects.filter(id=required_id)
                for income in income_list:

                    income_dict[str(income.id)] = {
                        "user":income.user.email,
                        "amount":income.amount,
                        "date_received":income.date_received,
                        "description":income.description,
                        "payment_method":income.payment_method,
                        "customer":income.customer.email,
                        "id":income.id
                        }
                message = {"success":{"income":income_dict}}
                return True,message
            
            return False,{"error":"income not exists on that date"}


        if "date_received" in cleaned_data.keys():
                
            #required date from cleaned_data
            required_date = cleaned_data["date_received"]
            #first checking if the income exists
            income_exists = Income.objects.filter(date_received=required_date).exists()
            if income_exists:
                income_dict = {}
                income_list = Income.objects.filter(date_received=required_date)
                for income in income_list:

                    income_dict[str(income.id)] = {
                        "user":income.user.email,
                        "amount":income.amount,
                        "date_received":income.date_received,
                        "description":income.description,
                        "payment_method":income.payment_method,
                        "customer":income.customer.email,
                        "id":income.id
                        }
                message = {"success":{"income":income_dict}}
                return True,message
            
            return False,{"error":"income not exists on that date"}



    def delete(self,cleaned_data):
        required_fields = ["date_received","income_id"]
        
        #checking if one of fields are invalid or missing
        try:
            required_date = cleaned_data["date_received"]
            required_id = cleaned_data["income_id"]
        except:
            message = {"error":"one of the fields are missing or invalid"}
            return False,message
        
        #first checking if the income exists
        income_exists = Income.objects.filter(date_received=required_date).filter(id=required_id).exists()
        if income_exists:
            delete_obj = Income.objects.get(id=required_id)

            #here im serializing the income object
            serialized_obj = {
                    "user":delete_obj.user.email,
                    "amount":delete_obj.amount,
                    "date_received":delete_obj.date_received,
                    "description":delete_obj.description,
                    "payment_method":delete_obj.payment_method,
                    "costumer":delete_obj.customer.email,
                    "deleted_id":required_id
                    }

            message = {"success":{"deleted information":serialized_obj}}
            delete_obj.delete()
            return True,message


        message = {"error":"income not found by this id"}
        return False,message


class UpdateIncomeSerializer(serializers.Serializer):
    date_received = serializers.DateField(default=None)
    income_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default=None)



    def get_info(self,cleaned_data):
        allowed_fields = ["date_received","income_id"]

        #checking that the user didnt pass both fields
        if len(cleaned_data.keys()) >= 2:
            message = {"error":"cant pass two fields and must choose one"}
            return False,message
            

        #checking that the fields are in the allowed list
        for keys in cleaned_data.keys():
            if keys not in allowed_fields:
                message = {"error":"invalid fields passed"}
                return False,message
            


        if "income_id" in cleaned_data.keys():
            required_id = cleaned_data["income_id"]
            income_exists = Income.objects.filter(id=required_id).exists()
            if income_exists:
                income_dict = {}
                income_list = Income.objects.filter(id=required_id)
                for income in income_list:

                    income_dict[str(income.id)] = {
                        "user":income.user.email,
                        "amount":income.amount,
                        "date_received":income.date_received,
                        "description":income.description,
                        "payment_method":income.payment_method,
                        "customer":income.customer.email,
                        "id":income.id
                        }
                message = {"success":{"income":income_dict}}
                return True,message
            
            return False,{"error":"income not exists on that date"}


        if "date_received" in cleaned_data.keys():
                
            #required date from cleaned_data
            required_date = cleaned_data["date_received"]
            #first checking if the income exists
            income_exists = Income.objects.filter(date_received=required_date).exists()
            if income_exists:
                income_dict = {}
                income_list = Income.objects.filter(date_received=required_date)
                for income in income_list:

                    income_dict[str(income.id)] = {
                        "user":income.user.email,
                        "amount":income.amount,
                        "date_received":income.date_received,
                        "description":income.description,
                        "payment_method":income.payment_method,
                        "customer":income.customer.email,
                        "id":income.id
                        }
                message = {"success":{"income":income_dict}}
                return True,message
            
            return False,{"error":"income not exists on that date"}



    def update(self,cleaned_data):
        allowed_update_fields = ["user_email","amount","description","payment_method","customer_id","date_received"]
        allowed_fields = ["income_id","update_data","date_received"]
        required_id = cleaned_data["income_id"]

        
        #checking that the user input is not less or more then required fields
        for key,value in self.__getattribute__("data").items():
            
            #* checking that the fields are in the allowed list
            if key not in allowed_fields:
                message = {"error":"invalid key passed"}
                return False,message
            
            #* checking that all three fields passed
            if value == None:
                message = {"error":"invalid fields passed"}
                return False,message
            
            #* checking that the keys inside the update_field are allowed to be updated
            if key == "update_data":
                for key,_ in value.items():
                    if key not in allowed_update_fields:
                        message = {"error":"invalid fields in update fields"}
                        return False,message



        #* this part is passing the update_data dict into another serializer so serialization
        validation_serializer = GeneralIncomeSerializer(data=cleaned_data["update_data"])

        if validation_serializer.is_valid():

            #* this is adding user object or customer objects into the cleaned_data if the user want to change the
            #* user or the customer 
            cleaned_data = validation_serializer.fk_check(cleaned_data=cleaned_data)

            #* result of the method might be True,cleaned_data(dict) so its meaning that the user or email are found
            if all(cleaned_data):
                #first checking if the income exists
                income_exists = Income.objects.filter(id=required_id).exists()
                if income_exists:
                    update_obj = Income.objects.get(id=required_id)

                    #here im getting a copy of the information for representation
                    for keys,values in cleaned_data[1]["update_data"].items():
                        
                        setattr(update_obj,keys,values)
                    
                    update_obj.save()
                    updated_obj_information = {
                            "user_email":update_obj.user.email,
                            "amount":update_obj.amount,
                            "date_recieved":update_obj.date_received,
                            "description":update_obj.description,
                            "payment_method":update_obj.payment_method,
                            "custumer_id":update_obj.customer.customer_id,
                            }
                                
                    message = {"success":{"updated information":updated_obj_information}}
                    return True,message

                
                message = {"error":"income not exists"}
                return False,

            #if user or customer are not found 
            message = {"error":cleaned_data[1]}
            return False,message

        
        message = {"error":"in update_data one of the values are invalid"}
        return False,message


class GetIncomeSerializer(serializers.Serializer):
    user_email = serializers.EmailField(default=None)
    date_received = serializers.DateField(default=None)
    customer_id = serializers.IntegerField(default=None)


    def get_info(self,cleaned_data):
        """
        getting info by one of the fields 
        """
        allowed_fields = ["date_received","user_email","customer_id"]


        #checking that the fields are in the allowed list
        for keys in cleaned_data.keys():
            if keys not in allowed_fields:
                message = {"error":"invalid fields passed"}
                return False,message


        #this will have the query fields that are not None
        query = Q()

        #checking that the user input is not less or more then required fields
        for key,value in self.__getattribute__("data").items():
            
            #* checking that the fields are in the allowed list
            if key not in allowed_fields:
                message = {"error":"invalid key passed"}
                return False,message
            
            #* passing the key,values that are not None into our passed_fields dict
            if value != None:
                if key == "user_email":
                    #checking that the user exists first
                    user_obj_exists = User.objects.filter(email=value).exists()
                    if user_obj_exists:
                        user_obj = User.objects.get(email=value)
                        query &= Q(user=user_obj)
                    else:
                        message = {"error":"this user is not exists"}
                        return False,message

                if key == "customer_id":
                    customer_obj_exists = Customer.objects.filter(customer_id=value).exists()
                    if customer_obj_exists:
                        customer_obj =  Customer.objects.get(customer_id=value)
                        query &= Q(customer=customer_obj)

                    else:
                        message = {"error":"this customer is not exists"}
                        return False,message

                if key == "date_received":
                    query &= Q(date_received=value)



        #* this is the query withe the provided fields
        search_query_exists = Income.objects.filter(query).all().annotate(
            user_email=F("user__email"),
            customer_id_=F("customer__customer_id")).values("user_email","amount","date_received","customer_id_").exists()
        
        if search_query_exists:

            search_query = Income.objects.filter(query).all().annotate(
            user_email=F("user__email"),
            customer_id_=F("customer__customer_id")).values("user_email","amount","date_received","customer_id_")
        
            message = {"data":search_query}
            return True,message

        message={"error":"data not found by provided fields"}
        return False,message




#* outcome serializers

class CreateOutcomeSerializer(serializers.Serializer):
    pass


class DeleteOutcomeSerializer(serializers.Serializer):
    pass


class UpdateOutcomeSerializer(serializers.Serializer):
    pass


class GetOutcomeSerializer(serializers.Serializer):
    pass

