from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from .models import Income,Outcome,Customer
from user.models import User
from django.db.models import Q,F
from custom_validation.validation import CustomValidation,OutputMessages





# allowed_update_fields = ["user","amount","description","payment_method","customer","date_recieved"]


#*general serializers 

class GeneralIncomeSerializer(serializers.Serializer):
    """
    purpose of this class is basically to have field validation when updating existing data
    and the data is passed to us from the user input and we dont trust it
    """
    user = serializers.EmailField(default=None)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2,default=None)
    description = serializers.CharField(max_length=300,default=None)
    payment_method = serializers.ChoiceField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer')],default=None)
    customer_id = serializers.IntegerField(default=None)


    def fk_check(self,update_data,company_object):
        """
        main reason for this method is if the required fields to change are user or customer
        that represented in the database as a foreign key 

        Returns:
            dict of the fields 
            if user or customer are required to change then it will get their object and pass it in as a value.
        """

        if "email" in update_data.keys():
            user_exists = company_object.user_set.filter(email=update_data["user_email"]).exists()
            if not user_exists:
                main = "this user is not exists"
                error_msg = OutputMessages.error_with_message(main)
                return error_msg
            
            else:
                update_data["user"] = company_object.user_set.get(email=update_data["user_email"])



        if "customer_id" in update_data.keys():
            
            customer_exists = company_object.customer_set.filter(customer_id=update_data["customer_id"]).exists()
            if not customer_exists:
                main = "this customer is not exists"
                error_msg = OutputMessages.error_with_message(main)
                return error_msg

            else:
                update_data["customer"] = company_object.customer_set.get(customer_id=update_data["customer_id"])
                update_data.pop("customer_id")



        return True,update_data


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
    amount = serializers.DecimalField(max_digits=10,decimal_places=2,default=None)
    date_received = serializers.DateField(default=None)
    description = serializers.CharField(max_length=300,default=None)
    payment_method = serializers.CharField(max_length=30,default=None)
    customer_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data,user):

        cv = CustomValidation()
        validation = cv.basic_validation(user=user,empty_json=True)
        if not all(validation):
            return validation
        else:
            main = "for creating the income this is how the json should look like"
            second = {"json_example":{
                "amount":"float number of the amount",
                "date_received":"YYYY-MM-DD format",
                "description":"text field of 300 digits allowed",
                "payment_method":"credit_card or cash allowed",
                "costumer_id":"existing customer ID"}}
                
            success_message = OutputMessages.success_with_message(main,second)
            return success_message


    def create(self,cleaned_data,user):
        required_fields = ["amount","date_received","description","payment_method","customer_id"]
    
        cv = CustomValidation()
        validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(validation):
            return validation
        else:
            user_obj = validation[1]["object"]
            company_obj = user_obj.company
    
        #checking if the customer exists
        customer_exists = company_obj.customer_set.filter(customer_id=cleaned_data["customer_id"]).exists()
        if not customer_exists:
            main = "customer not exists"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        
        else:
            customer_obj = company_obj.customer_set.get(customer_id=cleaned_data["customer_id"])


        income_obj = Income.objects.create(
            user=user_obj,
            amount=cleaned_data["amount"],
            date_received=cleaned_data["date_received"],
            description=cleaned_data["description"],
            payment_method=cleaned_data["payment_method"],
            customer=customer_obj,
            company=company_obj
            )
        income_obj.save()

        main = f"created income successfully"
        second = {"income_json":{
            "created_by":user_obj.email,
            "amount":cleaned_data["amount"],
            "date_received":cleaned_data["date_received"],
            "description":cleaned_data["description"],
            "payment_method":cleaned_data["payment_method"],
            "customer_name":customer_obj.name,
            "customer_id":customer_obj.customer_id,
            "payment_id":income_obj.payment_id
        }}
        success_msg = OutputMessages.success_with_message(main,second)
        return success_msg
        


