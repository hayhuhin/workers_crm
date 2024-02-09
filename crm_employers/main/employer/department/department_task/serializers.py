from rest_framework import serializers
from employer.models import Employer,Department,DepartmentTask
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
    department_id = serializers.CharField(max_length=50,default=None)


    def get_info(self,cleaned_data):
        message = {"success":{"example json":{
            "title":"check emails",
            "description":"each morning i have to check all emails that came from jonh-doe@gmail.com",
            "additional_description":"check engineer teams meetings emails also",
            "completed":"False",
            "department_id":3
        }}}

        return True,message

    def create(self,cleaned_data):
        required_fields = ["title","description","additional_data","completed","department_id"]
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


        #* checking that the department is existing
        department_exist = Department.objects.filter(id=cleaned_data["department_id"]).exists()
        if department_exist:
            department_obj = Department.objects.get(id=cleaned_data["department_id"])
            
        else:
            message = {"error":f"department not exist with the provided id:{cleaned_data['department_id']}"}
            return False,message


        #* assigning each key with its value in our task module
        task_obj = DepartmentTask()
        for key,value in cleaned_data.items():
            setattr(task_obj,key,value)

        task_obj.save()

        #* now we adding the task object into department many to many relationship

        department_obj.task.add(task_obj)
        message = {"success":"created successfully new task ","task_information":{
            "title":task_obj.title,
            "description":task_obj.description,
            "additional_description":task_obj.additional_description,
            "completed":task_obj.completed
        }}
        return True,message


class DeleteTaskSerializer(serializers.Serializer):
    department_name = serializers.CharField(max_length=50,default=None)
    task_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data):
        allowed_fields = ["task_id","department_name"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
            "department_name":"engineer",
            "task_id":1,
        }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"ivalid passed fields","allowed_fields":allowed_fields}
                return False,message
            
        # #* checking if the department is exists
        # department_exists = Department.objects.filter(name=cleaned_data["department_name"]).exists()
        # if department_exists:
        #     deparment_obj = Department.objects.get(name=cleaned_data["department_name"])
        # else:
        #     message = {"error","employer not exists"}
        #     return False,message


        #* this section will query the databases and return error if nothing was found
        query = Q()
        # print(self.__getattribute__("data").items())
        for item,item_value in self.__getattribute__("data").items():

            
            #* checking if the email are axists in the task table
            if item == "department_name" and item_value == True:
                department_task_exists = Department.objects.exists(name=cleaned_data["department_name"]).exists()
                if department_task_exists:
                    department_task_obj = Department.objects.get(name=cleaned_data["name"])
                    task_data = department_task_obj.task.all().values("id","title")
                    message = {"success":"department tasks found","department_tasks":task_data}
                    
                    return False,message
                else:
                    message = {"error":"invalid department name provided"}


            if item == "task_id" and item_value != None :

                #* first checking if the task exists
                task_exists = DepartmentTask.objects.filter(id=cleaned_data["task_id"]).exists()
                if task_exists:
                    task_obj = DepartmentTask.objects.get(id=cleaned_data["task_id"])
                    department_relation_exists = Department.task.filter(id=task_obj.id).exists()
                    if department_relation_exists:
                        query &= Q(id=cleaned_data["task_id"])
                    else:
                        message = {"error":"not data about tasks with this department"}
                        return False,message
                else:
                    message = {"error":"this task not exists"}
                    return False,message
                

        query_exists = DepartmentTask.objects.filter(query).exists()
        if query_exists:
            task_data= DepartmentTask.objects.filter(query).values("id","title","description")
            message = {"success":task_data}
            return True,message
        message = {"error":"all fields that was added are not found togheter","asumptions":"try to remove some of the fields and search again"}
        return False,message

    def delete(self,cleaned_data):
        required_fields = ["task_id","department_name"]

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
            

        # #* checking if department exists
        # employer_exists = Employer.objects.filter(email=user["email"]).exists()
        # if employer_exists:
        #     employer_obj = Employer.objects.get(email=user["email"])
        # else:
        #     message = {"error":"this user is not exists as employer"}
        #     return False,message


        #* checking if the id exists in the database and user have relationship to this id

        task_exists = DepartmentTask.objects.filter(id=cleaned_data["task_id"]).exists()
        if task_exists:
            delete_obj = DepartmentTask.objects.get(id=cleaned_data["task_id"])
            delete_obj.delete()
            message = {"success":"deleted the required department task successfully"}
            return False,message
    
        message = {"error":"task not found by the provided id"}
        return False,message




