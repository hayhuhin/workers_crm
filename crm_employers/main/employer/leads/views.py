from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from user.permissions import FinanceUpdatePermission,FinanceViewPermission
from .serializers import CreateLeadSerializer,DeleteLeadSerializer,UpdateLeadSerializer,GetLeadSerializer
from user.models import User
from finance.models import Customer
from employer.models import Employer


class CreateLead(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission,]


    def get(self,request):
        cleaned_data = request.data
        serializer = CreateLeadSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        serializer = CreateLeadSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            create_data = serializer.create(cleaned_data=cleaned_data)

            if all(create_data):
                return Response(create_data[1],status=status.HTTP_200_OK)
            return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)




class DeleteLead(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission,]


    def get(self,request):
        cleaned_data = request.data
        serializer = DeleteLeadSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        serializer = DeleteLeadSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            create_data = serializer.delete(cleaned_data=cleaned_data)

            if all(create_data):
                return Response(create_data[1],status=status.HTTP_200_OK)
            return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)




class UpdateLead(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceUpdatePermission,]


    def get(self,request):
        cleaned_data = request.data
        serializer = UpdateLeadSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        serializer = UpdateLeadSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            create_data = serializer.update(cleaned_data=cleaned_data)

            if all(create_data):
                return Response(create_data[1],status=status.HTTP_200_OK)
            return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)




class GetLead(APIView):
    permission_classes = [permissions.IsAuthenticated,FinanceViewPermission,]


    def get(self,request):
        cleaned_data = request.data
        serializer = GetLeadSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data)

            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    # def post(self,request):
    #     cleaned_data = request.data
    #     serializer = GetLeadSerializer(data = cleaned_data)
    #     if serializer.is_valid(raise_exception = True):
    #         create_data = serializer.create(cleaned_data=cleaned_data)

    #         if all(create_data):
    #             return Response(create_data[1],status=status.HTTP_200_OK)
    #         return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

    #     message = {"error":"invalid fields passed"}
    #     return Response(message,status=status.HTTP_404_NOT_FOUND)