class DeleteIncomeSerializer(serializers.Serializer):
    date_received = serializers.DateField(default=None)
    created_by = serializers.EmailField(default=None)
    customer_name = serializers.CharField(max_length=50,default=None)
    customer_id = serializers.IntegerField(default=None)
    payment_id = serializers.CharField(max_length=80,default=None)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["date_received","created_by","customer_name","customer_id","payment_id"]

        cv = CustomValidation()

        user_exists = User.objects.filter(email=user["email"]).exists()
        if not user_exists:
            main = "this user is not exists"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        else:
            user_obj = User.objects.get(email=user["email"])
            if not user_obj.company:
                main = "user dont have company"
                error_message = OutputMessages.error_with_message(main)
                return error_message
            else:
                company_obj = user_obj.company
            
        valid_fields = cv.passed_valid_fields(input_fields=cleaned_data,valid_fields=allowed_fields)
        if not all(valid_fields):
            return valid_fields
        
        
        # cant_be_passed_together= ["customer_name","customer_id"]
        if "customer_name" in cleaned_data.keys() and "customer_id" in cleaned_data.keys():
            main = "cant pass both the customer name and the customer id."
            error_message = OutputMessages.error_with_message(main)
            return error_message
        
        
        query = Q()
        for key,value in self.__getattribute__("data").items():
            #* checking keys and its values
            if key == "created_by" and value != None:
                required_user_exists = company_obj.user_set.filter(email=value).exists()
                if not required_user_exists:
                    main = "created_by field is invalid"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    created_by_obj = company_obj.user_set.get(email=value)
                    query &= Q(user=created_by_obj)

            if key == "customer_name" and value != None:
                customer_exists_by_name = company_obj.customer_set.filter(name=value).exists()
                if not customer_exists_by_name:
                    main = "customer not exists with the provided name"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    customer_obj = company_obj.customer_set.get(name=value)
                    query &= Q(customer=customer_obj)

            if key == "customer_id" and value != None:
                customer_exists_by_id = company_obj.customer_set.filter(customer_id=value).exists()
                if not customer_exists_by_id:
                    main = "customer not exists with the provided id"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    customer_obj = company_obj.customer_set.get(customer_id=value)
                    query &= Q(customer=customer_obj)
            
            if key == "date_received" and value != None:
                income_exists = company_obj.income_set.filter(date_received=value).exists()
                if not income_exists:
                    main = "income not exists with the provided date_received"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    query &= Q(date_received=value)
               
            if key == "payment_id" and value != None:
                try:
                    income_exists = company_obj.income_set.filter(payment_id=value).exists()
                    if not income_exists:
                        main = "income not exists with the provided payment_id"
                        error_message = OutputMessages.error_with_message(main)
                        return error_message
                    else:
                        query &= Q(payment_id=value)
                except:
                    main = "invalid payment_id field"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
    
        income_exists = company_obj.income_set.filter(query).exists()
        if not income_exists:
            main = "income not exists with the data provided.the data may not be created or you passed invalid fields"
            error_msg = OutputMessages.error_with_message(main)
            return error_msg
        
        else:
            include_fields = ["user__email","date_received","amount","description","payment_method","customer__name","company"]
            income_query_dict = company_obj.income_set.filter(query).values(*include_fields)
            main = "income found successfully"
            second = {"income_json":income_query_dict}
            success_msg = OutputMessages.success_with_message(main,second)
            return success_msg
        
        


    def delete(self,cleaned_data,user):
        required_fields = ["payment_id"]

        cv = CustomValidation()
        validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(validation):
            return validation
        else:
            user_obj = validation[1]["object"]
            company_obj = user_obj.company
        


        #first checking if the income exists
        income_exists = company_obj.income_set.filter(payment_id=cleaned_data["payment_id"]).exists()
        if not income_exists:
            main = "this income is not exists"
            error_msg = OutputMessages.error_with_message(main)
            return error_msg
        else:
            income_obj = company_obj.income_set.get(payment_id=cleaned_data["payment_id"])
            serialized_data = {
                    "user":income_obj.user.email,
                    "amount":income_obj.amount,
                    "date_received":income_obj.date_received,
                    "description":income_obj.description,
                    "payment_method":income_obj.payment_method,
                    "costumer_name":income_obj.customer.name,
                    "costumer_id":income_obj.customer.customer_id,
                    "payment_id":cleaned_data["payment_id"]
                    }
            income_obj.delete()
            main = "deleted_successfully"
            second = {"income_json":serialized_data}
            success_msg = OutputMessages.success_with_message(main,second)
            return success_msg



