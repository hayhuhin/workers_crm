
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
# from .serializers import CreateIncomeSerializer,DeleteIncomeSerializer,UpdateIncomeSerializer,GetIncomeSerializer,CreateOutcomeSerializer,DeleteOutcomeSerializer,UpdateOutcomeSerializer,GetOutcomeSerializer
# from user.models import User
# from employer.models import Employer
from user.permissions import FinanceFullPermission,FinanceUpdatePermission,FinanceViewPermission
from .serializers import CreateCustomerSerializer,DeleteClientSerializer,UpdateClientSerializer,GetClientSerializer

#* customer table fields
    # name = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    # address = models.TextField(blank=True, null=True)
    # notes = models.TextField(blank=True, null=True)
    # customer_id = models.IntegerField()


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
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = CreateCustomerSerializer(data = cleaned_data)
        if serializer.is_valid():
            create_data = serializer.create(cleaned_data=cleaned_data,user=user)
            if all(create_data):
                return Response(create_data[1],status=status.HTTP_200_OK)
            return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



class DeleteClientView(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission]


    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}
        serializer = DeleteClientSerializer(data = cleaned_data)
        if serializer.is_valid():
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)
        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}
        serializer = DeleteClientSerializer(data = cleaned_data)
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
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
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

