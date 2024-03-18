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
        response = {"message":["success","income_json"],"status":200}
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

       #* another company customer_id
        fields = {
            "customer_id":12
            }
        response = {"message":["error"],"status":404}
        another_company_customer_id= {"fields":fields,"response":response,"method":method}

       #* another company customer_name
        fields = {
            "customer_name":"partner1"
            }
        response = {"message":["error"],"status":404}
        another_company_customer_name = {"fields":fields,"response":response,"method":method}


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

       #* passing two different customer data together
        fields = {
            "customer_name":"radco1",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        two_customer_wrong_input = {"fields":fields,"response":response,"method":method}


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
            another_company_customer_id,
            another_company_customer_name,
            another_created_by,
            another_company_created_by,
            two_customer_wrong_input,
            invalid_customer_name,
            invalid_payment_id
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #*testing delete with valid input (GET REQUEST)
    def test_delete_valid_get(self):
        path="/v1/api/finance/income/delete"
        method = "get"
      

        #* passing valid customer_name
        fields = {
            "customer_name":"radco3"
            }
        response = {"message":["success","income_json"],"status":200}
        valid_customer_name = {"fields":fields,"response":response,"method":method}


        #* passing valid customer_name
        fields = {
            "customer_id":"4"
            }
        response = {"message":["success","income_json"],"status":200}
        valid_customer_id = {"fields":fields,"response":response,"method":method}


        #* passing valid created_by
        fields = {
            "created_by":"test@test.com"
            }
        response = {"message":["success","income_json"],"status":200}
        valid_created_by = {"fields":fields,"response":response,"method":method}


        #* passing valid date_received
        fields = {
            "date_received":"2024-01-01"
            }
        response = {"message":["success","income_json"],"status":200}
        valid_date_received = {"fields":fields,"response":response,"method":method}

   

        test_list= [valid_customer_name,valid_customer_id,valid_created_by,valid_date_received]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #! for now its not possible to test this because the db always erases 
    #! and i cant get the random income id that generated each time we
    #! create an income in our database
    #*testing delete with invalid input(POST REQUEST)
    def test_delete_invalid_post(self):
        path="/v1/api/finance/income/delete"
        method = "post"
      

        # #* passing invalid income id 
        # fields = {
        #     "income_id":True
        #     }
        # response = {"message":["error"],"status":404}
        # invalid_income_id = {"fields":fields,"response":response,"method":method}

   
        # #* passing field name
        # fields = {
        #     "invalid":"invalid"
        #     }
        # response = {"message":["error"],"status":404}
        # invalid_field_name = {"fields":fields,"response":response,"method":method}


        # #* passing income_id of another company
        # fields = {
        #     "income_id":"another company"
        #     }
        # response = {"message":["error"],"status":404}
        # another_company_income_id = {"fields":fields,"response":response,"method":method}

        # #* passing empty json
        # fields = {}
        # response = {"message":["error","required_fields"],"status":404}
        # another_company_income_id = {"fields":fields,"response":response,"method":method}



        # test_list = [
        #     invalid_income_id,
        #     invalid_field_name,
        #     another_company_income_id
        #     ]
        # valid_test = self.generic_tests(path=path,custom_fields=test_list)

    #* testing update with invalid fields(GET REQUEST)
    def test_update_invalid_get(self):
        path="/v1/api/finance/income/update"
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
        response = {"message":["success","income_json"],"status":200}
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

       #* another company customer_id
        fields = {
            "customer_id":12
            }
        response = {"message":["error"],"status":404}
        another_company_customer_id= {"fields":fields,"response":response,"method":method}

       #* another company customer_name
        fields = {
            "customer_name":"partner1"
            }
        response = {"message":["error"],"status":404}
        another_company_customer_name = {"fields":fields,"response":response,"method":method}


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

       #* passing two different customer data together
        fields = {
            "customer_name":"radco1",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        two_customer_wrong_input = {"fields":fields,"response":response,"method":method}


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
            another_company_customer_id,
            another_company_customer_name,
            another_created_by,
            another_company_created_by,
            two_customer_wrong_input,
            invalid_customer_name,
            invalid_payment_id
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)



    #!cant test update valid data and invalid data as post 
        
    #*testing get with invalid fields (GER REQUEST)
    def test_get_invalid_get(self):
        path="/v1/api/finance/income/get"
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
        response = {"message":["success","income_json"],"status":200}
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

       #* another company customer_id
        fields = {
            "customer_id":12
            }
        response = {"message":["error"],"status":404}
        another_company_customer_id= {"fields":fields,"response":response,"method":method}

       #* another company customer_name
        fields = {
            "customer_name":"partner1"
            }
        response = {"message":["error"],"status":404}
        another_company_customer_name = {"fields":fields,"response":response,"method":method}


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

       #* passing two different customer data together
        fields = {
            "customer_name":"radco1",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        two_customer_wrong_input = {"fields":fields,"response":response,"method":method}


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
            another_company_customer_id,
            another_company_customer_name,
            another_created_by,
            another_company_created_by,
            two_customer_wrong_input,
            invalid_customer_name,
            invalid_payment_id
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)



    #*testing get with valid input(GET REQUEST)
    def test_get_valid_get(self):
        path="/v1/api/finance/income/get"
        method = "get"
            

        #* passing valid customer_name
        fields = {
            "customer_name":"radco3"
            }
        response = {"message":["success","income_json"],"status":200}
        valid_customer_name = {"fields":fields,"response":response,"method":method}


        #* passing valid customer_name
        fields = {
            "customer_id":"4"
            }
        response = {"message":["success","income_json"],"status":200}
        valid_customer_id = {"fields":fields,"response":response,"method":method}


        #* passing valid created_by
        fields = {
            "created_by":"test@test.com"
            }
        response = {"message":["success","income_json"],"status":200}
        valid_created_by = {"fields":fields,"response":response,"method":method}


        #* passing valid date_received
        fields = {
            "date_received":"2024-01-01"
            }
        response = {"message":["success","income_json"],"status":200}
        valid_date_received = {"fields":fields,"response":response,"method":method}

   

        test_list= [valid_customer_name,valid_customer_id,valid_created_by,valid_date_received]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)





