from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from user.permissions import ITAdminPermission,SystemAdminPermission,MediumPermission
from .serializers import CreateDepartmentSerializer,DeleteDepartmentSerializer,UpdateDepartmentSerializer,GetDepartmentSerializer





#*need to create department handling of creation and deletion

class CreateDepartment(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission,)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = CreateDepartmentSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = False):
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}

        serializer = CreateDepartmentSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=False):
            created_department = serializer.create(cleaned_data=cleaned_data,user=user)

            if all(created_department):
                return Response(created_department[1],status=status.HTTP_201_CREATED)
            
            return Response(created_department[1],status=status.HTTP_404_NOT_FOUND)
        
        else:
            response = {"error":"invalid input","required_fields":{
            "name":"name of the department (engineer ...)",
            "rank":"rank of the department",
            "salary":"integer of the salary of the mployer"
        }}
            return Response(response,status=status.HTTP_404_NOT_FOUND)


class DeleteDepartment(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission,)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = DeleteDepartmentSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = False):
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}

        serializer = DeleteDepartmentSerializer(data=cleaned_data)
        if serializer.is_valid():
            deleted_department = serializer.delete(cleaned_data=cleaned_data,user=user)

            if all(deleted_department):
                return Response(deleted_department[1],status=status.HTTP_201_CREATED)
            
            return Response(deleted_department[1],status=status.HTTP_404_NOT_FOUND)
        
        response = {"error":"invalid input","required_fields":{
            "name":"name of the department you want to delete"
        }}
        return Response(response,status=status.HTTP_404_NOT_FOUND)


class UpdateDepartment(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission,)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = UpdateDepartmentSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = False):
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = UpdateDepartmentSerializer(data=cleaned_data)
        if serializer.is_valid():
            updated_department = serializer.update(cleaned_data=cleaned_data,user=user)

            if all(updated_department):
                return Response(updated_department[1],status=status.HTTP_201_CREATED)
            
            return Response(updated_department[1],status=status.HTTP_404_NOT_FOUND)
        response = {"error":"invalid input","required_fields":{
            "name":"name of the department",
            "update_data":{
                "name":"update the name",
                "rank":"update the rank",
                "salary":"update the salary",
            }
        }}
        return Response(response,status=status.HTTP_404_NOT_FOUND)


class GetDepartment(APIView):
    permission_classes = (permissions.IsAuthenticated,)


    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = GetDepartmentSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_department = serializer.get_info(cleaned_data=cleaned_data,user=user)

            if all(created_department):
                return Response(created_department[1],status=status.HTTP_201_CREATED)
            
            return Response(created_department[1],status=status.HTTP_404_NOT_FOUND)
        response = {"error":"invalid input","required_fields":{
            "name":"name of the department",
            "all_departments":"all departments that are created"
        }}
        return Response(response,status=status.HTTP_404_NOT_FOUND)
