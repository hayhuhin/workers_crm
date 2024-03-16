from django.test import TestCase
from user.models import User
from employer.models import Employer,Department
from company.models import Company
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from custom_validation.tests import GeneralTestAPI


class IncomeTest(GeneralTestAPI):

    #*testing create with invalid data(GET REQUEST)
    def test_create_invalid_get(self):
        path="/v1/api/finance/income/create"
        method = "get"

        #* empty json
        fields = {}
        response = {"message":["success","json_example"],"status":200}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["success","json_example"],"status":200}
        invalid_field = {"fields":fields,"response":response,"method":method}


        test_list = [empty_json,invalid_field]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #*testing create with valid data(GET REQUEST)
    def test_create_valid_get(self):
        path="/v1/api/finance/income/create"
        method = "get"

        #* valid fields
        fields = {}
        response = {"message":["success","json_example"],"status":200}
        invalid_field = {"fields":fields,"response":response,"method":method}


        test_list = [invalid_field]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing create with invalid input (POST REQUEST)
    def test_create_invalid_post(self):
        path="/v1/api/finance/income/create"
        method = "post"

        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing only one field
        fields = {"amount":1111}
        response = {"message":["error","required_fields"],"status":404}
        only_one_field = {"fields":fields,"response":response,"method":method}

       #* date fields is incorrect  
        fields = {
            "amount":1111,
            "date_received":True,
            "description":"some desc",
            "payment_method":"bank_transfer",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        incorrect_date = {"fields":fields,"response":response,"method":method}

       #* invalid customer_id
        fields = {
            "amount":1111,
            "date_received":"2024-12-12",
            "description":"some desc",
            "payment_method":"bank_transfer",
            "customer_id":99
            }
        response = {"message":["error"],"status":404}
        invalid_customer_id= {"fields":fields,"response":response,"method":method}

       #* another company customer
        fields = {
            "amount":1111,
            "date_received":"2024-12-12",
            "description":"some desc",
            "payment_method":"bank_transfer",
            "customer_id":12
            }
        response = {"message":["error"],"status":404}
        another_company_customer= {"fields":fields,"response":response,"method":method}

        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_date,
            invalid_customer_id,
            another_company_customer
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing create with valid input(POST REQUEST)
    def test_create_valid_post(self):
        path="/v1/api/finance/income/create"
        method = "post"
      

             #* another company customer
        fields = {
            "amount":1111,
            "date_received":"2024-12-12",
            "description":"some desc",
            "payment_method":"bank_transfer",
            "customer_id":3
            }
        response = {"message":["success","income_json"],"status":201}
        valid_input= {"fields":fields,"response":response,"method":method}

        test_list = [valid_input]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing delete with invalid fields(GET REQUEST)
    def test_delete_invalid_get(self):
        path="/v1/api/finance/income/delete"
        method = "get"
      
        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid field name
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing only one field
        fields = {"date_received":"2024-01-01"}
        response = {"message":["error","required_fields"],"status":404}
        only_one_field = {"fields":fields,"response":response,"method":method}

       #* date fields is incorrect  
        fields = {
            "date_received":True
            }
        response = {"message":["error"],"status":404}
        incorrect_date = {"fields":fields,"response":response,"method":method}

       #* invalid customer_id
        fields = {
            "date_received":"2024-12-12",
            "customer_id":99
            }
        response = {"message":["error"],"status":404}
        invalid_customer_id= {"fields":fields,"response":response,"method":method}

       #* another company customer
        fields = {
            "customer_id":12
            }
        response = {"message":["error"],"status":404}
        another_company_customer= {"fields":fields,"response":response,"method":method}


       #* invalid created_by
        fields = {
            "created_by":"invalid@invalid.com"
            }
        response = {"message":["error"],"status":404}
        another_created_by= {"fields":fields,"response":response,"method":method}


       #* invalid created_by from another company
        fields = {
            "created_by":"aa@aa.com"
            }
        response = {"message":["error"],"status":404}
        another_company_created_by= {"fields":fields,"response":response,"method":method}



       #* invalid customer name
        fields = {
            "customer_name":"invalid"
            }
        response = {"message":["error"],"status":404}
        invalid_customer_name = {"fields":fields,"response":response,"method":method}

       #* invalid payment_id
        fields = {
            "payment_id":"123123"
            }
        response = {"message":["error"],"status":404}
        invalid_payment_id = {"fields":fields,"response":response,"method":method}



        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_date,
            invalid_customer_id,
            another_company_customer,
            another_created_by,
            another_company_created_by,
            invalid_customer_name,
            invalid_payment_id
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)

