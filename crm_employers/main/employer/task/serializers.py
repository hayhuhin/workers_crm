from rest_framework import serializers
from employer.models import Employer,Task
from finance.models import Customer
from django.db.models import Q,F


#* general serializers

class GeneralTaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50,default=None)
    description = serializers.CharField(max_length=350,default=None)
    additional_description= serializers.CharField(max_length=350,default=None)
    completed = serializers.BooleanField(default=False)

    #! no need for the check unique in this example 
    #! because we dont have here FK to handle
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



#* task serializers

class CreateTaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50,default=None)
    description = serializers.CharField(max_length=350,default=None)
    additional_description= serializers.CharField(max_length=350,default=None)
    completed = serializers.BooleanField(default=False)

    def get_info(self,cleaned_data,user):
        message = {"success":{"example json":{
            "title":"check emails",
            "description":"each morning i have to check all emails that came from jonh-doe@gmail.com",
            "additional_description":"check engineer teams meetings emails also",
            "completed":"False"
        }}}

        return True,message

    def create(self,cleaned_data,user):
        required_fields = ["title","description","additional_data","completed"]
        for fields in required_fields:
            if fields not in cleaned_data.keys():
                message = {"error":"you must add all required fields","required_fields":required_fields}
                return False,message
            
        #* checking if the user passed empty json
        if not cleaned_data.items():
            message = {"error":"you passed empty json","example_json":{
            "title":"check emails",
            "description":"each morning i have to check all emails that came from jonh-doe@gmail.com",
            "additional_description":"check engineer teams meetings emails also",
            "completed":"False"
        }}
            return False,message


        #* checking that the user that send trying to create the task is already an employer
        employer_exist = Employer.objects.filter(email=user["email"]).exists()
        if employer_exist:
            employer_obj = Employer.objects.get(email=user["email"])
            
        else:
            message = {"error":f"employer not exist with the provided email:{user['email']}"}
            return False,message


        #* assigning each key with its value in our task module
        task_obj = Task()
        for key,value in cleaned_data.items():
            setattr(task_obj,key,value)

        task_obj.save()

        #* now we adding the task object into employers many to many relationship

        employer_obj.task.add(task_obj)
        message = {"success":"created successfully new task ","task_information":{
            "title":task_obj.title,
            "description":task_obj.description,
            "additional_description":task_obj.additional_description,
            "completed":task_obj.completed
        }}
        return True,message


class DeleteTaskSerializer(serializers.Serializer):
    all_tasks = serializers.BooleanField(default=False)
    task_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["task_id","all_tasks"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
            "all_tasks":"True",
            "task_id":1,
        }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"ivalid passed fields","allowed_fields":allowed_fields}
                return False,message
            
        #* checking if the user exists as employer
        employer_exists = Employer.objects.filter(email=user["email"]).exists()
        if employer_exists:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error","employer not exists"}
            return False,message


        #* this section will query the databases and return error if nothing was found
        query = Q()
        # print(self.__getattribute__("data").items())
        for item,item_value in self.__getattribute__("data").items():

            
            #* checking if the email are axists in the task table
            if item == "all_tasks" and item_value == True:
                employer_tasks = employer_obj.task.all().values("id","title","description","additional_description","completed")
                return True,employer_tasks
            
            if item == "task_id" and item_value != None :

                #* first checking if the task exists
                task_exists = Task.objects.filter(id=cleaned_data["task_id"]).exists()
                if task_exists:
                    task_obj = Task.objects.get(id=cleaned_data["task_id"])
                    employer_relation_exists = employer_obj.task.filter(id=task_obj.id).exists()
                    if employer_relation_exists:
                        query &= Q(id=cleaned_data["task_id"])
                    else:
                        message = {"error":"not data about tasks with this employer"}
                        return False,message
                else:
                    message = {"error":"this task not exists"}
                    return False,message
                

        query_exists = Task.objects.filter(query).exists()
        if query_exists:
            task_data= Task.objects.filter(query).values("id","title","description")
            message = {"success":task_data}
            return True,message
        message = {"error":"all fields that was added are not found togheter","asumptions":"try to remove some of the fields and search again"}
        return False,message

    def delete(self,cleaned_data,user):
        required_fields = ["task_id"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
                "task_id":"if known the id you can search by the id as get method"
            }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in required_fields:
                message = {"error":"passed invalid fields","required fields are":{
                    "task_id":"integer of the required to delete id"
                }}
                return False,message
            

        #* checking if the user is an existing employer
        employer_exists = Employer.objects.filter(email=user["email"]).exists()
        if employer_exists:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"this user is not exists as employer"}
            return False,message


        #* checking if the id exists in the database and user have relationship to this id

        task_exists = Task.objects.filter(id=cleaned_data["task_id"]).exists()
        if task_exists:
            task_obj = Task.objects.get(id=cleaned_data["task_id"])
            employer_relation_exists = employer_obj.task.filter(id=task_obj.id).exists()

            #* only if have relation and user as employer it deletes the task
            if employer_relation_exists:
                delete_obj = Task.objects.get(id=cleaned_data["task_id"])
                delete_obj.delete()
                message = {"success":"deleted the required task successfully"}
                return False,message

            message = {"error":"this employer doesnt have task with the provided id"}
            return False,message
    
        message = {"error":"task not found by the provided id"}
        return False,message


