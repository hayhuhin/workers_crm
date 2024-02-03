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


class GeneralOutcomeSerializer(serializers.Serializer):
    user_email = serializers.EmailField(default=None)
    date_time = serializers.DateField(default=None)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2,default=None)
    description = serializers.CharField(max_length=300,default=None)
    payment_method = serializers.ChoiceField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer')],default=None)
    vendor = serializers.CharField(default=None)
    project_or_department = serializers.CharField(default=None)

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

        return True,cleaned_data




#* income CRUD serializers

class CreateIncomeSerializer(serializers.Serializer):
    user_email = serializers.EmailField(default=None)
    amount = serializers.DecimalField(max_digits=10,decimal_places=2,default=None)
    date_received = serializers.DateField(default=None)
    description = serializers.CharField(max_length=300,default=None)
    payment_method = serializers.CharField(max_length=30,default=None)
    customer_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data):
        message = {"error":"for creating the income this is how the json should look like","json_example":{
                "user_email":"the user email that submits the income",
                "amount":"float number of the amount",
                "date_received":"YYYY-MM-DD format",
                "description":"text field of 300 digits allowed",
                "payment_method":"credit_card or cash allowed",
                "costumer_id":"existing customer ID"}
                }
        
        return True,message


    def create(self,cleaned_data):
        required_fields = ["user_email","amount","date_received","description","payment_method","customer_id"]
        allowed_fields = ["user_email","amount","date_received","description","payment_method","customer_id"]
    
        #checking if the user passed allowed_fields
        for key in cleaned_data.keys():
            if key not in allowed_fields:
                message = {"error":"invalid field passed"}
                return False,message
        
        #checking that the user passed all required fields
        for fields in required_fields:
            if fields not in cleaned_data.keys():
                message = {"error":"you must pass all required fields","required_fields":required_fields}
                return False,message



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
        
        if not cleaned_data.items():
            message = {"error":"the user must pass one of the fields (date_received or income_id)"}
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
        allowed_fields = ["date_received","income_id"]

        #performing couple of checks
        for key in cleaned_data.keys():
            #checking if the fields are allowed
            if key not in allowed_fields:
                message = {"error":"invalid field passed","required_fields":required_fields}
                return False,message
            
            #user must pass only income_id fields
            if key != "income_id":
                message = {"error":"you must pass only income_id to delete this income"}
                return False,message
        
        if not cleaned_data.items():
            message = {"error":"you must pass income_id to delete this specific income record"}
            return False,message
        
        #first checking if the income exists
        income_exists = Income.objects.filter(id=cleaned_data["income_id"]).exists()
        if income_exists:
            delete_obj = Income.objects.get(id=cleaned_data["income_id"])

            #here im serializing the income object
            serialized_obj = {
                    "user":delete_obj.user.email,
                    "amount":delete_obj.amount,
                    "date_received":delete_obj.date_received,
                    "description":delete_obj.description,
                    "payment_method":delete_obj.payment_method,
                    "costumer":delete_obj.customer.email,
                    "deleted_id":cleaned_data["income_id"]
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
        
        if not cleaned_data.items():
            message = {
                    "error":{
                        "example for the acceptebale json":{
                            "date_received":"YYYY-MM-DD",
                            "income_id":"id of the income",
                            "update_data":{
                                "user_email":"user email",
                                "amount":"amount",
                                "description":"description",
                                "payment_method":"payment_method",
                                "customer_id":"customer id",
                                "date_received":"YYYY-MM-DD"
                            }}}}
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
        required_fields = ["income_id","update_data"]

        #checking if the user passed empty json
        if not cleaned_data.items():
            message = {"error":"must pass valid fields","required fields":{
                        "example for the acceptebale json":{
                            "date_received":"YYYY-MM-DD",
                            "income_id":"id of the income",
                            "update_data":{
                                "user_email":"user email",
                                "amount":"amount",
                                "description":"description",
                                "payment_method":"payment_method",
                                "customer_id":"customer id",
                                "date_received":"YYYY-MM-DD"
                            }}}}
            
            return False,message

        for key in cleaned_data.keys():
            if key not in required_fields:
                message = {"error":f"invalid field {key}"}
                return False,message


        #checking that the user input is not less or more then required fields
        for key,value in self.__getattribute__("data").items():

            if key == "date_received" and value != None:
                message = {"error":f"you passed {key} but its not required to update the income "}
                return False,message

            #* checking that the fields are in the allowed list
            if key not in allowed_fields:
                message = {"error":"invalid key passed"}
                return False,message
            
            #* checking that the user didnt pass invalid fields
            if value and key not in required_fields:
                message = {"error":f"you passed {key} but this field doesnt required and you have to pass only : {required_fields}"}
                return False,message
            

            #* checking that the keys inside the update_field are allowed to be updated
            if key == "update_data":
                for key,_ in value.items():
                    if key not in allowed_update_fields:
                        message = {"error":"invalid fields in update fields"}
                        return False,message



        #* this part is passing the update_data dict into another serializer to serialization
        validation_serializer = GeneralIncomeSerializer(data=cleaned_data["update_data"])

        if validation_serializer.is_valid():

            #* this is adding user object or customer objects into the cleaned_data if the user want to change the
            #* user or the customer 
            update_data = validation_serializer.fk_check(cleaned_data=cleaned_data)

            #* result of the method might be True,cleaned_data(dict) so its meaning that the user or email are found
            if all(update_data):
                required_id = cleaned_data["income_id"]

                #first checking if the income exists
                outcome_exists = Income.objects.filter(id=required_id).exists()
                if outcome_exists:
                    update_obj = Income.objects.get(id=required_id)

                    #here im getting a copy of the information for representation
                    for keys,values in update_data[1]["update_data"].items():
                        
                        setattr(update_obj,keys,values)
                    
                    update_obj.save()
                    updated_obj_information = {
                            "user_email":update_obj.user.email,
                            "amount":update_obj.amount,
                            "date_received":update_obj.date_received,
                            "description":update_obj.description,
                            "payment_method":update_obj.payment_method,
                            "customer_id":update_obj.customer.customer_id
                            }
                                
                    message = {"success":{"updated information":updated_obj_information}}
                    return True,message

                
                message = {"error":"income not exists"}
                return False,message

            #if user not found
            message = {"error":update_data[1]}
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

        if not cleaned_data.items():
            message = {"error":"must pass one of the fields : (date_received,user_email,customer_id)"}

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



        #* this is the query with the provided fields
        search_query_exists = Income.objects.filter(query).all().annotate(
            user_email=F("user__email"),
            customer_id_=F("customer__customer_id")).values("user_email","amount","date_received","customer_id_").exists()
        
        if search_query_exists:

            search_query = Income.objects.filter(query).all().annotate(
            user_email=F("user__email"),
            customer_id_=F("customer__customer_id")).values("id","user_email","amount","date_received","customer_id_")
        
            message = {"data":search_query}
            return True,message

        message={"error":"data not found by provided fields"}
        return False,message



#* outcome serializers
    
class CreateOutcomeSerializer(serializers.Serializer):
    user_email = serializers.EmailField(default = None)
    date_time = serializers.DateField(default = None)
    category = serializers.CharField(max_length=50,default = None)
    amount = serializers.DecimalField(max_digits=10,decimal_places=2,default = None)
    description = serializers.CharField(max_length=300,default = None)
    payment_method = serializers.CharField(max_length=50,default = None)
    vendor = serializers.CharField(max_length=100,default=None)
    project_or_department = serializers.CharField(max_length=100,default=None)


    def get_info(self,cleaned_data):
        message = {"success":{"post example":{
            "user_email":"ben@ben.com",
            "date_time":"2023-11-11",
            "category":"one,two,three",
            "amount":123123123,
            "description":"some description about the outcome",
            "payment_method":"credit_card,bank_transfer,cash",
            "vendor":"max stock",
            "project_or_department":"department"
        }}}

        return True,message


    def create(self,cleaned_data):
        #checking if the user exists
        required_fields = ["user_email","date_time","category","amount","description","payment_method","vendor","project_or_department"]

        if not cleaned_data.items():
            message = {"error":"you must pass these fields","example":{
                "user_email": "ben@ben.com",
                "date_time" : "2024-11-11",
                "category" : "spendings" ,
                "amount":110011,
                "description": "just some description about the things here",
                "payment_method" :"bank_transfer",
                "vendor" : "max stock",
                "project_or_department" : "department"
            }}
            return False,message

        for fields in required_fields:
            if fields not in cleaned_data.keys():
                message = {"error":"you must provide all the fields","example_fields":{
                "user_email": "ben@ben.com",
                "date_time" : "2024-11-11",
                "category" : "spendings" ,
                "amount":110011,
                "description": "just some description about the things here",
                "payment_method" :"bank_transfer",
                "vendor" : "max stock",
                "project_or_department" : "department"}}
                
                return False,message


        user_exists = User.objects.filter(email=cleaned_data["user_email"]).exists()
        if user_exists:

            user_obj = User.objects.get(email=cleaned_data["user_email"])


            outcome_obj = Outcome.objects.create(
                user = user_obj,
                date_time = cleaned_data["date_time"],
                category = cleaned_data["category"],
                amount = cleaned_data["amount"],
                description = cleaned_data["description"],
                payment_method = cleaned_data["payment_method"],
                vendor = cleaned_data["vendor"],
                project_or_department = cleaned_data["project_or_department"]
                )
            
            #saving the created object
            outcome_obj.save()
            message = {"success":f"created outcome by {user_obj.username}. amount : {outcome_obj.amount} . with payment method : {outcome_obj.payment_method} in {outcome_obj.date_time}"}
            return True,message
        
        message = {"error":"user not exists"}
        return False,message
        

class DeleteOutcomeSerializer(serializers.Serializer):
    date_time = serializers.DateField(default=None)
    outcome_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data):
        allowed_fields = ["date_time","outcome_id"]
        query = Q()

        #checkinf that the dict is not empty
        if not cleaned_data.items():
            message = {"error":"you have to provide at least one of the fields","json example":{
                "date_time":"2024-11-11",
                "outcome_id":123
                }}
            return False,message

        for key,value in cleaned_data.items():
            if key not in allowed_fields:
                message = {"error":"invalid key or value"}
                return False,message

            
            else:
                if key == "outcome_id":
                    query &= Q(id=value)
                if key == "date_time":
                    query &= Q(date_time=value)
        
        #checking that the outcome exists
        obj_exists = Outcome.objects.filter(query).exists()
        if obj_exists:
            outcome_obj = Outcome.objects.filter(query).all()
            message = {"success":{"query result is:":outcome_obj.values()}}
            return True,message
        
        message = {"error":"nothing have found in the database"}
        return False,message


    def delete(self,cleaned_data):
        allowed_fields = ["outcome_id"]
        query = Q()


        #check if the dict is empty
        if not cleaned_data.items():
            message = {"error":"you have to provide one of the fields","json example":{
                "outcome_id":123
                }}
            return False,message

        #checking that both fields are provided
        if "outcome_id" not in cleaned_data.keys():
            message = {"error":"you must provide outcome_id field with id to delete"}
            return False,message
        
        for key,value in cleaned_data.items():
            if key not in allowed_fields:
                message = {"error":"invalid key or value"}
                return False,message

            
            else:
                if key == "outcome_id":
                    query &= Q(id=value)
                if key == "date_time":
                    query &= Q(date_time=value)
        
        #checking that the outcome exists
        obj_exists = Outcome.objects.filter(query).exists()
        if obj_exists:
            outcome_obj = Outcome.objects.get(query)
            outcome_obj.delete()
            message = {"success":"deleted successfuly "}
            return True,message
        
        message = {"error":"nothing have found in the database"}
        return False,message


