from rest_framework import serializers
from employer.models import Department


class CreateDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

    def create(self,cleaned_data):
        required_department = cleaned_data["name"]

        #check if the department exists
        department_exists = Department.objects.filter(name=required_department).exists()
        if department_exists:
            message = {"error":"this department is already exists"}
            return False,message
        
        obj_instance = Department.objects.create(
            name=cleaned_data["name"],
            salary=cleaned_data["salary"]
        )
        obj_instance.save()

        return True,{"success":f"department {obj_instance.name} created with the salary of {obj_instance.salary}"}


class DeleteDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["name"]


    def delete(self,cleaned_data):
        required_department = cleaned_data["name"]

        #check if the department exists
        department_exists = Department.objects.filter(name=required_department).exists()
        if department_exists:
            #getting object instance of the department
            department = Department.objects.get(name=cleaned_data["name"])
            #getting the department name for the message
            department_name = str(department)
            #deleting it
            department.delete()
            
            message = {"success":f"{department_name} is deleted, employers that were in this department set to Null"}
            return True,message
        

        message = {"error":"this department doesnt exists"}
        return False,message



class UpdateDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    required_field = serializers.DictField()

    def update(self,cleaned_data):
        restricted_fields = ["id","rank","started_at"]
        allowed_fields = ["name","salary"]

        required_department = cleaned_data["name"]

        #check if the department exists
        department_exists = Department.objects.filter(name=required_department).exists()
        if department_exists:
            #getting object instance of the department
            department = Department.objects.get(name=cleaned_data["name"])
            #iterating over the requiored fields
            for key,values in cleaned_data["required_field"].items():
                #check if the key in the restricted list
                if key in restricted_fields:
                    message = {"error":"cant change this fields"}
                    return False,message
                #validate that the key is only in the allowed field
                if key in allowed_fields:
                    setattr(department,key,values)
                
                else:
                    message = {"error":"cant assign this fields"}
                    return False,message
                
            #if all valid saving the changes  
            department.save()
            message = {"success":f"{department.name} is changed."}
            return True,message
        

        message = {"error":"this department doesnt exists"}
        return False,message



class GetDepartmentSerializer(serializers.Serializer):
    choices = ["specific","all"]

    view = serializers.ChoiceField(choices=choices)
    name = serializers.CharField(max_length=20,default="no name")

    def get(self,cleaned_data):
        

        if cleaned_data["view"] == "specific":
            
            #this is checking if the user didnt add the name key to the request
            try :
                required_name = cleaned_data["name"]

            except:
                message = {"error":"you must add key of name and the required value to get the specific department"}
                return False,message
            
            #checking if the department exists
            required_department = Department.objects.filter(name=required_name).exists()
            if required_department:
                department_data = Department.objects.get(name=required_name)

                message = {"success":{
                    "name":department_data.name,
                    "rank":department_data.rank,
                    "salary":department_data.salary }}
                
                return True,message
            
            message = {"error":"this department doesnt exists"}
            return False,message
        

        if cleaned_data["view"] == "all":
            
            departments_dict = {}
            departments = Department.objects.all()
            for job in departments:
                departments_dict[job.name]={
                    "name":job.name,
                    "rank":job.rank,
                    "salary":job.salary}
            
            message = {"success":{"departments":departments_dict}}
            return True,message

        message = {"error":"invalid field provided"}
        return False,message
        