class UpdateTaskSerializer(serializers.Serializer):
    all_tasks = serializers.BooleanField(default=False)
    task_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default=None)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["task_id","all_tasks"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
            "all_tasks":"True",
            "task_id":1,
        }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"ivalid passed fields","allowed_fields":allowed_fields}
                return False,message
            
        #* checking if the user exists as employer
        employer_exists = Employer.objects.filter(email=user["email"]).exists()
        if employer_exists:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error","employer not exists"}
            return False,message


        #* this section will query the databases and return error if nothing was found
        query = Q()
        # print(self.__getattribute__("data").items())
        for item,item_value in self.__getattribute__("data").items():

            
            #* checking if the email are axists in the task table
            if item == "all_tasks" and item_value == True:
                employer_tasks = employer_obj.task.all().values("id","title","description","additional_description","completed")
                return True,employer_tasks
            
            if item == "task_id" and item_value != None :

                #* first checking if the task exists
                task_exists = Task.objects.filter(id=cleaned_data["task_id"]).exists()
                if task_exists:
                    task_obj = Task.objects.get(id=cleaned_data["task_id"])
                    employer_relation_exists = employer_obj.task.filter(id=task_obj.id).exists()
                    if employer_relation_exists:
                        query &= Q(id=cleaned_data["task_id"])
                    else:
                        message = {"error":"not data about tasks with this employer"}
                        return False,message
                else:
                    message = {"error":"this task not exists"}
                    return False,message
                

        query_exists = Task.objects.filter(query).exists()
        if query_exists:
            task_data= Task.objects.filter(query).values("id","title","description")
            message = {"success":task_data}
            return True,message
        message = {"error":"all fields that was added are not found togheter","asumptions":"try to remove some of the fields and search again"}
        return False,message


    def update(self,cleaned_data,user):
        required_fields = ["task_id","update_data"]
        allowed_update_fields = ["title","description","additional_data","completed"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass all this fields","example_json":{
                "task_id":"id of the task as integer",
                "update_data":{
                    "title":"example title",
                    "description":"example description",
                    "additional_data":"example additional data",
                    "completed":"False",
                    }}}
            
            return False,message
        
        #*checking that the user passed all fields
        for field in required_fields:
            if field not in cleaned_data.keys():
                message = {"error":"you must pass all fields","json_example":{
                "task_id":"id of the task as integer",
                "update_data":{
                    "title":"example title",
                    "description":"example description",
                    "additional_data":"example additional data",
                    "completed":"False",
                    },
                    "and you passed":cleaned_data.items()
                    }}
            
                return False,message

        #* checking that the user didnt pass additional fields and only the allowed in the update data
        for field in cleaned_data["update_data"].keys():
            if field not in allowed_update_fields:
                message = {"error":"passed invalid fields into the update_data json","json example of update_data":{
                "task_id":"id of the task as integer",
                "update_data":{
                    "title":"example title",
                    "description":"example description",
                    "additional_data":"example additional data",
                    "completed":"False",
                    }}}
                return False,message


        #* checking if the user is an existing employer
        employer_exists = Employer.objects.filter(email=user["email"]).exists()
        if employer_exists:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error":"this user is not exists as employer"}
            return False,message


        #* checking if the id exists in the database and user have relationship to this id
        task_exists = Task.objects.filter(id=cleaned_data["task_id"]).exists()
        if task_exists:
            task_obj = Task.objects.get(id=cleaned_data["task_id"])
            employer_relation_exists = employer_obj.task.filter(id=task_obj.id).exists()

            #* only if have relation and user as employer it creates the update_obj of the task
            if not employer_relation_exists:
                message = {"error":"this employer doesnt have task with the provided id"}
                return False,message
        else:
            message = {"error":"task not found by the provided id"}
            return False,message



        #* checking that the user didnt pass empty update data dict
        if not cleaned_data["update_data"]:
            message = {"error":"you cant pass empty udpate_data ","json_example for updata_data":{
                "task_id":"id of the task as integer",
                "update_data":{
                    "title":"example title",
                    "description":"example description",
                    "additional_data":"example additional data",
                    "completed":"False",
                    }}}
            return False,message
        


        #*serializing update_data fields in another serializer
        update_data_serializer = GeneralTaskSerializer(data=cleaned_data["update_data"])
        if update_data_serializer.is_valid(raise_exception=True):
            update_obj = Task.objects.get(id=cleaned_data["task_id"])
            for key,value in cleaned_data["update_data"].items():
                setattr(update_obj,key,value)
                

                update_obj.save()
            message = {"success":"updated the required fields","updated_data":{
                "title":update_obj.title,
                "description":update_obj.description,
                "additional_description":update_obj.additional_description,
                "completed":update_obj.completed,
                }}
            return True,message

        message = {"error":"invalid update_data fields"}
        return False,message


class GetTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(default = None)
    all_tasks = serializers.BooleanField(default=False)

    def get_info(self,cleaned_data,user):
        allowed_fields = ["task_id","all_tasks"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
            "all_tasks":"True",
            "task_id":1,
        }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"ivalid passed fields","allowed_fields":allowed_fields}
                return False,message
            
        #* checking if the user exists as employer
        employer_exists = Employer.objects.filter(email=user["email"]).exists()
        if employer_exists:
            employer_obj = Employer.objects.get(email=user["email"])
        else:
            message = {"error","employer not exists"}
            return False,message


        #* this section will query the databases and return error if nothing was found
        query = Q()
        # print(self.__getattribute__("data").items())
        for item,item_value in self.__getattribute__("data").items():

            
            #* checking if the email are axists in the task table
            if item == "all_tasks" and item_value == True:
                employer_tasks = employer_obj.task.all().values("id","title","description","additional_description","completed")
                return True,employer_tasks
            
            if item == "task_id" and item_value != None :

                #* first checking if the task exists
                task_exists = Task.objects.filter(id=cleaned_data["task_id"]).exists()
                if task_exists:
                    task_obj = Task.objects.get(id=cleaned_data["task_id"])
                    employer_relation_exists = employer_obj.task.filter(id=task_obj.id).exists()
                    if employer_relation_exists:
                        query &= Q(id=cleaned_data["task_id"])
                    else:
                        message = {"error":"not data about tasks with this employer"}
                        return False,message
                else:
                    message = {"error":"this task not exists"}
                    return False,message
                

        query_exists = Task.objects.filter(query).exists()
        if query_exists:
            task_data= Task.objects.filter(query).values("id","title","description")
            message = {"success":task_data}
            return True,message
        message = {"error":"all fields that was added are not found togheter","asumptions":"try to remove some of the fields and search again"}
        return False,message

