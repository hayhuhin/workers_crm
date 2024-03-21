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
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}


        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing only one field
        fields = {"name":"only one name"}
        response = {"message":["error","required_fields"],"status":404}
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
        response = {"message":["error"],"status":404}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}


       #* another company customer
        fields = {
            "name":"partner1",
            "email":"mujanga@mujanga.com",
            "phone_number":"121212",
            "address":"mujanga 12 at NY",
            "notes":"mujanga is some test customer",
            "customer_id":"11"
            }
        response = {"message":["success","customer_json"],"status":200}
        another_company_customer = {"fields":fields,"response":response,"method":method}


       #* existing current comapny customer
        fields = {
            "name":"radco1",
            "email":"mujanga@mujanga.com",
            "phone_number":"121212",
            "address":"mujanga 12 at NY",
            "notes":"mujanga is some test customer",
            "customer_id":"1"
            }
        response = {"message":["error"],"status":404}
        existing_customer = {"fields":fields,"response":response,"method":method}



       #* existing current comapny customer_name
        fields = {
            "name":"radco1",
            "email":"mujanga@mujanga.com",
            "phone_number":"121212",
            "address":"mujanga 12 at NY",
            "notes":"mujanga is some test customer",
            "customer_id":"44"
            }
        response = {"message":["error"],"status":404}
        existing_customer_name = {"fields":fields,"response":response,"method":method}


       #* existing current comapny customer_name
        fields = {
            "name":"some new customer",
            "email":"mujanga@mujanga.com",
            "phone_number":"121212",
            "address":"mujanga 12 at NY",
            "notes":"mujanga is some test customer",
            "customer_id":"1"
            }
        response = {"message":["error"],"status":404}
        existing_customer_id = {"fields":fields,"response":response,"method":method}


        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_customer_id,
            another_company_customer,
            existing_customer,
            existing_customer_name,
            existing_customer_id
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
        response = {"message":["success","customer_json"],"status":200}
        valid_input = {"fields":fields,"response":response,"method":method}

        test_list = [
            valid_input
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing delete invalid get
    def test_delete_invalid_get(self):
        path="/v1/api/finance/customer/delete"
        method = "get"

        
        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}


        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing invalid name
        fields = {"name":"invalid name"}
        response = {"message":["error"],"status":404}
        only_one_field = {"fields":fields,"response":response,"method":method}

       #* customer id is invalid
        fields = {
            "name":"radco1",
            "customer_id":True
            }
        response = {"message":["error"],"status":404}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}


       #* another company customer
        fields = {
            "name":"partner1",
            "email":"partner1@partner1.com",
            "phone_number":"112233",
            "address":"partner address",
            "customer_id":11
            }
        response = {"message":["error"],"status":404}
        another_company_customer = {"fields":fields,"response":response,"method":method}



       #* invalid email
        fields = {
            "name":"radco1",
            "email":"mujanga@mujanga.com",
            "phone_number":"112233",
            "address":"partner address",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        existing_customer_name = {"fields":fields,"response":response,"method":method}


       #* invalid phone number
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "phone_number":"111111",
            "address":"partner address",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        existing_customer_id = {"fields":fields,"response":response,"method":method}


       #* invalid address
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "phone_number":"112233",
            "address":"invalid address",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        invalid_address = {"fields":fields,"response":response,"method":method}



       #* invalid address
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "phone_number":"112233",
            "address":"partner address",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        invalid_notes = {"fields":fields,"response":response,"method":method}



       #* invalid customer_id
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "phone_number":"112233",
            "address":"partner address",
            "customer_id":999999
            }
        response = {"message":["error"],"status":404}
        invalid_customer_id = {"fields":fields,"response":response,"method":method}



        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_customer_id,
            another_company_customer,
            existing_customer_name,
            existing_customer_id,
            invalid_address,
            invalid_notes,
            invalid_customer_id
            ]
        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    def test_delete_valid_get(self):
        path="/v1/api/finance/customer/delete"
        method = "get"

        
        #* passing valid name
        fields = {"name":"radco1"}
        response = {"message":["success","customer_json"],"status":200}
        only_one_field = {"fields":fields,"response":response,"method":method}


       #* valid customer id
        fields = {
            "name":"radco1",
            "customer_id":0
            }
        response = {"message":["success","customer_json"],"status":200}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}


       #* valid email
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            }
        response = {"message":["success","customer_json"],"status":200}
        existing_customer_name = {"fields":fields,"response":response,"method":method}


       #* phone number
        fields = {
            "phone_number":"112233",
            }
        response = {"message":["success","customer_json"],"status":200}
        existing_customer_id = {"fields":fields,"response":response,"method":method}


       #* valid address
        fields = {
            "address":"radco1 address",
            }
        response = {"message":["success","customer_json"],"status":200}
        invalid_address = {"fields":fields,"response":response,"method":method}


        test_list = [
            only_one_field,
            incorrect_customer_id,
            existing_customer_name,
            existing_customer_id,
            invalid_address,
            ]
        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)

    #*testing delete with invalid input(POST REQUEST)
    def test_delete_invalid_post(self):
        path="/v1/api/finance/customer/delete"
        method = "post"

        
        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}


        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing invalid name
        fields = {
            "email":"invalid@invalid.com",
            "customer_id":1
            }
        response = {"message":["required_fields"],"status":404}
        only_one_field = {"fields":fields,"response":response,"method":method}


       #* invalid customer id
        fields = {
            "email":"radco1",
            "customer_id":99
            }
        response = {"message":["error"],"status":404}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}


       #* another company customer
        fields = {
            "email":"partner1@partner1.com",
            "customer_id":10,
            }
        response = {"message":["error"],"status":404}
        another_company_customer = {"fields":fields,"response":response,"method":method}

        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_customer_id,
            another_company_customer,
            ]
        
        test_list = []        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing delete with valid input(POST REQUEST)
    def test_delete_valid_post(self):
        path="/v1/api/finance/customer/delete"
        method = "post"

        
        #* valid input
        fields = {
            "email":"radco1@radco1.com",
            "customer_id":0,
            }
        response = {"message":["success","customer_json"],"status":200}
        valid_input1 = {"fields":fields,"response":response,"method":method}


        #* valid input2
        fields = {
            "email":"radco2@radco2.com",
            "customer_id":1,
            }
        response = {"message":["success","customer_json"],"status":200}
        valid_input2 = {"fields":fields,"response":response,"method":method}


        #* valid input3
        fields = {
            "email":"partner1@partner1.com",
            "customer_id":10,
            }
        response = {"message":["error",],"status":404}
        valid_input3 = {"fields":fields,"response":response,"method":method}

        test_list = [valid_input1,valid_input2,valid_input3]        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing update with invalid input(GET REQUEST)
    def test_update_invalid_get(self):
        path="/v1/api/finance/customer/update"
        method = "get"

        
        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}


        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing invalid name
        fields = {"name":"invalid name"}
        response = {"message":["error"],"status":404}
        only_one_field = {"fields":fields,"response":response,"method":method}

       #* customer id is invalid
        fields = {
            "name":"radco1",
            "customer_id":True
            }
        response = {"message":["error"],"status":404}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}


       #* another company customer
        fields = {
            "name":"partner1",
            "email":"partner1@partner1.com",
            "phone_number":"112233",
            "address":"partner address",
            "customer_id":11
            }
        response = {"message":["error"],"status":404}
        another_company_customer = {"fields":fields,"response":response,"method":method}



       #* invalid email
        fields = {
            "name":"radco1",
            "email":"mujanga@mujanga.com",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        existing_customer_name = {"fields":fields,"response":response,"method":method}


       #* invalid customer_id
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "customer_id":999999
            }
        response = {"message":["error"],"status":404}
        invalid_customer_id = {"fields":fields,"response":response,"method":method}



        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_customer_id,
            another_company_customer,
            existing_customer_name,
            invalid_customer_id
            ]
        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)

    def test_update_valid_get(self):
        path="/v1/api/finance/customer/update"
        method = "get"

        
        #* passing valid name
        fields = {"name":"radco1"}
        response = {"message":["success","customer_json"],"status":200}
        only_one_field = {"fields":fields,"response":response,"method":method}


       #* valid customer id
        fields = {
            "name":"radco1",
            "customer_id":0
            }
        response = {"message":["success","customer_json"],"status":200}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}


       #* valid email
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            }
        response = {"message":["success","customer_json"],"status":200}
        existing_customer_name = {"fields":fields,"response":response,"method":method}


       #* phone number
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "customer_id":0
            }
        response = {"message":["success","customer_json"],"status":200}
        existing_customer_id = {"fields":fields,"response":response,"method":method}


        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "customer_id":"0"            }
        response = {"message":["success","customer_json"],"status":200}
        str_customer_id = {"fields":fields,"response":response,"method":method}



        test_list = [
            only_one_field,
            incorrect_customer_id,
            existing_customer_name,
            str_customer_id,
            existing_customer_id,
            ]
        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)



    #*testing delete with invalid input(POST REQUEST)
    def test_update_invalid_post(self):
        path="/v1/api/finance/customer/update"
        method = "post"

        
        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}


        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing invalid name
        fields = {
            "email":"invalid@invalid.com",
            "customer_id":1,
            "update_data":{"name":"new_name"}
            }
        response = {"message":["error","required_fields"],"status":404}
        only_one_field = {"fields":fields,"response":response,"method":method}


       #* invalid customer id
        fields = {
            "email":"radco1",
            "customer_id":99,
            "update_data":{"name":"new_name"}
            }
        response = {"message":["error"],"status":404}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}


       #* another company customer
        fields = {
            "email":"partner1@partner1.com",
            "customer_id":10,
            "update_data":{"name":"new_name"}

            }
        response = {"message":["error"],"status":404}
        another_company_customer = {"fields":fields,"response":response,"method":method}


       #* empty update_data
        fields = {
            "email":"radco1@radco1.com",
            "customer_id":0,
            "update_data":{}
            }
        response = {"message":["error"],"status":404}
        empty_update_data = {"fields":fields,"response":response,"method":method}

        #*existing email in update data
        fields = {
            "email":"radco1@radco1.com",
            "customer_id":0,
            "update_data":{"email":"radco2@radco2.com"}
            }
        response = {"message":["error"],"status":404}
        update_data_existing_email = {"fields":fields,"response":response,"method":method}


        #*existing name in update data
        fields = {
            "email":"radco1@radco1.com",
            "customer_id":0,
            "update_data":{"name":"radco2"}
            }
        response = {"message":["error"],"status":404}
        update_data_existing_name= {"fields":fields,"response":response,"method":method}

        #*invalid field type in update data
        fields = {
            "email":"radco1@radco1.com",
            "customer_id":0,
            "update_data":{"name":True}
            }
        response = {"message":["error"],"status":404}
        update_data_invalid_field_type = {"fields":fields,"response":response,"method":method}


        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_customer_id,
            another_company_customer,
            empty_update_data,
            update_data_existing_email,
            update_data_existing_name,
            update_data_invalid_field_type
            ]
        
        test_list = []        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    def test_update_valid_post(self):
        path="/v1/api/finance/customer/update"
        method = "post"

        
        #* valid input
        fields = {
            "email":"radco1@radco1.com",
            "customer_id":0,
            "update_data":{
                "name":"new_name",
                "email":"radco@radco.com",
                "phone_number":"new phone",
                "address":"new address 1212",
                "notes":"new notes",
                "customer_id":998899
            }}
        response = {"message":["success","customer_json"],"status":200}
        valid_input1 = {"fields":fields,"response":response,"method":method}


        #* valid input2
        fields = {
            "email":"radco2@radco2.com",
            "customer_id":1,
            "update_data":{
                "name":"new_name",
                "email":"radcoco@radcoco.com",
                "phone_number":"new phone",
                "address":"new address 1212",
                "notes":"new notes",
            }}
        response = {"message":["success","customer_json"],"status":200}
        valid_input2 = {"fields":fields,"response":response,"method":method}


        #* valid input3
        fields = {
            "email":"radco4@radco4.com",
            "customer_id":3,
            "update_data":{
                "phone_number":"new phone",
                "address":"new address 1212",
                "notes":"new notes",
            }}
        response = {"message":["success","customer_json"],"status":200}
        valid_input3 = {"fields":fields,"response":response,"method":method}

        test_list = [valid_input1,valid_input2,valid_input3]        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)



    #* testing get with invalid input(GET REQUEST)
    def test_get_invalid_get(self):
        path="/v1/api/finance/customer/get"
        method = "get"

        
        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}


        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field = {"fields":fields,"response":response,"method":method}


        #* passing invalid name
        fields = {"name":"invalid name"}
        response = {"message":["error"],"status":404}
        only_one_field = {"fields":fields,"response":response,"method":method}

       #* customer id is invalid
        fields = {
            "name":"radco1",
            "customer_id":True
            }
        response = {"message":["error"],"status":404}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}


       #* another company customer
        fields = {
            "name":"partner1",
            "email":"partner1@partner1.com",
            "phone_number":"112233",
            "address":"partner address",
            "customer_id":11
            }
        response = {"message":["error"],"status":404}
        another_company_customer = {"fields":fields,"response":response,"method":method}



       #* invalid email
        fields = {
            "name":"radco1",
            "email":"mujanga@mujanga.com",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        existing_customer_name = {"fields":fields,"response":response,"method":method}


       #* invalid customer_id
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "customer_id":999999
            }
        response = {"message":["error"],"status":404}
        invalid_customer_id = {"fields":fields,"response":response,"method":method}



        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_customer_id,
            another_company_customer,
            existing_customer_name,
            invalid_customer_id
            ]
        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)

    def test_get_valid_get(self):
        path="/v1/api/finance/customer/get"
        method = "get"

        
        #* passing valid name
        fields = {"name":"radco1"}
        response = {"message":["success","customer_json"],"status":200}
        only_one_field = {"fields":fields,"response":response,"method":method}


       #* valid customer id
        fields = {
            "name":"radco1",
            "customer_id":0
            }
        response = {"message":["success","customer_json"],"status":200}
        incorrect_customer_id = {"fields":fields,"response":response,"method":method}


       #* valid email
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            }
        response = {"message":["success","customer_json"],"status":200}
        existing_customer_name = {"fields":fields,"response":response,"method":method}


       #* phone number
        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "customer_id":0
            }
        response = {"message":["success","customer_json"],"status":200}
        existing_customer_id = {"fields":fields,"response":response,"method":method}


        fields = {
            "name":"radco1",
            "email":"radco1@radco1.com",
            "customer_id":"0"            }
        response = {"message":["success","customer_json"],"status":200}
        str_customer_id = {"fields":fields,"response":response,"method":method}



        test_list = [
            only_one_field,
            incorrect_customer_id,
            existing_customer_name,
            str_customer_id,
            existing_customer_id,
            ]
        
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


