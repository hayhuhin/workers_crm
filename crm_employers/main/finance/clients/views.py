
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
# from .serializers import CreateIncomeSerializer,DeleteIncomeSerializer,UpdateIncomeSerializer,GetIncomeSerializer,CreateOutcomeSerializer,DeleteOutcomeSerializer,UpdateOutcomeSerializer,GetOutcomeSerializer
# from user.models import User
# from employer.models import Employer
from user.permissions import FinanceFullPermission,FinanceUpdatePermission,FinanceViewPermission
from .serializers import CreateClientSerializer,DeleteClientSerializer,UpdateClientSerializer,GetClientSerializer

#* customer table fields
    # name = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    # address = models.TextField(blank=True, null=True)
    # notes = models.TextField(blank=True, null=True)
    # customer_id = models.IntegerField()


class CreateClientView(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission,]


    def get(self,request):
        cleaned_data = request.data
        serializer = CreateClientSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        serializer = CreateClientSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            create_data = serializer.create(cleaned_data=cleaned_data)

            if all(create_data):
                return Response(create_data[1],status=status.HTTP_200_OK)
            return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



class DeleteClientView(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission]


    def get(self,request):
        cleaned_data = request.data
        serializer = DeleteClientSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        serializer = DeleteClientSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            delete_data = serializer.delete(cleaned_data=cleaned_data)

            if all(delete_data):
                return Response(delete_data[1],status=status.HTTP_200_OK)
            return Response(delete_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)




class UpdateClientView(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission]


    def get(self,request):
        cleaned_data = request.data
        serializer = UpdateClientSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            delete_data = serializer.get_info(cleaned_data=cleaned_data)

            if all(delete_data):
                return Response(delete_data[1],status=status.HTTP_200_OK)
            return Response(delete_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        serializer = UpdateClientSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            update_data = serializer.update(cleaned_data=cleaned_data)

            if all(update_data):
                return Response(update_data[1],status=status.HTTP_200_OK)
            return Response(update_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



class GetClientView(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission]

    def get(self,request):
        cleaned_data = request.data
        serializer = GetClientSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            delete_data = serializer.get_info(cleaned_data=cleaned_data)

            if all(delete_data):
                return Response(delete_data[1],status=status.HTTP_200_OK)
            return Response(delete_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    # def post(self,request):
    #     cleaned_data = request.data
    #     serializer = GetClientSerializer(data = cleaned_data)
    #     if serializer.is_valid(raise_exception = True):
    #         delete_data = serializer.(cleaned_data=cleaned_data)

    #         if all(delete_data):
    #             return Response(delete_data[1],status=status.HTTP_200_OK)
    #         return Response(delete_data[1],status=status.HTTP_404_NOT_FOUND)

    #     message = {"error":"invalid fields passed"}
    #     return Response(message,status=status.HTTP_404_NOT_FOUND)





