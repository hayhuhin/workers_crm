from django.test import TestCase
from user.models import User
from company.models import Company
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group



class TestAPIData:
    def __init__(self,user_email):
        self.email = user_email

    def create_user(self):
        self.user_obj = User.objects.create_user(username="test",email=self.email,password="Aa1122!!")
        self.user_obj.save()
        token = Token.objects.get(user=self.user_obj)
        return self.user_obj,token

    def delete_user(self):
        self.user_obj.delete()


    def permit_admin(self):
        it,med = Group.objects.create(name="IT_permission"),Group.objects.create(name="medium_permission"),
        self.user_obj.groups.add(it,med)

    def create_company(self):
        user_obj = User.objects.get(email=self.email)
        company_data = {
            "name":"test_company",
            "description":"for testing purposes only",
            "address":"test address 1212",
            "admin_email":user_obj.email
                }
        compnay_obj = Company.objects.create(**company_data)
        #* creating the relationship uf the creator and the company
        self.user_obj.company = compnay_obj
        self.user_obj.save()

        #* creating another mopck companies for testing
        mock_user_obj = User.objects.create_user(username="john",email="jonh@john.com",password="Aa1122!!")
        mock_user_obj.save()

        company_data = {
            "name":"django_dev",
            "description":"for testing purposes only",
            "address":"test address 1212",
            "admin_email":mock_user_obj.email
                }
        compnay_obj = Company.objects.create(**company_data)
        #* creating the relationship uf the creator and the company
        mock_user_obj.company = compnay_obj
        mock_user_obj.save()

    def delete_company(self):
        company_obj = Company.objects.get(admin_email=self.user_obj.email)
        company_obj.delete()