class UpdateIncomeSerializer(serializers.Serializer):
    date_received = serializers.DateField(default=None)
    created_by = serializers.EmailField(default=None)
    customer_name = serializers.CharField(max_length=50,default=None)
    customer_id = serializers.IntegerField(default=None)
    payment_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default=None)



    def get_info(self,cleaned_data,user):
        allowed_fields = ["date_received","created_by","customer_name","customer_id","payment_id"]
        cv = CustomValidation()

        user_exists = User.objects.filter(email=user["email"]).exists()
        if not user_exists:
            main = "this user is not exists"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        else:
            user_obj = User.objects.get(email=user["email"])
            if not user_obj.company:
                main = "user dont have company"
                error_message = OutputMessages.error_with_message(main)
                return error_message
            else:
                company_obj = user_obj.company
            
        valid_fields = cv.passed_valid_fields(input_fields=cleaned_data,valid_fields=allowed_fields)
        if not all(valid_fields):
            return valid_fields
        
        
        # cant_be_passed_together= ["customer_name","customer_id"]
        if "customer_name" in cleaned_data.keys() and "customer_id" in cleaned_data.keys():
            main = "cant pass both the customer name and the customer id."
            error_message = OutputMessages.error_with_message(main)
            return error_message
        
        
        query = Q()
        for key,value in self.__getattribute__("data").items():
            #* checking keys and its values
            if key == "created_by" and value != None:
                required_user_exists = company_obj.user_set.filter(email=value).exists()
                if not required_user_exists:
                    main = "created_by field is invalid"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    created_by_obj = company_obj.user_set.get(email=value)
                    query &= Q(user=created_by_obj)

            if key == "customer_name" and value != None:
                customer_exists_by_name = company_obj.customer_set.filter(name=value).exists()
                if not customer_exists_by_name:
                    main = "customer not exists with the provided name"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    customer_obj = company_obj.customer_set.get(name=value)
                    query &= Q(customer=customer_obj)

            if key == "customer_id" and value != None:
                customer_exists_by_id = company_obj.customer_set.filter(customer_id=value).exists()
                if not customer_exists_by_id:
                    main = "customer not exists with the provided id"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    customer_obj = company_obj.customer_set.get(customer_id=value)
                    query &= Q(customer=customer_obj)
            
            if key == "date_received" and value != None:
                income_exists = company_obj.income_set.filter(date_received=value).exists()
                if not income_exists:
                    main = "income not exists with the provided date_received"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    query &= Q(date_received=value)
               
            if key == "payment_id" and value != None:
                income_exists = company_obj.income_set.filter(payment_id=value).exists()
                if not income_exists:
                    main = "income not exists with the provided payment_id"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    query &= Q(payment_id=value)
                

        income_exists = company_obj.income_set.filter(query).exists()
        if not income_exists:
            main = "income not exists with the data provided.the data may not be created or you passed invalid fields"
            error_msg = OutputMessages.error_with_message(main)
            return error_msg
        
        else:
            include_fields = ["user__email","date_received","amount","description","payment_method","customer__name","company"]
            income_query_dict = company_obj.income_set.filter(query).values(*include_fields)
            main = "income found successfully"
            second = {"income_json":income_query_dict}
            success_msg = OutputMessages.success_with_message(main,second)
            return success_msg
        
        


    def update(self,cleaned_data,user):
        required_fields = ["payment_id","update_data"]
        allowed_update_fields = ["user","amount","description","payment_method","customer_id"]

        cv = CustomValidation()
        validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(validation):
            return validation
        else:
            user_obj = validation[1]["object"]
            company_obj = user_obj.company


        update_data_validation = cv.passed_valid_fields(input_fields=cleaned_data["update_data"],valid_fields=allowed_update_fields)
        if not all(update_data_validation):
            return update_data_validation
        
        #*checking if income exists
        income_exists = company_obj.income_set.filter(payment_id=cleaned_data["payment_id"]).exists()
        if not income_exists:
            main = "income not exists with the provided payment_id"
            error_msg = OutputMessages.error_with_message(main)
            return error_msg
        else:
            income_obj  = company_obj.income_set.get(payment_id=cleaned_data["payment_id"])

        
        #* this part is passing the update_data dict into another serializer to serialization
        update_data_serializer = GeneralIncomeSerializer(data=cleaned_data["update_data"])

        if update_data_serializer.is_valid():
            update_data = update_data_serializer.fk_check(cleaned_data=cleaned_data["update_data"],company_object=company_obj)

            if not all(update_data):
                main = "error in the update_data field"
                second = {"error":update_data}
                error_msg = OutputMessages.error_with_message(main,second)
                return error_msg
            
            else:
                for keys,values in update_data[1].items():   
                    setattr(income_obj,keys,values)
                    income_obj.save()
                
                updated_income_json = {
                    "user_email":income_obj.user.email,
                    "amount":income_obj.amount,
                    "date_received":income_obj.date_received,
                    "description":income_obj.description,
                    "payment_method":income_obj.payment_method,
                    "customer_id":income_obj.customer.customer_id
                    }
                            
                main = "income updated successfully "
                second = {"income_json":updated_income_json}
                success_msg = OutputMessages.success_with_message(main,second)
                return success_msg

        main = "in update_data one of the fields are invalid"
        error_msg = OutputMessages.error_with_message( main)
        return error_msg



