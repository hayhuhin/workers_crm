from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from company.models import Company
from user.models import User,CompanyInvitation
from custom_validation.validation import CustomValidation,OutputMessages
UserModel = get_user_model()


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
    

class JoinCompanySerializer(serializers.Serializer):
    admin_email = serializers.EmailField(default = None)
    otp = serializers.CharField(default=None)

    def get_info(self,cleaned_data,user):
        user_obj = User.objects.get(email=user["email"])

        main = "request have to be sent as post"
        second = {
            "admin_email":"admin@admin.com",
            "otp":"one time password that the admin gave you"
                  }
        success_msg = OutputMessages.success_with_message(main,second)
        
        return success_msg
    
    def create(self,cleaned_data,user):
        required_fields = list(self.fields.keys())
        cv = CustomValidation()
        validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(validation):
            return validation
        else:
            user_obj = validation[1]["object"]
        
        required_company_exists = CompanyInvitation.objects.filter(code=cleaned_data["otp"]).exists()
        if not required_company_exists:
            main = "cant join this company"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg
        else:
            join_otp = CompanyInvitation.objects.get(code=cleaned_data["otp"])
        
        if join_otp.is_valid():
            join_otp.used = True
            join_otp.save()
            # print(join_otp.company)
            required_company = join_otp.company
        
        else:
            main = "expired OTP or already used"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg

        #* here im adding the user to the company
        user_obj.companies.add(required_company)
        user_obj.blocked_by.add(required_company)
        user_obj.save()

        main = "successfully joined the company"
        second = {"company_json":{
            "company":required_company.name,
            "company_admin":cleaned_data["admin_email"]
            }}
        success_msg = OutputMessages.success_with_message(main,second)
        return success_msg


class GenerateOTPSerializer(serializers.Serializer):
    def get_info(self,cleaned_data,user):
        user_obj = User.objects.get(email=user["email"])

        #* if the admin didn't selected the company he cant generate the otp
        if not user_obj.selected_company:
            main = "admin must select company first and then generate the otp"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg
        else:
            company_obj = user_obj.selected_company


        code_otp = CompanyInvitation.generate(company=company_obj)
        # Send otp.code to the user via email
        main = "otp generated successfully"
        second = {"otp_json":{
            "code":code_otp.code,"created_at":code_otp.created_at,"important":"its valid only for three minutes"
            }}
        success_msg = OutputMessages.success_with_message(main,second)
        
        return success_msg
        # When user submits OTP:
        user_inputted_otp = request.POST.get('otp')
        otp = OTP.objects.filter(code=user_inputted_otp).first()
        if otp and otp.is_valid():
            otp.used = True
            otp.save()
            # Add user to company


class CompanySelectSerializer(serializers.Serializer):
    company_name = serializers.CharField(default = None)

    def get_info(self,cleaned_data,user):

        cv = CustomValidation()
        validation = cv.basic_validation(user=user,empty_json=True)
        if not all(validation):
            return validation
        else:
            user_obj = validation[1]["object"]

        
        if user_obj.managed_company :
            managed_companies = user_obj.managed_company.name
        else:
            managed_companies = None

        joined_companies = user_obj.companies.all().values("name")

        main = "data found successfully"
        second = {
            "managed_companies":managed_companies,
            "companies":joined_companies
                  }
        success_msg = OutputMessages.success_with_message(main,second)
        return success_msg
    

    def select(self,cleaned_data,user):
        selected_company_permission = Group.objects.get(name="selected_company_permission")
        required_fields = list(self.fields.keys())
        cv = CustomValidation()
        validation = cv.basic_validation(input_fields=cleaned_data,required_fields=required_fields,user=user)
        if not all(validation):
            return validation
        else:
            user_obj = validation[1]["object"]
        

        #* checking if the selected company in blocked list
        if user_obj.blocked_by.filter(name=cleaned_data["company_name"]).exists():
            user_obj.groups.remove(selected_company_permission)
            main = "this user is blocked"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg

        required_company_exists = user_obj.companies.filter(name=cleaned_data["company_name"]).exists()
        if not required_company_exists:
            main = "company not found"
            err_msg = OutputMessages.error_with_message(main)
            return err_msg
        else:
            company_obj =  user_obj.companies.get(name=cleaned_data["company_name"])

        #*adding selected_company_permission so the user can access other api urls
        user_obj.groups.add(selected_company_permission)

        #*adding the selected company into the 
        user_obj.selected_company = company_obj
        user_obj.save()

        main = "successfully selected company"
        second = {
            "selected_company":user_obj.selected_company.name
            }
        success_msg = OutputMessages.success_with_message(main,second)
        return success_msg


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

