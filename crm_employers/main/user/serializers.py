from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from company.models import Company
from user.models import User 
from custom_validation.validation import CustomValidation,OutputMessages
UserModel = get_user_model()


# class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ["username","email","password"]


#     def get_info(self,cleaned_data):
#         main = "you have to fill this json as a post method"
#         second = {"example_json":{
#             "username":"the wanted username for the user",
#             "email":"email of the user",
#             "password":"password of the user"
#         }}
#         success_msg = OutputMessages.success_with_message(main,second)
#         return success_msg


#     def create(self,cleaned_data,user):
#         admin_email = user["email"]

#         #* first im checking if the admin is already has a company
#         admin_has_company = User.objects.get(email=admin_email)
#         if not admin_has_company.company:
#             main = "the admin didn't created a company"
#             err_msg = OutputMessages.error_with_message(main)
#             return err_msg

#         else:
#             creator_user_obj = User.objects.get(email=admin_email)
#             creator_company_obj = creator_user_obj.company


#         user_obj = User.objects.create_user(email=cleaned_data["email"],username=cleaned_data["username"],password=cleaned_data["password"])
#         user_obj.save()

#         user_obj.company = creator_company_obj
#         user_obj.save()
#         token = Token.objects.get(user=user_obj).key

#         main = "user created successfully"
#         second = {"user_json":{
#             "username" :user_obj.username,
#             "email" :user_obj.email,
#             "token" : token,
#             "company": creator_company_obj.name
#         }}
#         success_msg = OutputMessages.success_with_message(main,second)
#         return success_msg



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self,cleaned_data):
        user_obj = UserModel.objects.create_user(email=cleaned_data["email"],username=cleaned_data["username"],password=cleaned_data["password"])
        user_obj.save()
        token = Token.objects.get(user=user_obj).key
        main = "new user created successfully"
        second = {
            "user_json":{
                "username":user_obj.username,
                "email" : user_obj.email,
                "token" : token
        }}
        
        # #* this section im creating all start permission and admin permission for this specific user
        # admin_permissions = ["admin_permission","IT_permission","medium_permission","finance_full_permission","finance_view_permission","finance_update_permission"]

        # for permission in admin_permissions:
        #     group_obj = Group.objects.create(name=permission)
        #     group_obj.save()

        #     user_obj.groups.add(group_obj)
        #     user_obj.save()
        
        success_msg = OutputMessages.success_with_message(main,second)
        return success_msg



class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email","password")
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self,clean_data):
        user = authenticate(username=clean_data["email"],password=clean_data["password"])
        if not user:
            raise ValueError("user not found")
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email","username")
    

#* assign rules serializer section
class AssignFinanceFullPermissionSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def assign(self,cleaned_data):
        
        try:
            #the user that we want to perform the actions
            user_found = UserModel.objects.get(email=cleaned_data["email"])
            permission_found = Group.objects.get(name="finance_full_permission")

            #checking if the user is already have the group permission
            user_have_permission = user_found.groups.filter(name="finance_full_permission").exists()
            if user_have_permission:
                message = {"error":f" {user_found} already have this permission"}    
                return False,message

            #if the user added the first time
            user_found.groups.add(permission_found)
            message = {"success":f"added  {user_found} to finance full permission"}
            return True,message
        
        except:
             message = {"error":f"no {user_found} or permission is found"}
             return False,message
     	

class AssignFinanceViewPermissionSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def assign(self,cleaned_data):
        
        try:
            #the user that we want to perform the actions
            user_found = UserModel.objects.get(email=cleaned_data["email"])

            #checking if the user is admin or staff
            if user_found.is_superuser or user_found.is_staff:
                message = {"error":"cant assign to this user permissions"}
                return False,message

            permission_found = Group.objects.get(name="finance_view_permission")

            #checking if the user is already have the group permission
            user_have_permission = user_found.groups.filter(name="finance_view_permission").exists()
            if user_have_permission:
                message = {"error":f" {user_found} already have this permission"}    
                return False,message


            user_found.groups.add(permission_found)
            message = {"success":f"added  {user_found} to finance view permission"}
            return True,message
        
        except:
             message = {"error":f"no {user_found} or permission is found"}
             return False,message
     
	
class AssignFinanceUpdatePermissionSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def assign(self,cleaned_data):
        
        try:
            #the user that we want to perform the actions
            user_found = UserModel.objects.get(email=cleaned_data["email"])

            #checking if the user is admin or staff
            if user_found.is_superuser or user_found.is_staff:
                message = {"error":"cant assign to this user permissions"}
                return False,message
            
            permission_found = Group.objects.get(name="finance_update_permission")

            #checking if the user is already have the group permission
            user_have_permission = user_found.groups.filter(name="finance_update_permission").exists()
            if user_have_permission:
                message = {"error":f" {user_found} already have this permission"}    
                return False,message


            user_found.groups.add(permission_found)
            message = {"success":f"added  {user_found} to finance update permission"}
            return True,message
        
        except:
             message = {"error":f"no {user_found} or permission is found"}
             return False,message
     


#* disallow section serializers
class DisallowFinanceFullPermissionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def disallow(self,cleaned_data):
        try:
            #the user that we want to perform the actions
            user_found = UserModel.objects.get(email=cleaned_data["email"])

            #checking if the user is admin or staff
            if user_found.is_superuser or user_found.is_staff:
                message = {"error":"cant disallow this user permissions"}
                return False,message
            
            permission_found = Group.objects.get(name="finance_full_permission")

            #checking if the user is already not in the group permission
            user_have_permission = user_found.groups.filter(name="finance_full_permission").exists()
            if not user_have_permission:
                message = {"error":f" {user_found} already dont have this permission"}    
                return False,message
            
            user_found.groups.remove(permission_found)
            message = {"success":f"removed  {user_found} from finance full permission"}
            return True,message

        except:
            message = {"error":f"no {user_found} or permission is found"}
            return False,message


class DisallowFinanceViewPermissionSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def disallow(self,cleaned_data):
        try:
            #the user that we want to perform the actions
            user_found = UserModel.objects.get(email=cleaned_data["email"])

            #checking if the user is admin or staff
            if user_found.is_superuser or user_found.is_staff:
                message = {"error":"cant disallow this user permissions"}
                return False,message
            
            
            permission_found = Group.objects.get(name="finance_view_permission")

            #checking iff the {user_found} is already not in the group permission
            user_have_permission = user_found.groups.filter(name="finance_view_permission").exists()
            if not user_have_permission:
                message = {"error":f" {user_found} already dont have this permission"}    
                return False,message
            
            user_found.groups.remove(permission_found)
            message = {"success":f"removed  {user_found} from finance view permission"}
            return True,message

        except:
            message = {"error":f"no {user_found} or permission is found"}
            return False,message


class DisallowFinanceUpdatePermissionSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def disallow(self,cleaned_data):
        try:
            #the user that we want to perform the actions
            user_found = UserModel.objects.get(email=cleaned_data["email"])

            #checking if the user is admin or staff
            if user_found.is_superuser or user_found.is_staff:
                message = {"error":"cant disallow this user permissions"}
                return False,message
            
            permission_found = Group.objects.get(name="finance_update_permission")

            #checking iff the {user_found} is already not in the group permission
            user_have_permission = user_found.groups.filter(name="finance_update_permission").exists()
            if not user_have_permission:
                message = {"error":f" {user_found} already dont have this permission"}    
                return False,message
            
            user_found.groups.remove(permission_found)
            message = {"success":f"removed  {user_found} from finance update permission"}
            return True,message

        except:
            message = {"error":f"no {user_found} or permission is found"}
            return False,message