class UpdateOutcomeSerializer(serializers.Serializer):
    date_time = serializers.DateField(default=None)
    outcome_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default=None)



    def get_info(self,cleaned_data):
        allowed_fields = ["date_time","outcome_id"]

        #checking that the user didnt pass both fields
        if len(cleaned_data.keys()) >= 2:
            message = {"error":"cant pass two fields and must choose one"}
            return False,message
            

        #checking that the fields are in the allowed list
        for keys in cleaned_data.keys():
            if keys not in allowed_fields:
                message = {"error":"invalid fields passed"}
                return False,message
            

        if not cleaned_data.items():
            message = {"error":"must provide at least one of these fields: (date_time or outcome_id) this will represent its current data"}
            return False,message
            


        if "outcome_id" in cleaned_data.keys():
            required_id = cleaned_data["outcome_id"]
            outcome_exists = Outcome.objects.filter(id=required_id).exists()
            if outcome_exists:
                outcome_obj = Outcome.objects.get(id=required_id)
                outcome_dict = {}

                outcome_dict[str(outcome_obj.id)] = {
                    "user":outcome_obj.user.email,
                    "date_time":outcome_obj.date_time,
                    "category":outcome_obj.category,
                    "amount":outcome_obj.amount,
                    "description":outcome_obj.description,
                    "payment_method":outcome_obj.payment_method,
                    "vendor":outcome_obj.vendor,
                    "project_or_department":outcome_obj.project_or_department,
                    "id":outcome_obj.id
                    }
                
                message = {"success":{"outcome":outcome_dict}}
                return True,message
            
            return False,{"error":"outcome not exists with this id"}


        if "date_time" in cleaned_data.keys():
                
            #required date from cleaned_data
            required_date = cleaned_data["date_time"]
            #first checking if the outcome exists
            outcome_exists = Outcome.objects.filter(date_time=required_date).exists()
            if outcome_exists:
                outcome_dict = {}
                outcome_list = Outcome.objects.filter(date_time=required_date)
                for outcome in outcome_list:

                    outcome_dict[str(outcome.id)] = {
                    "user":outcome.user.username,
                    "date_time":outcome.date_time,
                    "category":outcome.category,
                    "amount":outcome.amount,
                    "description":outcome.description,
                    "payment_method":outcome.payment_method,
                    "vendor":outcome.vendor,
                    "project_or_department":outcome.project_or_department
                        }
                message = {"success":{"outcome":outcome_dict}}
                return True,message
            
            return False,{"error":"outcome not exists on that date"}



    def update(self,cleaned_data):
        allowed_update_fields = ["user_email","date_time","category","amount","description","payment_method","vendor","project_or_department"]
        allowed_fields = ["outcome_id","update_data","date_received"]
        required_fields = ["outcome_id","update_data"]


        #* checkinf if the json is empty
        if not cleaned_data.items():
            message = {"error":"you must pass these fields","json_example":{
                "outcome_id":1,
                "update_data":{
                    "user_email":"test@test.com",
                    "date_time":"2023-11-11",
                    "category":"sales",
                    "amount":1234567,
                    "description":"test description",
                    "payment_method":"credit_card",
                    "vendor":"max stock",
                    "project_or_department":"max stock",
                    "id":112233
                            }
                }}
            return False,message
        



        #* checking that the user passed currectly all required fields
        for key,value in self.__getattribute__("data").items():


            #* the user cant pass date_received into the post request
            if key == "date_received":
                if value != None:
                    message = {"error":"you cant pass this field","json_example":{
                        "outcome_id":1,
                        "update_data":{
                            "user_email":"test@test.com",
                            "date_time":"2023-11-11",
                            "category":"sales",
                            "amount":1234567,
                            "description":"test description",
                            "payment_method":"credit_card",
                            "vendor":"max stock",
                            "project_or_department":"max stock",
                            "id":112233
                            }}}
                    
                    return False,message

            #* checking that the user didnt pass empty update fields
            if key == "update_data":
                if not value:
                    message = {"error":"cant pass empty update_data json","json example":{
                    "outcome_id":1,
                    "update_data":{
                        "user_email":"test@test.com",
                        "date_time":"2023-11-11",
                        "category":"sales",
                        "amount":1234567,
                        "description":"test description",
                        "payment_method":"credit_card",
                        "vendor":"max stock",
                        "project_or_department":"max stock",
                        "id":112233
                            }}}
                    return False,message



                #* loop over the nested dict keys and checking if its in the allowed fields
                for item in value.keys():
                    if item not in allowed_update_fields:
                        message = {"error":"invalid fields in update_data fields"}
                        return False,message



        #* this part is passing the update_data dict into another serializer to serialization
        validation_serializer = GeneralOutcomeSerializer(data=cleaned_data["update_data"])

        if validation_serializer.is_valid():

            #* this is adding user object or customer objects into the cleaned_data if the user want to change the
            #* user foreignkey extractipon
            cleaned_data = validation_serializer.fk_check(cleaned_data=cleaned_data)

            #* result of the method might be True,cleaned_data(dict) so its meaning that the user or email are found
            if all(cleaned_data):
                required_id = cleaned_data["required_id"]
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


class GetOutcomeSerializer(serializers.Serializer):
    pass

