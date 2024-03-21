from django.test import TestCase
from user.models import User
from company.models import Company 
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import Group



class AdminUserTest(TestCase):

    def setUp(self):
        self.send_request = APIClient()

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
        print(get_response.json())
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


class SimpleUserTest(TestCase):


    def setUp(self):
        self.send_request = APIClient()

    def create_permissions(self):
        admin_permissions = ["admin_permission","IT_permission","medium_permission","finance_full_permission","finance_view_permission","finance_update_permission"]
        for permission in admin_permissions:
            group_obj = Group.objects.create(name=permission)
            group_obj.save()



    def create_admin_user(self,user_kwargs,company_kwargs):
        user_obj = User.objects.create(**user_kwargs)
        company_obj = Company.objects.create(**company_kwargs)
        user_obj.company = company_obj

        #* adding all admin permissions for our admin user
        admin_permissions = ["admin_permission","IT_permission","medium_permission","finance_full_permission","finance_view_permission","finance_update_permission"]
        for permission in admin_permissions:
            group_obj = Group.objects.get(name=permission)
            user_obj.groups.add(group_obj)
            user_obj.save()
        


        company_obj.save()


        admin_token = Token.objects.get(user=user_obj)
        return admin_token
    

    #*testing create user with invalid fields
    def test_create_invalid_post(self):
        #* first we initialize admin user
        #* and now we send the requests with the auth token
        self.create_permissions()
        
        user_1_kwargs = {
            "username":"radco1",
            "email":"radco1@radco1.com",
            "password":"Aa1122!!"
                       }
        company_1_kwargs = {
            "name":"radco1",
            "description":"radco1",
            "address":"radco1",
            "admin_email":"radco1@radco1.com",
        }
        
        #*first admin and company
        radco_1_token = self.create_admin_user(user_1_kwargs,company_1_kwargs)
        radco_1_request = APIClient()
        radco_1_request.credentials(HTTP_AUTHORIZATION=f'Token {radco_1_token}')
        
        user_2_kwargs = {
            "username":"radco2",
            "email":"radco2@radco2.com",
            "password":"Aa1122!!"
                       }

        company_2_kwargs = {
            "name":"radco2",
            "description":"radco2",
            "address":"radco2",
            "admin_email":"radco2@radco2.com",
        }
        #* second admin and company
        radco_2_token = self.create_admin_user(user_2_kwargs,company_2_kwargs)
        radco_2_request = APIClient()
        radco_2_request.credentials(HTTP_AUTHORIZATION=f'Token {radco_2_token}')



        #* radco 1 creating an employer 
        path = "/v1/api/user/create_user"
        data = {
            "username":"papa",
            "email":"qwert@qwert.com",
            "password":"Aa1122!!"
            }       
        first_response = radco_1_request.post(format="json",path=path,data=data)
        first_message = self.assertEqual(list(first_response.json().keys()),["success","user_json"])
        status_code_test = self.assertEqual(first_response.status_code,201)

        #* radco 2 creating an employer 
        path = "/v1/api/user/create_user"
        data = {
            "username":"papa",
            "email":"qwert@qwert.com",
            "password":"Aa1122!!"
            }       
        second_response = radco_2_request.post(format="json",path=path,data=data)
        print(second_response.json())
        second_message = self.assertEqual(list(second_response.json().keys()),["success","user_json"])
        status_code_test = self.assertEqual(second_response.status_code,201)

        first_response_company = first_response.json().get("company")
        print(first_response_company)

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