# Create your tests here.
class TestCompanyAPI(TestCase):
    def setUp(self):
        self.APIClassTest = TestAPIData(user_email="test@test.com")
        self.created_user = self.APIClassTest.create_user()
        self.token = self.created_user[1]
        self.user_info = self.created_user[0]
        self.headers = {"content_type":"application/json"}

        self.send_request = APIClient()
        self.send_request.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')


    def tearDown(self):
        self.APIClassTest.delete_user()
        # self.APIClassTest.delete_company()

    #* authorization test
    def test_admin_cant_access_other_companies(self):
    #* this test is to check that this admin user cant access other admins companies
    
        #* give the user admin permissions
        self.APIClassTest.permit_admin()

        #* create mock company
        self.APIClassTest.create_company()
        new_data = {"name":"django_dev","update_data":{"name":"gg"}}#django_dev is already exists but with another admin
        post_response = self.send_request.post(format="json",path="/v1/api/company/update",data=new_data)
        message_test = self.assertEqual(list(post_response.json().keys()),["error"])
        status_code_test = self.assertEqual(post_response.status_code,404)





    #* testing the creation of the company 
    def test_wrong_inputs_create(self):
        #* give the user the admin permission
        self.APIClassTest.permit_admin()

        #* passed empty name (POST REQUEST)
        data = {"name":"","description":"no desc","address":"no addr"}
        response = self.send_request.post(format="json",path="/v1/api/company/create",data=data)
        message_test = self.assertEqual(list(response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(response.status_code,404)
        

        #* passed empty description
        data = {"name":"test","description":"","address":"no addr"}
        response = self.send_request.post(format="json",path="/v1/api/company/create",data=data)
        message_test = self.assertEqual(list(response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(response.status_code,404)
        

        # #* passed empty address
        data = {"name":"test","description":"","address":""}
        response = self.send_request.post(format="json",path="/v1/api/company/create",data=data)
        message_test = self.assertEqual(list(response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(response.status_code,404)
        

        # #* passed empty json
        data = {}
        response = self.send_request.post(format="json",path="/v1/api/company/create",data=data)
        message_test = self.assertEqual(list(response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(response.status_code,404)

        
    #* test of successfully creation(POST REQUEST)
    def test_success_create(self):
        #* give the user admin permission
        self.APIClassTest.permit_admin()

        #* passed empty name
        data = {"name":"test","description":"no desc","address":"no addr"}
        response = self.send_request.post(format="json",path="/v1/api/company/create",data=data)
        print(response.json())
        message_test = self.assertEqual(list(response.json().keys()),["success"])
        status_code_test = self.assertEqual(response.status_code,201)
        
    
    
    #* tests for delete company(GET REQUESTS)
    def test_get_wrong_inputs_delete(self):
        #* give the user admin permissions
        self.APIClassTest.permit_admin()

        #* creating company mock
        self.APIClassTest.create_company()

        #*passing empty json
        data = {}
        #*get test
        get_response = self.send_request.get(format="json",path="/v1/api/company/delete",data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,404)

        #*not existing company
        data = {"test":"qwerqwr"}
        # #* get test
        sa = self.send_request.get(format="json",path="/v1/api/company/delete",data=data)
        message_test = self.assertEqual(list(sa.json().keys()),["error"])
        status_code_test = self.assertEqual(sa.status_code,404)
        
        #* invalid fields input
        data = {"id":1}
        #* get test
        get_response = self.send_request.get(format="json",path="/v1/api/company/delete",data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,404)
        

    #* tests for delete company(POST REQUESTS)
    def test_post_wrong_inputs_delete(self):
        #* give the user admin permissions
        self.APIClassTest.permit_admin()


        #*passing empty json
        data = {}


        post_response = self.send_request.post(format="json",path="/v1/api/company/delete",data=data)
        message_test = self.assertEqual(list(post_response.json().keys()),["error"])
        status_code_test = self.assertEqual(post_response.status_code,404)

        #*not existing company
        data = {"test":"qwerqwr"}

        post_response = self.send_request.post(format="json",path="/v1/api/company/delete",data=data)
        message_test = self.assertEqual(list(post_response.json().keys()),["error"])
        status_code_test = self.assertEqual(post_response.status_code,404)
        
        #* invalid fields input
        data = {"id":1}

        post_response = self.send_request.post(format="json",path="/v1/api/company/delete",data=data)
        message_test = self.assertEqual(list(post_response.json().keys()),["error"])
        status_code_test = self.assertEqual(post_response.status_code,404)
        

    #* testing delete company successfully(POST REQUEST)
    def test_success_delete(self):
        #* give the user admin permissions
        self.APIClassTest.permit_admin()

        #* create mock company
        self.APIClassTest.create_company()

        data = {"name":"test_company"}
        post_response = self.send_request.post(format="json",path="/v1/api/company/delete",data=data)
        message_test = self.assertEqual(list(post_response.json().keys()),["success"])
        status_code_test = self.assertEqual(post_response.status_code,201)
        
    #* test of valid company name(GET REQUEST)
    def test_get_valid_input(self):

        #* give the user admin permissions
        self.APIClassTest.permit_admin()

        #* create mock company
        self.APIClassTest.create_company()


        data = {"name":"test_company"}
        get_response = self.send_request.get(format="json",path="/v1/api/company/update",data=data)

        message_test = self.assertEqual(list(get_response.json().keys()),["success","company_json"])
        status_code_test = self.assertEqual(get_response.status_code,200)



    #* tests for update company section(GET REQUEST)
    def test_get_wrong_inputs_update(self):

        #* give the user admin permissions
        self.APIClassTest.permit_admin()

        #* create mock company
        self.APIClassTest.create_company()


        #* invalid key field
        data = {"id":"test_company"}
        get_response = self.send_request.get(format="json",path="/v1/api/company/update",data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(get_response.status_code,404)

        #* invalid value field
        data = {"name":"test"}
        get_response = self.send_request.get(format="json",path="/v1/api/company/update",data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,404)

        #* invalid value field(empty)
        data = {"name":""}
        get_response = self.send_request.get(format="json",path="/v1/api/company/update",data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,404)

        #* invalid empty json
        data = {}
        get_response = self.send_request.get(format="json",path="/v1/api/company/update",data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(get_response.status_code,404)


    #* tests with wrong input in update company(POST REQUEST)
    def test_post_wrong_inputs_update(self):
    
        #* give the user admin permissions
        self.APIClassTest.permit_admin()

        #* create mock company
        self.APIClassTest.create_company()

        #*invalid name input(company not exists with this name)
        new_data = {"name":"wrong_company"}
        post_response = self.send_request.post(format="json",path="/v1/api/company/update",data=new_data)
        message_test = self.assertEqual(list(post_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(post_response.status_code,404)


        #*invalid update_data input (not existing fields)
        new_data = {"name":"test_company","update_data":{"wrong":"wrong123"}}
        post_response = self.send_request.post(format="json",path="/v1/api/company/update",data=new_data)
        
        message_test = self.assertEqual(list(post_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(post_response.status_code,404)
        
        #*invalid update_data input (empty json)
        new_data = {"name":"test_company","update_data":{}}
        post_response = self.send_request.post(format="json",path="/v1/api/company/update",data=new_data)
        message_test = self.assertEqual(list(post_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(post_response.status_code,404)

        #*invalid update_data input(not passing update_data field)
        new_data = {"name":"test_company"}
        post_response = self.send_request.post(format="json",path="/v1/api/company/update",data=new_data)
        
        message_test = self.assertEqual(list(post_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(post_response.status_code,404)


    def test_post_success(self):

        #* give the user admin permissions
        self.APIClassTest.permit_admin()

        #* create mock company
        self.APIClassTest.create_company()


        #* invalid key field
        data = {"name":"test_company","update_data":{"name":"tested_successfully_company"}}
        get_response = self.send_request.post(format="json",path="/v1/api/company/update",data=data)
        message_test = self.assertEqual(list(get_response.json().keys()),["success","updated_data"])
        status_code_test = self.assertEqual(get_response.status_code,201)



    #* testing the get company operation
    def test_get_company_invalid_input(self):
        #* give the user admin permissions
        self.APIClassTest.permit_admin()

        #* create mock company
        self.APIClassTest.create_company()

        #*invalid name input(company not exists with this name)
        new_data = {"name":"wrong_company"}
        post_response = self.send_request.get(format="json",path="/v1/api/company/get",data=new_data)
        message_test = self.assertEqual(list(post_response.json().keys()),["error"])
        status_code_test = self.assertEqual(post_response.status_code,404)



        #*invalid field name
        new_data = {"id":1}
        post_response = self.send_request.get(format="json",path="/v1/api/company/get",data=new_data)
        message_test = self.assertEqual(list(post_response.json().keys()),["error"])
        status_code_test = self.assertEqual(post_response.status_code,404)

        #*someone elses company
        new_data = {"name":"django_dev"}
        post_response = self.send_request.get(format="json",path="/v1/api/company/get",data=new_data)

        message_test = self.assertEqual(list(post_response.json().keys()),["error"])
        status_code_test = self.assertEqual(post_response.status_code,404)


    def test_get_company_valid_input(self):
        #* give the user admin permissions
        self.APIClassTest.permit_admin()

        #* create mock company
        self.APIClassTest.create_company()

        #*valid company name
        new_data = {"name":"test_company"}
        post_response = self.send_request.get(format="json",path="/v1/api/company/get",data=new_data)

        message_test = self.assertEqual(list(post_response.json().keys()),["success","company_json"])
        status_code_test = self.assertEqual(post_response.status_code,200)