class GetIncomeSerializer(serializers.Serializer):
    date_received = serializers.DateField(default=None)
    created_by = serializers.EmailField(default=None)
    customer_name = serializers.CharField(max_length=50,default=None)
    customer_id = serializers.IntegerField(default=None)
    payment_id = serializers.IntegerField(default=None)


    def get_info(self,cleaned_data,user):
        allowed_fields = ["date_received","created_by","customer_name","customer_id","payment_id"]

        cv = CustomValidation()

        user_exists = User.objects.filter(email=user["email"]).exists()
        if not user_exists:
            main = "this user is not exists"
            error_message = OutputMessages.error_with_message(main)
            return error_message
        else:
            user_obj = User.objects.get(email=user["email"])
            if not user_obj.company:
                main = "user dont have company"
                error_message = OutputMessages.error_with_message(main)
                return error_message
            else:
                company_obj = user_obj.company
            
        valid_fields = cv.passed_valid_fields(input_fields=cleaned_data,valid_fields=allowed_fields)
        if not all(valid_fields):
            return valid_fields
        
        
        # cant_be_passed_together= ["customer_name","customer_id"]
        if "customer_name" in cleaned_data.keys() and "customer_id" in cleaned_data.keys():
            main = "cant pass both the customer name and the customer id."
            error_message = OutputMessages.error_with_message(main)
            return error_message
        
        
        query = Q()
        for key,value in self.__getattribute__("data").items():
            #* checking keys and its values
            if key == "created_by" and value != None:
                required_user_exists = company_obj.user_set.filter(email=value).exists()
                if not required_user_exists:
                    main = "created_by field is invalid"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    created_by_obj = company_obj.user_set.get(email=value)
                    query &= Q(user=created_by_obj)

            if key == "customer_name" and value != None:
                customer_exists_by_name = company_obj.customer_set.filter(name=value).exists()
                if not customer_exists_by_name:
                    main = "customer not exists with the provided name"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    customer_obj = company_obj.customer_set.get(name=value)
                    query &= Q(customer=customer_obj)

            if key == "customer_id" and value != None:
                customer_exists_by_id = company_obj.customer_set.filter(customer_id=value).exists()
                if not customer_exists_by_id:
                    main = "customer not exists with the provided id"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    customer_obj = company_obj.customer_set.get(customer_id=value)
                    query &= Q(customer=customer_obj)
            
            if key == "date_received" and value != None:
                income_exists = company_obj.income_set.filter(date_received=value).exists()
                if not income_exists:
                    main = "income not exists with the provided date_received"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    query &= Q(date_received=value)
               
            if key == "payment_id" and value != None:
                income_exists = company_obj.income_set.filter(payment_id=value).exists()
                if not income_exists:
                    main = "income not exists with the provided payment_id"
                    error_message = OutputMessages.error_with_message(main)
                    return error_message
                else:
                    query &= Q(payment_id=value)
                

        income_exists = company_obj.income_set.filter(query).exists()
        if not income_exists:
            main = "income not exists with the data provided.the data may not be created or you passed invalid fields"
            error_msg = OutputMessages.error_with_message(main)
            return error_msg
        
        else:
            include_fields = ["user__email","date_received","amount","description","payment_method","customer__name","company"]
            income_query_dict = company_obj.income_set.filter(query).values(*include_fields)
            main = "income found successfully"
            second = {"income_json":income_query_dict}
            success_msg = OutputMessages.success_with_message(main,second)
            return success_msg
        
        



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
        allowed_fields = ["outcome_id","update_data","date_time"]
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
            if key == "date_time":
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
            update_data = validation_serializer.fk_check(cleaned_data=cleaned_data)

            #* result of the method might be True,cleaned_data(dict) so its meaning that the user or email are found
            if all(cleaned_data):
                required_id = cleaned_data["outcome_id"]
                #first checking if the income exists
                outcome_exists = Outcome.objects.filter(id=required_id).exists()
                if outcome_exists:
                    update_obj = Outcome.objects.get(id=required_id)

                    #here im getting a copy of the information for representation
                    for keys,values in update_data[1]["update_data"].items():
                        
                        setattr(update_obj,keys,values)
                    
                    update_obj.save()
                    updated_obj_information = {
                            "user_email":update_obj.user.email,
                            "amount":update_obj.amount,
                            "date_time":update_obj.date_time,
                            "description":update_obj.description,
                            "payment_method":update_obj.payment_method,
                            "vendor": update_obj.vendor,
                            "project_or_department": update_obj.project_or_department
                            }
                                
                    message = {"success":{"updated information":updated_obj_information}}
                    return True,message

                
                message = {"error":"outcome not exists"}
                return False,message

            #if user or customer are not found 
            message = {"error":cleaned_data[1]}
            return False,message

        
        message = {"error":"in update_data one of the values are invalid"}
        return False,message


