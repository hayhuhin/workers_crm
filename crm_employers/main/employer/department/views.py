from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from user.permissions import ITAdminPermission,SystemAdminPermission
from .serializers import CreateDepartmentSerializer,DeleteDepartmentSerializer,UpdateDepartmentSerializer,GetDepartmentSerializer
from user.models import User
from employer.models import Employer



#*need to create department handling of creation and deletion

class CreateDepartment(APIView):
    permission_classes = (permissions.IsAuthenticated, ITAdminPermission)

    def post(self,request):
        cleaned_data = request.data

        serializer = CreateDepartmentSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_department = serializer.create(cleaned_data=cleaned_data)

            if all(created_department):
                return Response(created_department[1],status=status.HTTP_201_CREATED)
            
            return Response(created_department[1],status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"invalid input"},status=status.HTTP_404_NOT_FOUND)


class DeleteDepartment(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission)

    def post(self,request):
        cleaned_data = request.data

        serializer = CreateDepartmentSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_department = serializer.delete(cleaned_data=cleaned_data)

            if all(created_department):
                return Response(created_department[1],status=status.HTTP_201_CREATED)
            
            return Response(created_department[1],status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"invalid input"},status=status.HTTP_404_NOT_FOUND)


class UpdateDepartment(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission)

    def post(self,request):
        cleaned_data = request.data

        serializer = CreateDepartmentSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_department = serializer.update(cleaned_data=cleaned_data)

            if all(created_department):
                return Response(created_department[1],status=status.HTTP_201_CREATED)
            
            return Response(created_department[1],status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"invalid input"},status=status.HTTP_404_NOT_FOUND)


class GetDepartment(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission)

    def get(self,request):
        cleaned_data = request.data

        serializer = CreateDepartmentSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_department = serializer.get(cleaned_data=cleaned_data)

            if all(created_department):
                return Response(created_department[1],status=status.HTTP_201_CREATED)
            
            return Response(created_department[1],status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"invalid input"},status=status.HTTP_404_NOT_FOUND)
