from rest_framework import serializers
from employer.models import Employer,Lead
from finance.models import Customer


class CreateLeadSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100,default=None)
    last_name = serializers.CharField(max_length=100,default=None)
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(max_length=20,default = None)
    customer_id = serializers.IntegerField(default=None)
    status = serializers.ChoiceField(choices=[
            ('new', 'New'),
            ('contacted', 'Contacted'),
            ('qualified', 'Qualified'),
            ('lost', 'Lost'),
            ('converted', 'Converted'),
        ], default='new')
    source = serializers.CharField(max_length=100,default=None)
    notes = serializers.CharField(max_length=350,default=None)
    assigned_to = serializers.EmailField(default=None)


    def get_info(self,cleaned_data):
        message = {"success":{"example json":{
            "first_name":"john",
            "last_name":"doe",
            "email":"john_doe@electric.com",
            "phone_number":"112233",
            "customer_id":123456789,
            "status":"choose one of these: new,contacted,qulified,lost,converted",
            "source":"Source from which the lead was acquired (optional, e.g., website, referral, cold call)",
            "notes":"notes text",
            "assigned_to":"employee email who assigned to the lead"
        }}}

        return True,message

    def create(self,cleaned_data):
        required_fields = ["first_name","last_name","email","phone_number","customer_id","status","source","notes","assigned_to"]
        for fields in required_fields:
            if fields not in cleaned_data.keys():
                message = {"error":"you must add all required fields","required_fields":required_fields}
                return False,message
            
        #* checkinf if the user passed empty json
        if not cleaned_data.items():
            message = {"error":"you passed empty json","example_json":{
            "first_name":"john",
            "last_name":"doe",
            "email":"john_doe@electric.com",
            "phone_number":"112233",
            "customer_id":123456789,
            "status":"choose one of these: new,contacted,qulified,lost,converted",
            "source":"Source from which the lead was acquired (optional, e.g., website, referral, cold call)",
            "notes":"notes text",
            "assigned_to":"employee email who assigned to the lead"}}
            return False,message


        #* checking that the customer exist with the provided id
        customer_exist = Customer.objects.filter(customer_id=cleaned_data["customer_id"]).exists()
        if customer_exist:
            customer_obj = Customer.objects.get(customer_id=cleaned_data["customer_id"])
            
            #*removing the customer_id and adding the customer object
            cleaned_data.pop("customer_id")
            cleaned_data["company"] = customer_obj
        else:
            message = {"error":"this customer not exist with the provided customer_id"}
            return False,message

        #*checking if the assigned worker is exists
        employer_exist = Employer.objects.filter(email=cleaned_data["assigned_to"]).exists()
        if employer_exist:
            employer_obj = Employer.objects.filter(email=cleaned_data["assigned_to"])

            #*changing assigned_to from email to employer object
            cleaned_data["assigned_to"] = employer_obj
            
        else:
            message = {"error":"employer not exist with the provied email"}
            return False,message


        #* assigning each key with its value in our lead module
        lead_obj = Lead()
        for key,value in cleaned_data.items():
            setattr(lead_obj,key,value)

        lead_obj.save()

        lead_id = lead_obj.id
        lead_repr = Lead.object.filter(id=lead_id).value()
        message = {"success":"created successfully new lead ","lead_information":lead_repr}
        return True,message


class DeleteLeadSerializer(serializers.Serializer):
    pass

class UpdateLeadSerializer(serializers.Serializer):
    pass

class GetLeadSerializer(serializers.Serializer):
    pass