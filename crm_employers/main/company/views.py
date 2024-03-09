from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from user.permissions import ITAdminPermission,SystemAdminPermission,MediumPermission
from .serializers import CreateCompanySerializer,DeleteCompanySerializer,UpdateCompanySerializer,GetCompanySerializer




#*need to create department handling of creation and deletion

class CreateCompany(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission,)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}

        serializer = CreateCompanySerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}

        serializer = CreateCompanySerializer(data=cleaned_data)
        if serializer.is_valid():
            created_department = serializer.create(cleaned_data=cleaned_data,user=user)

            if all(created_department):
                return Response(created_department[1],status=status.HTTP_201_CREATED)
            
            return Response(created_department[1],status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"passed invalid fields","valid_fields":serializer.fields.keys()},status=status.HTTP_404_NOT_FOUND)


class DeleteCompany(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission,)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}

        user = {"email":request.user.email}

        serializer = DeleteCompanySerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = False):
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)
        
        else:
            message = {"error":"invalid fields passed"}
            return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = DeleteCompanySerializer(data=cleaned_data)
        if serializer.is_valid():
            deleted_department = serializer.delete(cleaned_data=cleaned_data,user=user)

            if all(deleted_department):
                return Response(deleted_department[1],status=status.HTTP_201_CREATED)
            
            return Response(deleted_department[1],status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"invalid input"},status=status.HTTP_404_NOT_FOUND)


class UpdateCompany(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission,)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}




        user = {"email":request.user.email}
        print(cleaned_data)
        serializer = UpdateCompanySerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)




    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}

        print(cleaned_data)
        serializer = UpdateCompanySerializer(data=cleaned_data)
        if serializer.is_valid():
            updated_department = serializer.update(cleaned_data=cleaned_data,user=user)

            if all(updated_department):
                return Response(updated_department[1],status=status.HTTP_201_CREATED)
            
            return Response(updated_department[1],status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"invalid input"},status=status.HTTP_404_NOT_FOUND)


class GetCompany(APIView):
    permission_classes = (permissions.IsAuthenticated,ITAdminPermission)


    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}

        serializer = DeleteCompanySerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)
