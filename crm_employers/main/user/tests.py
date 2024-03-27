from django.test import TestCase
from user.models import User
from company.models import Company
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import Group



class UserRegistrationTest(TestCase):

    def setUp(self):
        self.send_request = APIClient()
        permissions = ["company_creator_permission","admin_permission","selected_company_permission","medium_permission","IT_permission"]

        for per in permissions:
            g_obj = Group.objects.create(name=per)
            g_obj.save()


    def simple_setup(self):
        #* admin user
        path = "/v1/api/user/register"
        data = {
            "username":"admin",
            "email":"admin@admin.com",
            "password":"Aa1122!!"
            }
        response = self.send_request.post(format="json",path=path,data=data)
        user_json = response.json()["user_json"]
        admin_token = user_json["token"]
        admin_request = APIClient()
        admin_request.credentials(HTTP_AUTHORIZATION=f'Token {admin_token}')
        admin = User.objects.get(email="admin@admin.com")
        ad,creator,selected,med,it = Group.objects.all()
        admin.groups.add(ad,creator,selected,med,it)

        #* simple user
        path = "/v1/api/user/register"
        data = {
            "username":"simple",
            "email":"simple@simple.com",
            "password":"Aa1122!!"
            }
        response = self.send_request.post(format="json",path=path,data=data)
        user_json = response.json()["user_json"]
        user_token = user_json["token"]
        user_request = APIClient()
        user_request.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')

        #*creating company with admin user
        path = "/v1/api/company/create"
        data = {
            "name":"dev",
            "description":"dev dev dev",
            "address":"some addr"
            }
        res = admin_request.post(format="json",path=path,data=data)

        #*making the admin to select the company he created
        path = "/v1/api/user/company/select"
        data = {
            "company_name":"dev"
            }
        admin_request.post(format="json",data=data,path=path)
        return admin_request,user_request


    def test_admin_invalid_post(self):

        #* first we creating some admin user
        path = "/v1/api/user/register"
        data = {
            "username":"papa",
            "email":"new@new.com",
            "password":"Aa1122!!"
            }
        get_response = self.send_request.post(format="json",path=path,data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["success","user_json"])
        status_code_test = self.assertEqual(get_response.status_code,201)


        #* now we trying to create same user
        path = "/v1/api/user/register"
        data = {
            "username":"papa",
            "email":"new@new.com",
            "password":"Aa1122!!"
            }
        get_response = self.send_request.post(format="json",path=path,data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,400)

        #* empty json
        path = "/v1/api/user/register"
        data = {}
        get_response = self.send_request.post(format="json",path=path,data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(get_response.status_code,400)


        #* testing invalid field
        path = "/v1/api/user/register"
        data = {
            "invalid":"invalid"
            }
        get_response = self.send_request.post(format="json",path=path,data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(get_response.status_code,400)



        #* testing invalid field type
        path = "/v1/api/user/register"
        data = {
            "username":"username",
            "email":True,
            "password":"Aa1122!!"
            }
        get_response = self.send_request.post(format="json",path=path,data=data)

        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,400)


    def test_admin_valid_post(self):

        #* testing with valid input
        path = "/v1/api/user/register"
        data = {
            "username":"valar",
            "email":"valar@valar.com",
            "password":"Aa1122!!"
            }
        get_response = self.send_request.post(format="json",path=path,data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["success","user_json"])
        status_code_test = self.assertEqual(get_response.status_code,201)


        #* testing with invalid input
        path = "/v1/api/user/register"
        data = {
            "username":"valar",
            "email":"valar@valar.com",
            "password":"Aa1122!!"
            }
        get_response = self.send_request.post(format="json",path=path,data=data)

        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,400)


    def test_generateOTP(self):
        admin_request,user_request = self.simple_setup()
        
        
        #*checking generate OTP
        path = "/v1/api/user/company_otp/create"
        data = {}
        response = admin_request.get(format="json",path=path,data=data)
        message_test = self.assertEqual(list(response.json().keys()),["success","otp_json"])
        status_code_test = self.assertEqual(response.status_code,200)

    def test_join_company(self):
        admin_request,user_request = self.simple_setup()
        path = "/v1/api/user/company_otp/create"
        data = {}
        response = admin_request.get(format="json",path=path,data=data)
        otp = response.json()["otp_json"]["code"]


        path = "/v1/api/user/company/join"
        data = {
            "admin_email":"admin@admin.com",
            "otp":otp,
            }
        response = user_request.post(format="json",path=path,data=data)
        message_test = self.assertEqual(list(response.json().keys()),["success","company_json"])
        status_code_test = self.assertEqual(response.status_code,201)


        #*trying to access this company another urls(before selected company)
        path = "/v1/api/department/get"
        data = {"all_departments":True}
        response = user_request.get(format="json",path=path,data=data)
        message_test = self.assertEqual(list(response.json().keys()),["error"])
        status_code_test = self.assertEqual(response.status_code,404)

        #*trying to access this company another urls(after selected company but blocked)
        #selecting company in the user
        simple_user = User.objects.get(email="simple@simple.com")
        company_obj = simple_user.companies.get(name="dev")
        simple_user.selected_company = company_obj
        simple_user.save()

        #trying to access the url after we selected the company but blocked
        path = "/v1/api/department/get"
        data = {"all_departments":True}
        response = user_request.get(format="json",path=path,data=data)
        message_test = self.assertEqual(list(response.json().keys()),["error"])
        status_code_test = self.assertEqual(response.status_code,404)



    def test_access_urls_successfully(self):

        #*first initialization
        admin_request,user_request = self.simple_setup()
        path = "/v1/api/user/company_otp/create"
        data = {}
        response = admin_request.get(format="json",path=path,data=data)
        otp = response.json()["otp_json"]["code"]


        path = "/v1/api/user/company/join"
        data = {
            "admin_email":"admin@admin.com",
            "otp":otp,
            }
        response = user_request.post(format="json",path=path,data=data)
        message_test = self.assertEqual(list(response.json().keys()),["success","company_json"])
        status_code_test = self.assertEqual(response.status_code,201)
        #*#######


        #unblocking the user and selecting the company
        simple_user = User.objects.get(email="simple@simple.com")
        company_obj = simple_user.blocked_by.get(name="dev")
        simple_user.blocked_by.remove(company_obj)
        simple_user.selected_company = company_obj
        simple_user.save()



        #creating department as an admin
        path = "/v1/api/department/create"
        data = {
            "name":"django",
            "rank":100,
            "salary":1000
        }
        admin_request.post(format="json",data=data,path=path)


        #* trying to access the url after we selected the company
        #* and unblocked the user
        #* and the department exists
        path = "/v1/api/department/get"
        data = {"all_departments":True}
        response = user_request.get(format="json",path=path,data=data)
        message_test = self.assertEqual(list(response.json().keys()),["success","department_json"])
        status_code_test = self.assertEqual(response.status_code,201)


