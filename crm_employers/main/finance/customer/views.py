
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from user.permissions import FinanceFullPermission,FinanceUpdatePermission,FinanceViewPermission
from .serializers import CreateCustomerSerializer,DeleteCustomerSerializer,UpdateClientSerializer,GetClientSerializer



class CreateCustomerView(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission,]


    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = CreateCustomerSerializer(data = cleaned_data)
        if serializer.is_valid():
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}

        serializer = CreateCustomerSerializer(data = cleaned_data)
        if serializer.is_valid():
            create_data = serializer.create(cleaned_data=cleaned_data,user=user)
            if all(create_data):
                return Response(create_data[1],status=status.HTTP_200_OK)
            return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



class DeleteCustomertView(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission]


    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}
        serializer = DeleteCustomerSerializer(data = cleaned_data)
        if serializer.is_valid():
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)
        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = DeleteCustomerSerializer(data = cleaned_data)
        if serializer.is_valid():
            delete_data = serializer.delete(cleaned_data=cleaned_data,user=user)
            if all(delete_data):
                return Response(delete_data[1],status=status.HTTP_200_OK)
            return Response(delete_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)




class UpdateClientView(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission]


    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}
        serializer = UpdateClientSerializer(data = cleaned_data)
        if serializer.is_valid():
            delete_data = serializer.get_info(cleaned_data=cleaned_data,user=user)

            if all(delete_data):
                return Response(delete_data[1],status=status.HTTP_200_OK)
            return Response(delete_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data

        user = {"email":request.user.email}
        serializer = UpdateClientSerializer(data = cleaned_data)
        if serializer.is_valid():
            update_data = serializer.update(cleaned_data=cleaned_data,user=user)
            if all(update_data):
                return Response(update_data[1],status=status.HTTP_200_OK)
            return Response(update_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



class GetClientView(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission]

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}
        serializer = GetClientSerializer(data = cleaned_data)
        if serializer.is_valid():
            delete_data = serializer.get_info(cleaned_data=cleaned_data,user=user)

            if all(delete_data):
                return Response(delete_data[1],status=status.HTTP_200_OK)
            return Response(delete_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)

