from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
# from user.permissions import FinanceUpdatePermission,FinanceViewPermission
from .serializers import CreateTaskSerializer,DeleteTaskSerializer,UpdateTaskSerializer,GetTaskSerializer


class CreateTask(APIView):
    permission_classes = [permissions.IsAuthenticated,]


    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = CreateTaskSerializer(data=cleaned_data)
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
        serializer = CreateTaskSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            create_data = serializer.create(cleaned_data=cleaned_data,user=user)

            if all(create_data):
                return Response(create_data[1],status=status.HTTP_200_OK)
            return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)




class DeleteTask(APIView):
    permission_classes = [permissions.IsAuthenticated,]


    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = DeleteTaskSerializer(data = cleaned_data)
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
        serializer = DeleteTaskSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            create_data = serializer.delete(cleaned_data=cleaned_data,user=user)

            if all(create_data):
                return Response(create_data[1],status=status.HTTP_200_OK)
            return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)




class UpdateTask(APIView):
    permission_classes = [permissions.IsAuthenticated,]


    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = UpdateTaskSerializer(data = cleaned_data)
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
        serializer = UpdateTaskSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            create_data = serializer.update(cleaned_data=cleaned_data,user=user)

            if all(create_data):
                return Response(create_data[1],status=status.HTTP_200_OK)
            return Response(create_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields passed"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)




class GetTask(APIView):
    permission_classes = [permissions.IsAuthenticated,]


    def get(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = GetTaskSerializer(data = cleaned_data)
        if serializer.is_valid(raise_exception = True):
            get_info = serializer.get_info(cleaned_data=cleaned_data,user=user)

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
