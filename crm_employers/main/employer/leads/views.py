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
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = CreateLeadSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = False):
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_info):
                return Response(get_info[1],status=status.HTTP_200_OK)
            return Response(get_info[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed","required_fields":{
            "first_name":"john",
            "last_name":"doe",
            "email":"john_doe@electric.com",
            "phone_number":"112233",
            "customer_id":123456789,
            "status":"choose one of these: new,contacted,qulified,lost,converted",
            "source":"Source from which the lead was acquired (optional, e.g., website, referral, cold call)",
            "notes":"notes text",
            "assigned_to":"employee email who assigned to the lead"
        }}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = CreateLeadSerializer(data=cleaned_data)
        if serializer.is_valid(raise_exception=False):
            create_data = serializer.create(cleaned_data=cleaned_data,user=user)

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