class OutcomeTest(GeneralTestAPI):

    #*testing create with invalid data(GET REQUEST)
    def test_create_invalid_get(self):
        path="/v1/api/finance/outcome/create"
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
        path="/v1/api/finance/outcome/create"
        method = "get"

        #* valid fields
        fields = {}
        response = {"message":["success","json_example"],"status":200}
        invalid_field = {"fields":fields,"response":response,"method":method}


        test_list = [invalid_field]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing create with invalid input (POST REQUEST)
    def test_create_invalid_post(self):
        path="/v1/api/finance/outcome/create"
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
            "date_received":True,
            "category":"gogo",
            "amount":1111,
            "description":"some desc",
            "payment_method":"credit_card",
            "vendor":"vend",
            "project_or_department":"project"
            }
        response = {"message":["error"],"status":404}
        incorrect_date = {"fields":fields,"response":response,"method":method}

       #* invalid amount
        fields = {
            "date_received":"2024-12-12",
            "category":"test",
            "amount":True,
            "description":"some desc",
            "payment_method":"bank_transfer",
            "vendor":"test",
            "project_or_department":"project"
            }
        response = {"message":["error"],"status":404}
        invalid_amount= {"fields":fields,"response":response,"method":method}

       #* another company customer
        fields = {
            "date_received":"2024-12-12",
            "category":"test",
            "amount":True,
            "description":"some desc",
            "payment_method":"bank_transfer",
            "vendor":"test",
            "project_or_department":"project"
            }
        response = {"message":["error"],"status":404}
        another_company_customer= {"fields":fields,"response":response,"method":method}

        test_list = [
            empty_json,
            invalid_field,
            only_one_field,
            incorrect_date,
            invalid_amount,
            another_company_customer
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing create with valid input(POST REQUEST)
    def test_create_valid_post(self):
        path="/v1/api/finance/outcome/create"
        method = "post"


        #* another company customer
        fields = {
            "date_received":"2024-12-12",
            "category":"test",
            "amount":1212,
            "description":"some desc",
            "payment_method":"bank_transfer",
            "vendor":"test",
            "project_or_department":"project"
            }
        response = {"message":["success","outcome_json"],"status":201}
        valid_input= {"fields":fields,"response":response,"method":method}

        test_list = [valid_input]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing delete with invalid fields(GET REQUEST)
    def test_delete_invalid_get(self):
        path="/v1/api/finance/outcome/delete"
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
        response = {"message":["success","outcome_json"],"status":200}
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

       #* another company customer_id
        fields = {
            "customer_id":12
            }
        response = {"message":["error"],"status":404}
        another_company_customer_id= {"fields":fields,"response":response,"method":method}

       #* another company customer_name
        fields = {
            "customer_name":"partner1"
            }
        response = {"message":["error"],"status":404}
        another_company_customer_name = {"fields":fields,"response":response,"method":method}


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

       #* passing two different customer data together
        fields = {
            "customer_name":"radco1",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        two_customer_wrong_input = {"fields":fields,"response":response,"method":method}


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
            another_company_customer_id,
            another_company_customer_name,
            another_created_by,
            another_company_created_by,
            two_customer_wrong_input,
            invalid_customer_name,
            invalid_payment_id
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #*testing delete with valid input (GET REQUEST)
    def test_delete_valid_get(self):
        path="/v1/api/finance/outcome/delete"
        method = "get"
      

        #* passing valid customer_name
        fields = {
            "customer_name":"radco3"
            }
        response = {"message":["success","outcome_json"],"status":200}
        valid_customer_name = {"fields":fields,"response":response,"method":method}


        #* passing valid customer_name
        fields = {
            "customer_id":"4"
            }
        response = {"message":["success","outcome_json"],"status":200}
        valid_customer_id = {"fields":fields,"response":response,"method":method}


        #* passing valid created_by
        fields = {
            "created_by":"test@test.com"
            }
        response = {"message":["success","outcome_json"],"status":200}
        valid_created_by = {"fields":fields,"response":response,"method":method}


        #* passing valid date_received
        fields = {
            "date_received":"2024-01-01"
            }
        response = {"message":["success","outcome_json"],"status":200}
        valid_date_received = {"fields":fields,"response":response,"method":method}

   

        test_list= [valid_customer_name,valid_customer_id,valid_created_by,valid_date_received]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #! for now its not possible to test this because the db always erases 
    #! and i cant get the random income id that generated each time we
    #! create an income in our database
    #*testing delete with invalid input(POST REQUEST)
    def test_delete_invalid_post(self):
        path="/v1/api/finance/outcome/delete"
        method = "post"
      

        # #* passing invalid income id 
        # fields = {
        #     "income_id":True
        #     }
        # response = {"message":["error"],"status":404}
        # invalid_income_id = {"fields":fields,"response":response,"method":method}

   
        # #* passing field name
        # fields = {
        #     "invalid":"invalid"
        #     }
        # response = {"message":["error"],"status":404}
        # invalid_field_name = {"fields":fields,"response":response,"method":method}


        # #* passing income_id of another company
        # fields = {
        #     "income_id":"another company"
        #     }
        # response = {"message":["error"],"status":404}
        # another_company_income_id = {"fields":fields,"response":response,"method":method}

        # #* passing empty json
        # fields = {}
        # response = {"message":["error","required_fields"],"status":404}
        # another_company_income_id = {"fields":fields,"response":response,"method":method}



        # test_list = [
        #     invalid_income_id,
        #     invalid_field_name,
        #     another_company_income_id
        #     ]
        # valid_test = self.generic_tests(path=path,custom_fields=test_list)

    #* testing update with invalid fields(GET REQUEST)
    def test_update_invalid_get(self):
        path="/v1/api/finance/outcome/update"
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
        response = {"message":["success","outcome_json"],"status":200}
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

       #* another company customer_id
        fields = {
            "customer_id":12
            }
        response = {"message":["error"],"status":404}
        another_company_customer_id= {"fields":fields,"response":response,"method":method}

       #* another company customer_name
        fields = {
            "customer_name":"partner1"
            }
        response = {"message":["error"],"status":404}
        another_company_customer_name = {"fields":fields,"response":response,"method":method}


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

       #* passing two different customer data together
        fields = {
            "customer_name":"radco1",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        two_customer_wrong_input = {"fields":fields,"response":response,"method":method}


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
            another_company_customer_id,
            another_company_customer_name,
            another_created_by,
            another_company_created_by,
            two_customer_wrong_input,
            invalid_customer_name,
            invalid_payment_id
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)



    #!cant test update valid data and invalid data as post 
        
    #*testing get with invalid fields (GER REQUEST)
    def test_get_invalid_get(self):
        path="/v1/api/finance/outcome/get"
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
        response = {"message":["success","outcome_json"],"status":200}
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

       #* another company customer_id
        fields = {
            "customer_id":12
            }
        response = {"message":["error"],"status":404}
        another_company_customer_id= {"fields":fields,"response":response,"method":method}

       #* another company customer_name
        fields = {
            "customer_name":"partner1"
            }
        response = {"message":["error"],"status":404}
        another_company_customer_name = {"fields":fields,"response":response,"method":method}


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

       #* passing two different customer data together
        fields = {
            "customer_name":"radco1",
            "customer_id":1
            }
        response = {"message":["error"],"status":404}
        two_customer_wrong_input = {"fields":fields,"response":response,"method":method}


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
            another_company_customer_id,
            another_company_customer_name,
            another_created_by,
            another_company_created_by,
            two_customer_wrong_input,
            invalid_customer_name,
            invalid_payment_id
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)



    #*testing get with valid input(GET REQUEST)
    def test_get_valid_get(self):
        path="/v1/api/finance/outcome/get"
        method = "get"
            

        #* passing valid customer_name
        fields = {
            "customer_name":"radco3"
            }
        response = {"message":["success","outcome_json"],"status":200}
        valid_customer_name = {"fields":fields,"response":response,"method":method}


        #* passing valid customer_name
        fields = {
            "customer_id":"4"
            }
        response = {"message":["success","outcome_json"],"status":200}
        valid_customer_id = {"fields":fields,"response":response,"method":method}


        #* passing valid created_by
        fields = {
            "created_by":"test@test.com"
            }
        response = {"message":["success","outcome_json"],"status":200}
        valid_created_by = {"fields":fields,"response":response,"method":method}


        #* passing valid date_received
        fields = {
            "date_received":"2024-01-01"
            }
        response = {"message":["success","outcome_json"],"status":200}
        valid_date_received = {"fields":fields,"response":response,"method":method}

   

        test_list= [valid_customer_name,valid_customer_id,valid_created_by,valid_date_received]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)




