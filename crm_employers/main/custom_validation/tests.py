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
        self.request_args = self.initialize()
        
        self.user_obj = self.request_args[0]
        self.token = self.request_args[1]
        self.header_args = {"content_type":"application/json"}

    def initialize(self):
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
            
            #* first company customers
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
            
            #* second company customers
            for index,name in enumerate(second_names):
                customer_obj = Customer.objects.create(
                name=name,
                email=f"{name}@{name}.com",
                phone_number="112233",
                address="partner address",
                notes=f"{name} notes",
                customer_id=index+10,
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

        #*first company outcome
        for index,amount in enumerate(amount_list):
            #* creating outcome 
            outcome_obj = Outcome.objects.create(
                user = first_users[index],
                date_time = dates_list[index],
                category = "spending",
                amount = amount,
                description = f"some description",
                payment_method = "cash",
                vendor = "some some",
                project_or_department = "project"
                )
            outcome_obj.save()


        #*second company outcome
        for index,amount in enumerate(second_amount):
            #* creating outcome 
            outcome_obj = Outcome.objects.create(
                user = second_users[index],
                date_time = dates_list[index],
                category = "spending",
                amount = amount,
                description = f"some description",
                payment_method = "cash",
                vendor = "some some",
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

        #* creating another mock companies for testing
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


    def generate_mock_data(self):
        #this class will create the needed mock data:
        #1.15 users(5 in one company as employers and 5 in another and 5 users not as employers)
        #2.two companies
        #3.in each company two departments
        #4.creating customer to each company
        #5.creating mock income and outcome records to each company
        #6.the user is permitted as admin
        
        #?adding permission to our admin user
        admin_permissions = ["IT_permission","medium_permission"]
        finance_permission = ["finance_full_permission","finance_view_permission","finance_update_permission"]
        permission_objects = []
        for admin in admin_permissions:
            group_object = Group.objects.create(name=admin)
            permission_objects.append(group_object)
        
        for finance in finance_permission:
            group_object  = Group.objects.create(name=finance)
            permission_objects.append(group_object)

        for permission in permission_objects:
            self.user_obj.groups.add(permission)


        #*here im creating two companies
            
        company_data = {
            "name":"test_company",
            "description":"for testing purposes only",
            "address":"test address 1212",
            "admin_email":self.user_obj.email
                }
        first_company_obj = Company.objects.create(**company_data)
        
        #* creating the relationship uf the creator and the company
        self.user_obj.company = first_company_obj
        self.user_obj.save()

        #* creating another mock companies for testing
        mock_user_obj = User.objects.create_user(username="john",email="jonh@john.com",password="Aa1122!!")
        mock_user_obj.save()
        company_data = {
            "name":"django_dev",
            "description":"for testing purposes only",
            "address":"test address 1212",
            "admin_email":mock_user_obj.email
                }
        second_company_object = Company.objects.create(**company_data)
        #* creating the relationship uf the creator and the company
        mock_user_obj.company = second_company_object
        mock_user_obj.save()


        #*here im creating 15 users in total
        #5 normal users to a company
        #5 users as employers to first company
        #5 users as employers to second company
        
        normal_user_list = ["arti","dani","yuval","asisa","banan"]
        for user in normal_user_list:
            email = f"{user}@{user}.com"
            user_obj = User.objects.create_user(username=user,email=email,password="Aa1122!!")
            user_obj.company = first_company_obj
            user_obj.save()

        #* for creating employers we need departments first
        comp_1_dep_1 = Department.objects.create(name="test_department",salary=3000,company=first_company_obj)
        comp_1_dep_2 = Department.objects.create(name="test_company_department",salary=3000,company=first_company_obj)

        comp_2_dep_1 = Department.objects.create(name="test_department",salary=3000,company=second_company_object)
        comp_2_dep_2 = Department.objects.create(name="django_dev_department",salary=3000,company=second_company_object)

        first_comp_users = ["qq","ww","ee","rr","tt"]
        second_comp_users = ["aa","ss","dd","ff","gg"]

        #*creating the users first
        first_user_object_list = {}
        for user in first_comp_users:
            email = f"{user}@{user}.com"
            user_obj = User.objects.create_user(username=user,email=email,password="Aa1122!!")
            user_obj.company = first_company_obj
            user_obj.save()
            first_user_object_list[user] = user_obj
        
        #* here im creating the employers for them
        for name,obj in first_user_object_list.items():
            create_data = {"user":obj,"first_name":obj.username,"last_name":obj.username,"phone":"121212","email":obj.email,"department":comp_1_dep_1,"company":obj.company}
            emp_creation = Employer.objects.create(**create_data)
            emp_creation.save()

        #*creating first the employers for the second company
        second_user_object_list = {}
        for user in second_comp_users:
            email = f"{user}@{user}.com"
            user_obj = User.objects.create_user(username=user,email=email,password="Aa1122!!")
            user_obj.company = second_company_object
            user_obj.save()
            second_user_object_list[user] = user_obj
        
        #* here im creating the employers for them
        for name,obj in second_user_object_list.items():
            create_data = {"user":obj,"first_name":obj.username,"last_name":obj.username,"phone":"121212","email":obj.email,"department":comp_2_dep_1,"company":obj.company}
            emp_creation = Employer.objects.create(**create_data)
            emp_creation.save()
        
        
        #* now im creating the customers for each company
        first_customer_names = ["radco1","radco2","radco3","radco4","radco5"]
        second_customer_names = ["partner1","partner2","partner3","partner4","partner5"]
        
        #* first company customers
        for index,name in enumerate(first_customer_names):
            first_comp_customer = Customer.objects.create(
            name=name,
            email=f"{name}@{name}.com",
            phone_number="112233",
            address="radco inter",
            notes=f"{name} notes",
            customer_id=index,
            company=first_company_obj
            )
            first_comp_customer.save()
        
        #* second company customers
        for index,name in enumerate(second_customer_names):
            second_comp_customer = Customer.objects.create(
            name=name,
            email=f"{name}@{name}.com",
            phone_number="112233",
            address="partner address",
            notes=f"{name} notes",
            customer_id=index+10,
            company=second_company_object
            )
            second_comp_customer.save()


        #* here im creating the finance mock income and outcome records
            

        
        first_users = first_company_obj.user_set.all()
        second_users = second_company_object.user_set.all()

        first_customer = first_company_obj.customer_set.all()
        second_customer = second_company_object.customer_set.all()

        dates_list = ["2024-01-01","2024-02-01","2024-03-01","2024-04-01","2024-05-01",]
        amount_list = ["1111","2222","3333","4444","5555"]
        second_amount = ["6666","7777","8888","9999","1111"]

        #TODO:the bug is in this loop of the creation of Income record

        #*first company income
        for index,amount in enumerate(amount_list):
                
            #* creating income
            income_obj = Income.objects.create(
                user=first_users[index],
                amount=amount,
                date_received=dates_list[index],
                description="first company",
                payment_method="credit_card",
                customer=first_customer[index],
                company=first_company_obj
                )
            income_obj.save()




        #*second company income
        for index,amount in enumerate(second_amount):
                
            #* creating income
            income_obj = Income.objects.create(
                user=second_users[index],
                amount=amount,
                date_received=dates_list[index],
                description="some desc",
                payment_method="credit_card",
                customer=second_customer[index],
                company=second_company_object
                )
            income_obj.save()


        #*first company outcome
        for index,amount in enumerate(amount_list):
            #* creating outcome 
            outcome_obj = Outcome.objects.create(
                user = first_users[index],
                date_received = dates_list[index],
                category = "spending",
                amount = amount,
                description = f"some description",
                payment_method = "cash",
                vendor = "some some",
                project_or_department = "project",
                company=first_company_obj
                )
            outcome_obj.save()


        #*second company outcome
        for index,amount in enumerate(second_amount):
            #* creating outcome 
            outcome_obj = Outcome.objects.create(
                user = second_users[index],
                date_received = dates_list[index],
                category = "spending",
                amount = amount,
                description = f"some description",
                payment_method = "cash",
                vendor = "some some",
                project_or_department = "project",
                company=second_company_object
                )
            outcome_obj.save()


        #? adding income records to test@test.com user
        for index,amount in enumerate(amount_list):
                
            #* creating income
            income_obj = Income.objects.create(
                user=self.user_obj,
                amount=amount,
                date_received=dates_list[index],
                description="first company",
                payment_method="credit_card",
                customer=first_customer[index],
                company=first_company_obj
                )
            
            income_obj.save()

        #?  adding outcome records to test@test.com user
        for index,amount in enumerate(amount_list):
            #* creating outcome 
            outcome_obj = Outcome.objects.create(
                user = self.user_obj,
                date_received = dates_list[index],
                category = "spending",
                amount = amount,
                description = f"some description",
                payment_method = "cash",
                vendor = "some some",
                project_or_department = "project",
                company=first_company_obj
                )
            outcome_obj.save()


        first_company_obj.save()
        second_company_object.save()
            







# Create your tests here.
class GeneralTestAPI(TestCase):

    def setUp(self):
        self.APIClassTest = TestAPIData()
        # self.created_user = self.APIClassTest.initialize()
        self.user_info = self.APIClassTest.user_obj
        self.token = self.APIClassTest.token
        self.headers = self.APIClassTest.header_args

        self.send_request = APIClient()
        self.send_request.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def tearDown(self):
        self.APIClassTest.delete_user()



    def generic_tests(self,path,custom_method=None,custom_fields=None):
        json_format = "json"
        self.APIClassTest.generate_mock_data()


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

