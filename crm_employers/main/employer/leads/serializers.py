from rest_framework import serializers
from employer.models import Employer,Lead
from finance.models import Customer
from django.db.models import Q,F


#* general serializers

class GeneralLeadSerializer(serializers.Serializer):
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


    def check_unique(self,cleaned_data):
        """
        this method will check if there is already existing data with the same id.

        unique fields are customer_id,email
        """

        if "customer_id" in cleaned_data.keys():
            cleaned_data["company"] = cleaned_data["customer_id"]
            cleaned_data.pop("customer_id")

        for key in cleaned_data.keys():
            #* checking if the customer exists
            if key == "company":
                customer_exists = Customer.objects.filter(customer_id=cleaned_data["company"]).exists()
                if customer_exists:
                    #* this removes the customer id and will be added company object
                    company_obj = Customer.objects.get(customer_id=cleaned_data["company"])
                    cleaned_data["company"] = company_obj

                else:
                    message = {"error":"this compnay id not exists"}
                    return False,message

            if key == "assigned_to":
                assigned_to_exists = Employer.objects.filter(email=cleaned_data["assigned_to"]).exists()
                if assigned_to_exists:
                    #* this removes the assigned to email and changes it to the assigned to object
                    assigned_to_obj = Employer.objects.get(email=cleaned_data["assigned_to"])
                    cleaned_data["assigned_to"] = assigned_to_obj
                   
                else:
                    message = {"error","this employer not exists with the provided email"}
                    return False,message

        # #* removing the unecesery data to make clean cleaned_data
        # unnecesery_data = ["customer_id"]
        # for data in unnecesery_data:
        #     if data in  cleaned_data.keys():
        #         cleaned_data.pop(data)


        #* returning cleaned data with the objects inside that can be used to update the database
        return True,cleaned_data




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
            employer_obj = Employer.objects.get(email=cleaned_data["assigned_to"])

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
        lead_repr = Lead.objects.filter(id=lead_id).values()
        message = {"success":"created successfully new lead ","lead_information":lead_repr}
        return True,message


class DeleteLeadSerializer(serializers.Serializer):
    client_email = serializers.EmailField(default = None)
    assigned_to_email = serializers.EmailField(default=None)
    lead_id = serializers.IntegerField(default = None)

    def get_info(self,cleaned_data):
        allowed_fields = ["client_email","assigned_to_email","lead_id"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
                "client_email":"email of the client that was registered when adding lead",
                "assigned_to_email":"email of the assigned employee",
                "lead_id":"if known the id you can search by the id"
            }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"ivalid passed fields","allowed_fields":allowed_fields}
                return False,message
            

        #* this section will query the databases and return error if nothing was found
            
        query = Q()
        # print(self.__getattribute__("data").items())
        for item,item_value in self.__getattribute__("data").items():

            
            #* checking if the email are axists in the lead table
            if item == "client_email" and item_value != None:
                data_exists = Lead.objects.filter(email=cleaned_data["client_email"]).exists()
                if data_exists:
                    query &= Q(email=cleaned_data["client_email"])
                else:
                    message = {"error":"invalid email passed"}
                    return False,message
            
            if item == "assigned_to_email" and item_value != None :

                #* first checking if the user exists
                employer_exists = Employer.objects.filter(email=cleaned_data["assigned_to_email"])
                if employer_exists:
                    employer_obj = Employer.objects.get(email=cleaned_data["assigned_to_email"])
                    data_exists = Lead.objects.filter(assigned_to=employer_obj).exists()
                    if data_exists:
                        query &= Q(assigned_to=employer_obj)
                    else:
                        message = {"error":"not data about leads with this employer"}
                        return False,message
                else:
                    message = {"error":"this employer not exists"}
                    return False,message
                
            if item == "lead_id" and item_value != None:
                lead_id_exists = Lead.objects.filter(id=cleaned_data["lead_id"]).exists()
                if lead_id_exists:
                    query &= Q(id=cleaned_data["lead_id"])
                else:
                    message = {"error":"no leads found with this id"}
                    return False,message
                


        query_exists = Lead.objects.filter(query).exists()
        if query_exists:
            lead_data= Lead.objects.filter(query).values("id","first_name","last_name","company__email","assigned_to__email","created_at")
            message = {"success":lead_data}
            return True,message
        message = {"error":"all fields that was added are not found togheter","asumptions":"try to remove some of the fields and search again"}
        return False,message

    def delete(self,cleaned_data):
        required_fields = ["lead_id"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
                "lead_id":"if known the id you can search by the id as get method"
            }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in required_fields:
                message = {"error":"passed invalid fields","required fields are":{
                    "lead_id":"integer of the required to delete id"
                }}
                return False,message
            
        #* checking if the id exists in the database
        lead_id_exists = Lead.objects.filter(id=cleaned_data["lead_id"]).exists()
        if lead_id_exists:
            delete_obj = Lead.objects.get(id=cleaned_data["lead_id"])
            delete_obj.delete()
            message = {"success":"deleted the required lead successfully"}
            return False,message
        

        message = {"error":"lead not found by the provided id"}
        return False,message


