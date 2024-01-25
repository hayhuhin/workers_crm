
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .serializers import CreateIncomeSerializer,DeleteIncomeSerializer,UpdateIncomeSerializer,GetIncomeSerializer,CreateOutcomeSerializer,DeleteOutcomeSerializer,UpdateOutcomeSerializer,GetOutcomeSerializer
from user.models import User
from employer.models import Employer


# Create your views here.

#* Income section
class CreateIncome(APIView):
    pass

    def post(self,request):
        pass


class DeleteIncome(APIView):
    pass

    def post(self,request):
        pass


class UpdateIncome(APIView):
    pass

    def post(self,request):
        pass


class GetIncome(APIView):
    pass

    def get(self,request):
        pass


#*outcome section
class CreateOutcome(APIView):
    pass

    def post(self,request):
        pass


class DeleteOutcome(APIView):
    pass

    def post(self,request):
        pass


class UpdateOutcome(APIView):
    pass

    def post(self,request):
        pass


class GetOutcome(APIView):
    pass

    def get(self,request):
        pass


