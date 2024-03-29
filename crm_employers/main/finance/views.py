
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .serializers import CreateIncomeSerializer,DeleteIncomeSerializer,UpdateIncomeSerializer,GetIncomeSerializer,CreateOutcomeSerializer,DeleteOutcomeSerializer,UpdateOutcomeSerializer,GetOutcomeSerializer
from user.permissions import FinanceFullPermission,FinanceUpdatePermission,FinanceViewPermission

# Create your views here.



#* Income section
class CreateIncome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission,)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = CreateIncomeSerializer(data=cleaned_data)
        
        if serializer.is_valid():
            get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)

            return Response(get_data[1],status=status.HTTP_200_OK)

        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)
        


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        
        
        serializer = CreateIncomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.create(cleaned_data=cleaned_data,user=user)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
        
        message = {"error":"invalid fields"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


class DeleteIncome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceFullPermission)


    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = DeleteIncomeSerializer(data=cleaned_data)
        
        if serializer.is_valid():
            get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_data):
                return Response(get_data[1],status=status.HTTP_200_OK)

            return Response(get_data[1],status=status.HTTP_404_NOT_FOUND)
            
        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        serializer = DeleteIncomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.delete(cleaned_data=cleaned_data,user=user)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"passed invalid fields"},status=status.HTTP_404_NOT_FOUND)



class UpdateIncome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceUpdatePermission)


    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}
        serializer = UpdateIncomeSerializer(data=cleaned_data)
        
        if serializer.is_valid():
            get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_data):
                return Response(get_data[1],status=status.HTTP_200_OK)
            else:
                return Response(get_data[1],status=status.HTTP_404_NOT_FOUND)
        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}
        
        serializer = UpdateIncomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.update(cleaned_data=cleaned_data,user=user)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)


class GetIncome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceViewPermission)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = GetIncomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_200_OK)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
        
        message = {"error":"the fields are invalid"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)



#*outcome section
class CreateOutcome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceFullPermission)


    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = CreateOutcomeSerializer(data=cleaned_data)
        
        if serializer.is_valid():
            get_data = serializer.get_info(cleaned_data=cleaned_data,user=user)

            return Response(get_data[1],status=status.HTTP_200_OK)

        return Response({"error":"invalid data passed"},status=status.HTTP_404_NOT_FOUND)
        


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}

        serializer = CreateOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.create(cleaned_data=cleaned_data,user=user)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)

        return Response({"error":"invalid fields"},status=status.HTTP_404_NOT_FOUND)


class DeleteOutcome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceFullPermission)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = DeleteOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            get_information = serializer.get_info(cleaned_data=cleaned_data,user=user)
            if all(get_information):
                return Response(get_information[1],status=status.HTTP_200_OK)
            return Response(get_information[1],status=status.HTTP_404_NOT_FOUND)
        
        message = {"error":"invalid get request"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)
    

    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}

        serializer = DeleteOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.delete(cleaned_data=cleaned_data,user=user)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)


class UpdateOutcome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceFullPermission)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = UpdateOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_200_OK)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)
        
        message = {"error":"invalid fields"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        cleaned_data = request.data
        user = {"email":request.user.email}

        serializer = UpdateOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.update(cleaned_data=cleaned_data,user=user)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_201_CREATED)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)


class GetOutcome(APIView):
    permission_classes = (permissions.IsAuthenticated,FinanceViewPermission)

    def get(self,request):
        query_dict = {**request.GET}
        cleaned_data = {key: value[0] for key, value in query_dict.items()}
        user = {"email":request.user.email}

        serializer = GetOutcomeSerializer(data=cleaned_data)
        if serializer.is_valid():
            created_data = serializer.get_info(cleaned_data=cleaned_data,user=user)
            
            if all(created_data):
                return Response(created_data[1],status=status.HTTP_200_OK)
            
            return Response(created_data[1],status=status.HTTP_404_NOT_FOUND)

        message = {"error":"invalid fields"}
        return Response(message,status=status.HTTP_404_NOT_FOUND)
