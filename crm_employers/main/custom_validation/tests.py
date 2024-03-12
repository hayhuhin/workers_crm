from django.test import TestCase
from user.models import User
from employer.models import Employer,Department
from company.models import Company
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group


# Create your tests here.


class TestAPIData:
    def __init__(self):
        self.email = "test@test.com"

    def create_user(self):
        self.user_obj = User.objects.create_user(username="test",email=self.email,password="Aa1122!!")
        self.user_obj.save()
        token = Token.objects.get(user=self.user_obj)
        return self.user_obj,token

    def create_custom_user(self,name,email,company_name):
        user_obj = User.objects.create_user(username=name,email=email,password="Aa1122!!")
        user_obj.save()
        token = Token.objects.get(user=user_obj)

        company_obj = Company.objects.create(name=company_name,description="description",address="address",admin_email=email)
        company_obj.save()

        user_obj.company = company_obj
        user_obj.save()


    def create_5_users(self,company_name):
        company_obj = Company.objects.get(name=company_name)
        
        user_list = ["arti","dani","yuval","asisa","banan"]
        for user in user_list:
            email = f"{user}@{user}.com"
            user_obj = User.objects.create_user(username=user,email=email,password="Aa1122!!")
            user_obj.company = company_obj
            user_obj.save()

    def create_5_employer(self,company_name,department_name,employers_list):
        company_obj = Company.objects.get(name=company_name)
        department_creation = self.create_department(company_name=company_name,department_name=department_name)
        


        user_object_list = {}
        for user in employers_list:
            email = f"{user}@{user}.com"
            user_obj = User.objects.create_user(username=user,email=email,password="Aa1122!!")
            user_obj.company = company_obj
            user_obj.save()
            user_object_list[user] = user_obj
        
        #* getting the first one
        department_obj = company_obj.department_set.get(name=department_name)
        for name,obj in user_object_list.items():
            create_data = {"user":obj,"first_name":obj.username,"last_name":obj.username,"phone":"121212","email":obj.email,"department":department_obj,"company":obj.company}
            emp_creation = Employer.objects.create(**create_data)
            emp_creation.save()





    def delete_user(self):
        # for user in User.objects.all():
        #     user.delete()
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


    def create_department(self,company_name,department_name):
        company_obj = Company.objects.get(name=company_name)
        department_obj = Department.objects.create(name=department_name,salary=3000,company=company_obj)



    


    def delete_company(self):
        company_obj = Company.objects.get(admin_email=self.user_obj.email)
        company_obj.delete()


# Create your tests here.
class GeneralTestAPI(TestCase):

    def setUp(self):
        self.APIClassTest = TestAPIData()
        self.created_user = self.APIClassTest.create_user()
        self.token = self.created_user[1]
        self.user_info = self.created_user[0]
        self.headers = {"content_type":"application/json"}

        self.send_request = APIClient()
        self.send_request.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def tearDown(self):
        self.APIClassTest.delete_user()
        # self.APIClassTest.delete_company()
        # pass


    def generic_tests(self,path,custom_method=None,custom_fields=None):
        json_format = "json"
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        self.APIClassTest.create_5_employer(company_name="test_company",department_name="test_department",employers_list=["qq","ww","ee","rr","tt"])
        self.APIClassTest.create_5_employer(company_name="django_dev",department_name="test_department",employers_list=["aa","ss","dd","ff","gg"])
        self.APIClassTest.create_5_users(company_name="test_company")
        self.APIClassTest.create_department(company_name="test_company",department_name="test_company_department")
        self.APIClassTest.create_department(company_name="django_dev",department_name="django_dev_department")
        
        
        if custom_method:
            if custom_method == "get":
                #* empty json(GET REQUEST)
                empty_json = {}
                get_response = self.send_request.get(format=json_format,path=path,data=empty_json)
                message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
                status_code_test = self.assertEqual(get_response.status_code,404)

                #* invalid field name(GET REQUEST)
                invalid_field_name = {"invalid":"invalid@invalid.com"}
                get_response = self.send_request.get(format=json_format,path=path,data=invalid_field_name)
                message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
                status_code_test = self.assertEqual(get_response.status_code,404)

            if custom_method == "post":
                #* empty json(POST REQUEST)
                empty_json = {}
                get_response = self.send_request.post(format=json_format,path=path,data=empty_json)
                message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
                status_code_test = self.assertEqual(get_response.status_code,404)

                #* invalid field name(POST REQUEST)
                invalid_field_name = {"invalid":"invalid@invalid.com"}
                get_response = self.send_request.post(format=json_format,path=path,data=invalid_field_name)
                message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
                status_code_test = self.assertEqual(get_response.status_code,404)



        if not custom_fields:
            #* empty json(GET REQ`UEST)
            empty_json = {}
            get_response = self.send_request.get(format=json_format,path=path,data=empty_json)
            message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
            status_code_test = self.assertEqual(get_response.status_code,404)

            #* empty json(POST REQUEST)
            empty_json = {}
            get_response = self.send_request.post(format=json_format,path=path,data=empty_json)
            message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
            status_code_test = self.assertEqual(get_response.status_code,404)


            #* invalid field name(GET REQUEST)
            invalid_field_name = {"invalid":"invalid@invalid.com"}
            get_response = self.send_request.get(format=json_format,path=path,data=invalid_field_name)
            message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
            status_code_test = self.assertEqual(get_response.status_code,404)

            #* invalid field name(POST REQUEST)
            invalid_field_name = {"invalid":"invalid@invalid.com"}
            get_response = self.send_request.post(format=json_format,path=path,data=invalid_field_name)
            message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
            status_code_test = self.assertEqual(get_response.status_code,404)

        if custom_fields:
            #* empty json(GET REQUEST)
            for test_data in custom_fields:
                fields = test_data["fields"]
                response = test_data["response"]
                method = test_data["method"]
                
                if method == "get":
                    get_response = self.send_request.get(format=json_format,path=path,data=fields)
                    print(get_response.json())
                    message_test = self.assertEqual(list(get_response.json().keys()),response["message"])
                    status_code_test = self.assertEqual(get_response.status_code,response["status"])
                
                if method == "post":
                    get_response = self.send_request.post(format=json_format,path=path,data=fields)
                    print(get_response.json())
                    message_test = self.assertEqual(list(get_response.json().keys()),response["message"])
                    status_code_test = self.assertEqual(get_response.status_code,response["status"])

