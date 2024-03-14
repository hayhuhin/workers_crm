from django.test import TestCase
from user.models import User
from employer.models import Employer,Department
from company.models import Company
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from finance.models import Customer,Income,Outcome


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

    def create_customer_mock_data(self,company_name,second_company_name):
            company_obj = Company.objects.get(name=company_name)
            second_company_obj = Company.objects.get(name=second_company_name)
            customer_names = ["radco1","radco2","radco3","radco4","radco5"]
            second_names = ["partner1","partner2","partner3","partner4","partner5"]
            
            for index,name in enumerate(customer_names):
                customer_obj = Customer.objects.create(
                name=name,
                email=f"{name}@{name}.com",
                phone_number="112233",
                address="radco inter",
                notes=f"{name} notes",
                customer_id=index,
                company=company_obj
                )
                customer_obj.save()
            
            
            for index,name in enumerate(second_names):
                customer_obj = Customer.objects.create(
                name=name,
                email=f"{name}@{name}.com",
                phone_number="112233",
                address="partner address",
                notes=f"{name} notes",
                customer_id=index,
                company=second_company_obj
                )
                customer_obj.save()
            
    def create_finance_mock_data(self,company_name,second_company_name):
        company_obj = Company.objects.get(name=company_name)
        second_company_obj = Company.objects.get(name=second_company_name)
        customer_names = ["radco1","radco2","radco3","radco4","radco5"]
        second_names = ["partner1","partner2","partner3","partner4","partner5"]
        
        first_users = company_obj.user_set.all()
        second_users = second_company_obj.user_set.all()

        first_customer = company_obj.customer_set.all()
        second_customer = second_company_obj.customer_set.all()

        dates_list = ["2024-01-01","2024-02-01","2024-03-01","2024-04-01","2024-05-01",]
        amount_list = ["1111","2222","3333","4444","5555"]
        second_amount = ["6666","7777","8888","9999","1111"]

        #*first company income
        for index,amount in enumerate(amount_list):
                
            #* creating income
            income_obj = Income.objects.create(
                user=first_users[index],
                amount=amount,
                date_received=dates_list[index],
                description=f"{first_users[index].username}",
                payment_method="credit_card",
                customer=first_customer[index]
                )
            income_obj.save()
        
        #*second company income
        for index,amount in enumerate(second_amount):
                
            #* creating income
            income_obj = Income.objects.create(
                user=second_users[index],
                amount=amount,
                date_received=dates_list[index],
                description=f"{second_users[index].username}",
                payment_method="credit_card",
                customer=second_customer[index]
                )
            income_obj.save()

        #*fikrst company outcome
        for index,amount in enumerate(amount_list):
            #* creating outcome 
            outcome_obj = Outcome.objects.create(
                user = first_users[index],
                date_time = dates_list[index],
                category = "spendings",
                amount = amount,
                description = f"some description",
                payment_method = "cash",
                vendor = "somesome",
                project_or_department = "project"
                )
            outcome_obj.save()


        #*second company outcome
        for index,amount in enumerate(second_amount):
            #* creating outcome 
            outcome_obj = Outcome.objects.create(
                user = second_users[index],
                date_time = dates_list[index],
                category = "spendings",
                amount = amount,
                description = f"some description",
                payment_method = "cash",
                vendor = "somesome",
                project_or_department = "project"
                )
            outcome_obj.save()


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
        finance_full_per = Group.objects.create(name="finance_full_permission")
        finance_view_per = Group.objects.create(name="finance_view_permission")
        finance_update_per = Group.objects.create(name="finance_update_permission")
        self.user_obj.groups.add(it,med,finance_full_per,finance_update_per,finance_view_per)


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

        #TODO: sasasasa
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



    def generic_tests(self,path,custom_method=None,custom_fields=None):
        json_format = "json"
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        
        self.APIClassTest.create_5_employer(company_name="test_company",department_name="test_department",employers_list=["qq","ww","ee","rr","tt"])
        self.APIClassTest.create_5_employer(company_name="django_dev",department_name="test_department",employers_list=["aa","ss","dd","ff","gg"])
        self.APIClassTest.create_5_users(company_name="test_company")
        
        self.APIClassTest.create_department(company_name="test_company",department_name="test_company_department")
        self.APIClassTest.create_department(company_name="django_dev",department_name="django_dev_department")

        # self.APIClassTest.create_customer_mock_data(company_name="test_company",second_company_name="django_dev")
        # self.APIClassTest.create_finance_mock_data(company_name="test_company",second_company_name="django_dev")
        

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
                    error_message = {
                        "fields_passed":fields,
                        "response_passed":response,
                        "method_passed":method,
                        "API_response":get_response.json()
                        }
                    message_test = self.assertEqual(list(get_response.json().keys()),response["message"],msg=error_message)
                    status_code_test = self.assertEqual(get_response.status_code,response["status"],msg=error_message)
                
                if method == "post":
                    post_response = self.send_request.post(format=json_format,path=path,data=fields)
                    error_message = {
                        "fields_passed":fields,
                        "response_passed":response,
                        "method_passed":method,
                        "API_response":post_response.json()
                    }
                    message_test = self.assertEqual(list(post_response.json().keys()),response["message"],msg=error_message)
                    status_code_test = self.assertEqual(post_response.status_code,response["status"],msg=error_message)

