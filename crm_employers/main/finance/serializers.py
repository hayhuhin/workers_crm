from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from .models import Income,Outcome
from user.models import User

#!need to add an doption to pass email and then search for this worker first


class CreateIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"

    def create(self,cleaned_data):
        income_obj = Income.objects.create(
            user=cleaned_data["user"],
            amount=cleaned_data["amount"],
            date_received=cleaned_data["date_received"],
            description=cleaned_data["description"],
            payment_method=cleaned_data["payment_method"],
            customer=cleaned_data["customer"]
            )
        income_obj.save()
        message = {"success":f"created income by {income_obj.user} by the payment method {income_obj.payment_method}"}
        return True,message
    

class DeleteIncomeSerializer(serializers.Serializer):
    date_recieved = serializers.DateField()
    income_id = serializers.IntegerField(default=None)

    def get(self,cleaned_data):
        #required date from cleaned_data
        required_date = cleaned_data["date_received"]
        #first checking if the income exists
        income_exists = Income.objects.filter(date_recieved=required_date).exists()
        if income_exists:
            income_dict = {}
            income_list = Income.objects.get(date_received=required_date).all()
            for income in income_list:
                income_dict[income.date_recieved] = {
                    "user":income.user,
                    "amount":income.amount,
                    "date_received":income.date_received,
                    "description":income.description,
                    "payment_method":income.payment_methodm,
                    "costumer":income.costumer,
                    "id":income.id
                    }
                
            message = {"success":{"income":income_dict}}
            return True,message
        
        return False,{"error":"income not exists"}



    def delete(self,cleaned_data):
        required_fields = ["date_received","income_id"]
        
        required_date = cleaned_data["date_received"]
        required_id = cleaned_data["income_id"]

        #first checking if the income exists
        income_exists = Income.objects.filter(id=required_id).exists()
        if income_exists:
            delete_obj = Income.objects.get(id=required_id)

            #here im getting a copy of the information for representation
            delete_obj_information = {
                    "user":delete_obj.user,
                    "amount":delete_obj.amount,
                    "date_received":delete_obj.date_received,
                    "description":delete_obj.description,
                    "payment_method":delete_obj.payment_methodm,
                    "costumer":delete_obj.costumer,
                    }
            

            message = {"success":{"deleted information":delete_obj_information}}
            delete_obj.delete()
            return True,message


        message = {"error":"income not exists"}
        return False,


class UpdateIncomeSerializer(serializers.Serializer):
    required_date = serializers.DateField()
    required_id = serializers.IntegerField(default=None)
    update_fields = serializers.DictField(default=None)

    def get(self,cleaned_data):
        #required date from cleaned_data
        required_id = cleaned_data["required_id"]
        required_date = cleaned_data["required_date"]
        #first checking if the income exists
        income_exists = Income.objects.filter(date_received=required_date).exists()
        if income_exists:
            income_dict = {}
            income_list = Income.objects.get(date_received=required_date).all()
            for income in income_list:
                income_dict[income.date_recieved] = {
                    "user":income.user,
                    "amount":income.amount,
                    "date_recieved":income.date_received,
                    "description":income.description,
                    "payment_method":income.payment_methodm,
                    "costumer":income.costumer,
                    "id":income.id
                    }
                
            message = {"success":{"income":income_dict}}
            return True,message
        
        return False,{"error":"income not exists"}



    def update(self,cleaned_data):
        allowed_fields = ["user","amount","description","payment_method","costumer","date_recieved"]
        
        #checkin that all of this fields are provided in the cleaned_data
        try:
            required_date = cleaned_data["date_recieved"]
            required_id = cleaned_data["income_id"]
            update_fields = cleaned_data["update_fields"]
        except:
            message = {"error":"you must provide : required_date,required_id,update_fields"}
            return False,message


        #first checking if the income exists
        income_exists = Income.objects.filter(id=required_id).exists()
        if income_exists:
            update_obj = Income.objects.get(id=required_id)

            #here im getting a copy of the information for representation
            for key,value in update_obj.items():
                if key not in allowed_fields:
                    message = {"error":"cant change this field"}
                    return False,message
                
                getattr(update_obj,key,value)
            
            update_obj.save()
            updated_obj_information = {
                    "user":update_obj.user,
                    "amount":update_obj.amount,
                    "date_recieved":update_obj.date_received,
                    "description":update_obj.description,
                    "payment_method":update_obj.payment_methodm,
                    "costumer":update_obj.costumer,
                    }
                        
            message = {"success":{"updated information":updated_obj_information}}
            return True,message


        message = {"error":"income not exists"}
        return False,






class GetIncomeSerializer(serializers.Serializer):
    pass



class CreateOutcomeSerializer(serializers.Serializer):
    pass


class DeleteOutcomeSerializer(serializers.Serializer):
    pass


class UpdateOutcomeSerializer(serializers.Serializer):
    pass


class GetOutcomeSerializer(serializers.Serializer):
    pass

