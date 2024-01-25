from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from .models import Employer
from user.models import User



class CreateIncomeSerializer(serializers.Serializer):
    pass


class DeleteIncomeSerializer(serializers.Serializer):
    pass


class UpdateIncomeSerializer(serializers.Serializer):
    pass 


class GetIncomeSerializer(serializers.Serializer):
    pass






class CreateOutcomeSerializer(serializers.Serializer):
    pass


class DeleteOutcomeSerializer(serializers.Serializer):
    pass


class UpdateOutcomeSerializer(serializers.Serializer):
    pass


class GetOutcomeSerializer(serializers.Serializer):
    pass