class GetOutcomeSerializer(serializers.Serializer):
    user_email = serializers.EmailField(default=None)
    date_time = serializers.DateField(default=None)


    def get_info(self,cleaned_data):
        """
        getting info by one of the fields 
        """
        allowed_fields = ["date_time","user_email"]


        #checking that the fields are in the allowed list
        for keys in cleaned_data.keys():
            if keys not in allowed_fields:
                message = {"error":"invalid fields passed"}
                return False,message

        if not cleaned_data.items():
            message = {"error":"must pass one of the fields : (date_time,user_email)","json_example":{
                "user_email":"test@test.com",
                "date_time":"2011-11-11"
            }}

            return False,message

        #this will have the query fields that are not None
        query = Q()

        #checking that the user input is not less or more then required fields
        for key,value in self.__getattribute__("data").items():
            
            #* checking that the fields are in the allowed list
            if key not in allowed_fields:
                message = {"error":"invalid key passed"}
                return False,message
            
            #* passing the key,values that are not None into our invalid_fields dict
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

                if key == "date_time":
                    date_time_exists = Outcome.objects.filter(date_time=value).exists()
                    if date_time_exists:
                        query &= Q(date_time=value)

                    else:
                        message = {"error":"data not exists on that date"}
                        return False,message




        #* this is the query with the provided fields
        search_query_exists = Outcome.objects.filter(query).all().annotate(
            user_email=F("user__email")).values("user_email","date_time","category","amount","description","payment_method","vendor").exists()
        
        if search_query_exists:

            search_query = Outcome.objects.filter(query).all().annotate(
            user_email=F("user__email")).values("id","user_email","date_time","category","amount","description","payment_method","vendor")
        
            message = {"data":search_query}
            return True,message

        message={"error":"data not found by provided fields"}
        return False,message
