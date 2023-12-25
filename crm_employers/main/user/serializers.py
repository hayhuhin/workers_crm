from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token




UserModel = get_user_model()
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
    
    def create(self,clean_data):
        data = {}
        user_obj = UserModel.objects.create_user(email=clean_data["email"],username=clean_data["username"],password=clean_data["password"])
        user_obj.save()
        token = Token.objects.get(user=user_obj).key
        data["username"] = user_obj.username
        data["email"] = user_obj.email
        data["token"] = token
        return data
    
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email","password")
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self,clean_data):
        print(clean_data["email"])
        user = authenticate(username=clean_data["email"],password=clean_data["password"])
        if not user:
            raise ValueError("user not found")
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email","username")