class UpdateTaskSerializer(serializers.Serializer):
    department_id = serializers.IntegerField(default=None)
    task_id = serializers.IntegerField(default=None)
    update_data = serializers.DictField(default=None)

    def get_info(self,cleaned_data):
        allowed_fields = ["task_id","department_id"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
            "department_id":1,
            "task_id":1,
        }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"ivalid passed fields","allowed_fields":allowed_fields}
                return False,message
            
        # #* checking if the department is exists
        department_exists = Department.objects.filter(id=cleaned_data["department_id"]).exists()
        if department_exists:
            department_obj = Department.objects.get(id=cleaned_data["department_id"])
        else:
            message = {"error","department not exists"}
            return False,message


        #* this section will query the databases and return error if nothing was found
        query = Q()
        # print(self.__getattribute__("data").items())
        for item,item_value in self.__getattribute__("data").items():

            
            #* checking if the email are axists in the task table
            if item == "department_id" and item_value == True:
                department_task_exists = Department.objects.exists(id=cleaned_data["department_id"]).exists()
                if department_task_exists:
                    task_data = department_obj.task.all().values("id","title")
                    message = {"success":"department tasks found","department_tasks":task_data}
                    return False,message
                
                else:
                    message = {"error":"invalid department name provided"}


            if item == "task_id" and item_value != None :

                #* first checking if the task exists
                task_exists = DepartmentTask.objects.filter(id=cleaned_data["task_id"]).exists()
                if task_exists:
                    task_obj = DepartmentTask.objects.get(id=cleaned_data["task_id"])
                    department_relation_exists = Department.task.filter(id=task_obj.id).exists()
                    if department_relation_exists:
                        query &= Q(id=cleaned_data["task_id"])
                    else:
                        message = {"error":"not data about tasks with this department"}

                        return False,message
                else:
                    message = {"error":"this task not exists"}
                    return False,message
                

        query_exists = DepartmentTask.objects.filter(query).exists()
        if query_exists:
            task_data= DepartmentTask.objects.filter(query).values("id","title","description")
            message = {"success":task_data}
            return True,message
        message = {"error":"all fields that was added are not found togheter","asumptions":"try to remove some of the fields and search again"}
        return False,message


    def update(self,cleaned_data):
        required_fields = ["department_id","task_id","update_data"]
        allowed_update_fields = ["title","description","additional_data","completed"]

        #* returning example json if the user passed empty json
        if not cleaned_data.keys():
            message = {"error":"you must pass all this fields","example_json":{
                "department_id":1,
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
                "department_id":1,
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
                    "title":"example title",
                    "description":"example description",
                    "additional_data":"example additional data",
                    "completed":"False",
                    }}
                return False,message


        #* checking if the department is exists
        department_exists = Department.objects.filter(id=cleaned_data["department_id"]).exists()
        if department_exists:
            department_obj = Department.objects.get(id=cleaned_data["department_id"])
        else:
            message = {"error":"this department not exists with the id provided"}
            return False,message


        #* checking if the id exists in the database and user have relationship to this id
        task_exists = DepartmentTask.objects.filter(id=cleaned_data["task_id"]).exists()
        if task_exists:
            task_obj = DepartmentTask.objects.get(id=cleaned_data["task_id"])
            department_relation_exists = department_obj.task.filter(id=task_obj.id).exists()
            #* only if have relation between department and the task
            if not department_relation_exists:
                message = {"error":"this department doesnt have task with the provided id"}
                return False,message
        else:
            message = {"error":"task not found by the provided id"}
            return False,message



        #* checking that the user didnt pass empty update data dict
        if not cleaned_data["update_data"]:
            message = {"error":"you cant pass empty udpate_data ","json_example for updata_data":{
                "department_id":1,
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
            update_obj = DepartmentTask.objects.get(id=cleaned_data["task_id"])
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
    department_id = serializers.IntegerField(default=None)

    def get_info(self,cleaned_data):
        allowed_fields = ["task_id","department_id"]

        #* checking if passed empty json
        if not cleaned_data.items():
            message = {"error":"passed empty json","json_example":{
            "department_id":1,
            "task_id":1,
        }}
            return False,message

        #* this is checking if user passed allowed fields
        for field in cleaned_data.keys():
            if field not in allowed_fields:
                message = {"error":"ivalid passed fields","allowed_fields":allowed_fields}
                return False,message
            
        # #* checking if the department is exists
        department_exists = Department.objects.filter(id=cleaned_data["department_id"]).exists()
        if department_exists:
            department_obj = Department.objects.get(id=cleaned_data["department_id"])
        else:
            message = {"error","department not exists"}
            return False,message


        #* this section will query the databases and return error if nothing was found
        query = Q()
        # print(self.__getattribute__("data").items())
        for item,item_value in self.__getattribute__("data").items():

            
            #* checking if the email are axists in the task table
            if item == "department_id" and item_value == True:
                department_task_exists = Department.objects.exists(id=cleaned_data["department_id"]).exists()
                if department_task_exists:
                    task_data = department_obj.task.all().values("id","title")
                    message = {"success":"department tasks found","department_tasks":task_data}
                    return False,message
                
                else:
                    message = {"error":"invalid department name provided"}


            if item == "task_id" and item_value != None :

                #* first checking if the task exists
                task_exists = DepartmentTask.objects.filter(id=cleaned_data["task_id"]).exists()
                if task_exists:
                    task_obj = DepartmentTask.objects.get(id=cleaned_data["task_id"])
                    department_relation_exists = Department.task.filter(id=task_obj.id).exists()
                    if department_relation_exists:
                        query &= Q(id=cleaned_data["task_id"])
                    else:
                        message = {"error":"not data about tasks with this department"}

                        return False,message
                else:
                    message = {"error":"this task not exists"}
                    return False,message
                

        query_exists = DepartmentTask.objects.filter(query).exists()
        if query_exists:
            task_data= DepartmentTask.objects.filter(query).values("id","title","description")
            message = {"success":task_data}
            return True,message
        message = {"error":"all fields that was added are not found togheter","asumptions":"try to remove some of the fields and search again"}
        return False,message

