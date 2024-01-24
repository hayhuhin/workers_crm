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


class DeleteDepartmentSerializer(serializers.Serializer):
    pass

    def delete(self,cleaned_data):
        pass

class UpdateDepartmentSerializer(serializers.Serializer):
    pass

    def update(self,cleaned_data):
        pass

class GetDepartmentSerializer(serializers.Serializer):
    pass

    def get(self,cleaned_data):
        pass