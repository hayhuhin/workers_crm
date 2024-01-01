from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from .models import Employer
from user.models import User


class AddProfileSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Employer
        fields = ["first_name","last_name","email","phone"]
        # fields = ["first_name","last_name","email","phone",""]

    def create(self,cleaned_data):
        data = {}
        user_instance = User.objects.get(email=cleaned_data["email"])

        try:
            status = "HTTP_201_CREATED"
            employer_obj = Employer.objects.create(
                user=user_instance,
                first_name=cleaned_data["first_name"],
                last_name=cleaned_data["last_name"],
                email=cleaned_data["email"],
                phone=cleaned_data["phone"],)
            employer_obj.save()
            data["first_name"] = cleaned_data["first_name"]
            data["last_name"] = cleaned_data["last_name"]
            return data,status
        
        except:
            error_message = {"error":"this user is already exists as employer"}
            status = "HTTP_404_NOT_FOUND"
            return error_message,status



class GetProfileSerializer(serializers.Serializer):
    class Meta:
        model = Employer
        fields = "__all__"

        