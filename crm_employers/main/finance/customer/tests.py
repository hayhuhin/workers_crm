from django.test import TestCase
from user.models import User
from employer.models import Employer,Department
from company.models import Company
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from custom_validation.tests import GeneralTestAPI


class CustomerTest(GeneralTestAPI):

    #*testing create with invalid data(GET REQUEST)
    def test_create_invalid_get(self):
        path="/v1/api/finance/customer/create"
        method = "get"

        #* empty json
        fields = {}
        response = {"message":["success","json_example"],"status":200}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["success","json_example"],"status":200}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing only one field
        fields = {"amount":1111}
        response = {"message":["success","json_example"],"status":200}
        only_one_field = {"fields":fields,"response":response,"method":method}

       #* date fields is incorrect  
        fields = {
            "amount":1111,
            "date_received":True,
            "description":"some desc",
            "payment_method":"bank_transfer",
            "customer_id":1
            }
        response = {"message":["success","json_example"],"status":200}
        incorrect_date = {"fields":fields,"response":response,"method":method}

        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_date,
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    def test_create_valid_get(self):
        path="/v1/api/finance/customer/create"
        method = "get"

       #* date fields is incorrect  
        fields = {
            "name":"mujanga",
            "email":"mujanga@mujanga.com",
            "phone_number":"121212",
            "address":"mujanga 12 at NY",
            "notes":"mujanga is some test customer",
            "customer_id":"112222333"
        }
        response = {"message":["success","json_example"],"status":200}
        incorrect_date = {"fields":fields,"response":response,"method":method}

        test_list = [
            incorrect_date
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #*testing create with invalid (POST REQUEST)
    def test_create_invalid_post(self):
        path="/v1/api/finance/customer/create"
        method = "post"

        
        #* empty json
        fields = {}
        response = {"message":["success","json_example"],"status":200}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["success","json_example"],"status":200}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing only one field
        fields = {"name":"only one name"}
        response = {"message":["success","json_example"],"status":200}
        only_one_field = {"fields":fields,"response":response,"method":method}

       #* customer id is not correct
        fields = {
            "name":"mujanga",
            "email":"mujanga@mujanga.com",
            "phone_number":"121212",
            "address":"mujanga 12 at NY",
            "notes":"mujanga is some test customer",
            "customer_id":True
            }
        response = {"message":["success","json_example"],"status":200}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}

        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_customer_id
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #*testing create with valid input (POST REQUEST) 
    def test_create_valid_post(self):
        path="/v1/api/finance/customer/create"
        method = "post"

       #* date fields is incorrect  
        fields = {
            "name":"mujanga",
            "email":"mujanga@mujanga.com",
            "phone_number":"121212",
            "address":"mujanga 12 at NY",
            "notes":"mujanga is some test customer",
            "customer_id":"112222333"
        }
        response = {"message":["success","json_example"],"status":200}
        incorrect_date = {"fields":fields,"response":response,"method":method}

        test_list = [
            incorrect_date
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)