class UpdateLeadSerializer(serializers.Serializer):
    customer_email = serializers.EmailField(default=None)
    assigned_to_email = serializers.EmailField(default=None)
    lead_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default=None)

    def get_info(self,cleaned_data):
        allowed_fields = ["customer_email","assigned_to_email","lead_id"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass at least one of the fields","example_json":{
                "customer_email":"customer@customer.com",
                "assigned_to_email":"sales@valar.com",
                "lead_id":112233
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
            if key == "customer_email" and value != None:
                email_exists = Lead.objects.filter(email=value).exists()
                if email_exists: 
                    query &= Q(email=value)
                else:
                    message = {"error":"email not exist. try another field or check if you miss typed"}
                    return False,message
                
            if key == "assigned_to_email" and value != None:
                assigned_to_exists = Lead.objects.filter(assigned_to__email=value).exists()
                if assigned_to_exists:
                    query &= Q(assigned_to__email=value)
                else:
                    message = {"error":"employer with this email not exist. try another field or check if you miss typed"}
                    return False,message

            if key == "lead_id" and value != None:
                lead_id_exists = Lead.objects.filter(id=value).exists()
                if lead_id_exists:
                    query &= Q(id=value)
                else:
                    message = {"error":"lead not exist with this id. try another field or check if you miss typed"}
                    return False,message
        

        query_data = Lead.objects.filter(query).values("id","first_name","last_name","company__email","assigned_to__email","created_at")
        message = {"success":query_data}
        return True,message


    def update(self,cleaned_data):
        required_fields = ["lead_id","update_data"]
        allowed_update_fields = ["first_name","last_name","email","phone_number","customer_id","status","source","notes","assigned_to"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass all this fields","example_json":{
                "lead_id":"id of the lead as integer",
                "update_data":{
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
            
            return False,message
        
        #*checking that the user passed all fields
        for field in required_fields:
            if field not in cleaned_data.keys():
                message = {"error":"you must pass all fields","json_example":{
                "lead_id":"id of the lead as integer",
                "update_data":{
                    "first_name":"john",
                    "last_name":"doe",
                    "email":"john_doe@electric.com",
                    "phone_number":"112233",
                    "customer_id":123456789,
                    "status":"choose one of these: new,contacted,qulified,lost,converted",
                    "source":"Source from which the lead was acquired (optional, e.g., website, referral, cold call)",
                    "notes":"notes text",
                    "assigned_to":"employee email who assigned to the lead"
                    },
                    "and you passed":cleaned_data.items()
                    }}
            
                return False,message

        #* checking that the user didnt pass additional fields and only the allowed in the update data
        for field in cleaned_data["update_data"].keys():
            if field not in allowed_update_fields:
                message = {"error":"passed invalid fields into the update_data json","json example of update_data":{
                    "first_name":"john",
                    "last_name":"doe",
                    "email":"john_doe@electric.com",
                    "phone_number":"112233",
                    "customer_id":123456789,
                    "status":"choose one of these: new,contacted,qulified,lost,converted",
                    "source":"Source from which the lead was acquired (optional, e.g., website, referral, cold call)",
                    "notes":"notes text",
                    "assigned_to":"employee email who assigned to the lead"
                    }}
                return False,message


        # #*checking if the lead exists with the id provided
        lead_exists = Lead.objects.filter(id = cleaned_data["lead_id"]).exists()
        if not lead_exists:
            message = {"error":"this lead is not exist with this id"}
            return False,message



        #* checking that the user didnt pass empty update data dict
        if not cleaned_data["update_data"]:
            message = {"error":"you cant pass empty udpate_data ","json_example for updata_data":{
                    "first_name":"john",
                    "last_name":"doe",
                    "email":"john_doe@electric.com",
                    "phone_number":"112233",
                    "customer_id":123456789,
                    "status":"choose one of these: new,contacted,qulified,lost,converted",
                    "source":"Source from which the lead was acquired (optional, e.g., website, referral, cold call)",
                    "notes":"notes text",
                    "assigned_to":"employee email who assigned to the lead"
                    }}
            return False,message
        


        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralLeadSerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=True):

            check_unique_fields = update_data_serializer.check_unique(cleaned_data=cleaned_data["update_data"])
            if all(check_unique_fields):
                update_obj = Lead.objects.get(id=cleaned_data["lead_id"])

                update_data = check_unique_fields[1]

                for key,value in update_data.items():
                    setattr(update_obj,key,value)

                update_obj.save()
                message = {"success":"updated the required fields","updated_data":{
                    "first_name":update_obj.first_name,
                    "last_name":update_obj.last_name,
                    "email":update_obj.email,
                    "phone_number":update_obj.phone_number,
                    "customer_id":update_obj.company.customer_id,
                    "status":update_obj.status,
                    "source":update_obj.source,
                    "notes":update_obj.notes,
                    "assigned_to":update_obj.assigned_to.email
                }}
                return True,message
            
            return False,check_unique_fields[1]

        message = {"error":"invalid update_data fields"}
        return False,message



class GetLeadSerializer(serializers.Serializer):
    client_email = serializers.EmailField(default = None)
    assigned_to_email = serializers.EmailField(default=None)
    lead_id = serializers.IntegerField(default = None)

    def get_info(self,cleaned_data):
        allowed_fields = ["client_email","assigned_to_email","lead_id"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
                "client_email":"email of the client that was registered when adding lead",
                "assigned_to_email":"email of the assigned employee",
                "lead_id":"if known the id you can search by the id"
            }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"ivalid passed fields","allowed_fields":allowed_fields}
                return False,message
            

        #* this section will query the databases and return error if nothing was found
            
        query = Q()
        # print(self.__getattribute__("data").items())
        for item,item_value in self.__getattribute__("data").items():

            
            #* checking if the email are axists in the lead table
            if item == "client_email" and item_value != None:
                data_exists = Lead.objects.filter(email=cleaned_data["client_email"]).exists()
                if data_exists:
                    query &= Q(email=cleaned_data["client_email"])
                else:
                    message = {"error":"invalid email passed"}
                    return False,message
            
            if item == "assigned_to_email" and item_value != None :

                #* first checking if the user exists
                employer_exists = Employer.objects.filter(email=cleaned_data["assigned_to_email"])
                if employer_exists:
                    employer_obj = Employer.objects.get(email=cleaned_data["assigned_to_email"])
                    data_exists = Lead.objects.filter(assigned_to=employer_obj).exists()
                    if data_exists:
                        query &= Q(assigned_to=employer_obj)
                    else:
                        message = {"error":"not data about leads with this employer"}
                        return False,message
                else:
                    message = {"error":"this employer not exists"}
                    return False,message
                
            if item == "lead_id" and item_value != None:
                lead_id_exists = Lead.objects.filter(id=cleaned_data["lead_id"]).exists()
                if lead_id_exists:
                    query &= Q(id=cleaned_data["lead_id"])
                else:
                    message = {"error":"no leads found with this id"}
                    return False,message
                


        query_exists = Lead.objects.filter(query).exists()
        if query_exists:
            lead_data= Lead.objects.filter(query).values("id","first_name","last_name","company__email","assigned_to__email","created_at")
            message = {"success":lead_data}
            return True,message
        message = {"error":"all fields that was added are not found togheter","asumptions":"try to remove some of the fields and search again"}
        return False,message
