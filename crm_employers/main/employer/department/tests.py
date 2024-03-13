from django.test import TestCase
from user.models import User
from employer.models import Employer,Department
from company.models import Company
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from custom_validation.tests import GeneralTestAPI

class DepartmentTest(GeneralTestAPI):



    #* testing department create (GET REQUEST)
    def test_create_get_request(self):
        path="/v1/api/department/create"
        method = "get"

        
        #*valid input
        fields = {}
        response = {"message":["success","example_json"],"status":200}
        valid_input = {"fields":fields,"response":response,"method":method}
        
        #*invalid input
        fields = {"invalid":"invalid"}
        response = {"message":["success","example_json"],"status":200}
        invalid_input = {"fields":fields,"response":response,"method":method}
        

        test_list = [valid_input,invalid_input]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)

    #* testing create with invalid input (POST REQUEST)
    def test_create_invalid_input(self):
        path="/v1/api/department/create"
        method = "post"

        
        #*empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}
        
        #*invalid fieldname
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field_name= {"fields":fields,"response":response,"method":method}
        
        #* passing only "name"
        fields = {"name":"only name"}
        response = {"message":["error","required_fields"],"status":404}
        one_field_only = {"fields":fields,"response":response,"method":method}
        
        #* trying to create department that already exists
        fields = {"name":"test_department","rank":300,"salary":1000}
        response = {"message":["error"],"status":404}
        existing_department = {"fields":fields,"response":response,"method":method}
        
        #* extra fields
        fields = {"extra":"extra","name":"new department","rank":300,"salary":1000}
        response = {"message":["error","required_fields"],"status":404}
        extra_field = {"fields":fields,"response":response,"method":method}
        


        test_list = [empty_json,invalid_field_name,one_field_only,existing_department,extra_field]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)

    #* testing create department with valid input(POST REQUEST)
    def test_create_valid_input(self):
        path="/v1/api/department/create"
        method = "post"

        #* valid fields
        fields = {"name":"new department","rank":300,"salary":1000}
        response = {"message":["success","department_json"],"status":201}
        valid_fields = {"fields":fields,"response":response,"method":method}
        

        
        #* trying to create department that already exists in another company
        fields = {"name":"django_dev_department","rank":300,"salary":1000}
        response = {"message":["success","department_json"],"status":201}
        existing_department_another_company = {"fields":fields,"response":response,"method":method}
        
        test_list = [existing_department_another_company,valid_fields]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #! testing delete department
    #testing delete with invalid input(GET REQUEST)
    def test_delete_invalid_input(self):
        path="/v1/api/department/delete"
        method = "get"

        #* invalid name
        fields = {"name":"invalid department"}
        response = {"message":["error"],"status":404}
        invalid_name = {"fields":fields,"response":response,"method":method}

        #* invalid all_departments
        fields = {"all_departments":121}
        response = {"message":["error"],"status":404}
        invalid_all_departments = {"fields":fields,"response":response,"method":method}


        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid field name
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field_name = {"fields":fields,"response":response,"method":method}

        #* trying to get another company department
        fields = {"name":"django_dev_department"}
        response = {"message":["error"],"status":404}
        another_company_department = {"fields":fields,"response":response,"method":method}



        test_list = [invalid_name,invalid_all_departments,empty_json,invalid_field_name,another_company_department]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)
    
    
    #*testing delete with valid input(GET REQUEST)
    def test_delete_valid_input_get(self):
        path="/v1/api/department/delete"
        method = "get"

        #* valid name input
        fields = {"name":"test_department"}
        response = {"message":["success","department_json"],"status":200}
        valid_name = {"fields":fields,"response":response,"method":method}

        #* valid all_departments input
        fields = {"all_departments":"true"}
        response = {"message":["success","department_json"],"status":200}
        valid_all_departments = {"fields":fields,"response":response,"method":method}

        test_list = [valid_name,valid_all_departments]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)
    

    #* testing delete with invalid input (POST REQUEST)
    def test_delete_invalid_input_post(self):
        path="/v1/api/department/delete"
        method = "post"


        #* invalid name
        fields = {"name":"invalid department"}
        response = {"message":["error"],"status":404}
        invalid_name = {"fields":fields,"response":response,"method":method}

        #* invalid all_departments
        fields = {"all_departments":121}
        response = {"message":["error","required_fields"],"status":404}
        invalid_all_departments = {"fields":fields,"response":response,"method":method}


        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid field name
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field_name = {"fields":fields,"response":response,"method":method}

        #* trying to delete another company department
        fields = {"name":"django_dev_department"}
        response = {"message":["error"],"status":404}
        another_company_department = {"fields":fields,"response":response,"method":method}



        test_list = [invalid_name,invalid_all_departments,empty_json,invalid_field_name,another_company_department]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing delete with valid input fields(POST REQUEST)
    def test_delete_valid_input_post(self):
        path="/v1/api/department/delete"
        method = "post"


        #* valid name
        fields = {"name":"test_department"}
        response = {"message":["success"],"status":201}
        valid_name = {"fields":fields,"response":response,"method":method}

        test_list = [valid_name]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #! testing update department section
    #* testing update with invalid fields(GET REQUEST)
    def test_update_invalid_fields_get(self):
        path="/v1/api/department/update"
        method = "get"


        #* invalid name
        fields = {"name":"invalid department"}
        response = {"message":["error"],"status":404}
        invalid_name = {"fields":fields,"response":response,"method":method}

        #* invalid update_data value
        fields = {"update_data":121}
        response = {"message":["error"],"status":404}
        invalid_update_data = {"fields":fields,"response":response,"method":method}

        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid field name
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field_name = {"fields":fields,"response":response,"method":method}

        #* trying to delete another company department
        fields = {"name":"django_dev_department"}
        response = {"message":["error"],"status":404}
        another_company_department = {"fields":fields,"response":response,"method":method}


        #* invalid update data 
        fields = {"name":"test_department","update_data":121}
        response = {"message":["error"],"status":404}
        invalid_update_data_dict_value = {"fields":fields,"response":response,"method":method}



        test_list = [
            invalid_name,
            invalid_update_data,
            empty_json,
            invalid_field_name,
            another_company_department,
            invalid_update_data_dict_value
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing update with valid fields (GET REQUEST)
    def test_update_valid_fields_get(self):
        path="/v1/api/department/update"
        method = "get"

        #* valid name
        fields = {"name":"test_department"}
        response = {"message":["success","department_json"],"status":200}
        valid_name = {"fields":fields,"response":response,"method":method}

        test_list = [valid_name]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    #* testing update with invalid fields (POST REQUEST)
    def test_update_invalid_fields_post(self):
        path="/v1/api/department/update"
        method = "post"

        #* invalid name
        fields = {"name":"invalid department"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_name = {"fields":fields,"response":response,"method":method}

        #* invalid update_data value
        fields = {"update_data":121}
        response = {"message":["error","required_fields"],"status":404}
        invalid_update_data = {"fields":fields,"response":response,"method":method}

        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid field name
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field_name = {"fields":fields,"response":response,"method":method}

        #* trying to update another company department
        fields = {"name":"django_dev_department"}
        response = {"message":["error","required_fields"],"status":404}
        another_company_department = {"fields":fields,"response":response,"method":method}


        #* invalid update data 
        fields = {"name":"test_department","update_data":121}
        response = {"message":["error","required_fields"],"status":404}
        invalid_update_data_dict_value = {"fields":fields,"response":response,"method":method}



        test_list = [
            invalid_name,
            invalid_update_data,
            empty_json,
            invalid_field_name,
            another_company_department,
            invalid_update_data_dict_value
            ]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)


    def test_update_valid_post(self):
        path="/v1/api/department/update"
        method = "post"


        #*valid update_post
        fields = {"name":"test_department","update_data":{
            "name":"new_department",
            "rank":3000,
            "salary":1000
            }}
        response = {"message":["success","department_json"],"status":201}
        valid_fields = {"fields":fields,"response":response,"method":method}
        


        test_list = [valid_fields]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)



    #! testing get operations 
    #* testing get with invalid fields (GET REQUEST)
    def test_get_invalid_get(self):
        path="/v1/api/department/get"
        method = "get"


        #* invalid name
        fields = {"name":"invalid department"}
        response = {"message":["error"],"status":404}
        invalid_name = {"fields":fields,"response":response,"method":method}

        #* invalid all_departments
        fields = {"all_departments":121}
        response = {"message":["error","required_fields"],"status":404}
        invalid_all_departments = {"fields":fields,"response":response,"method":method}


        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        empty_json = {"fields":fields,"response":response,"method":method}

        #* invalid field name
        fields = {"invalid":"invalid"}
        response = {"message":["error","required_fields"],"status":404}
        invalid_field_name = {"fields":fields,"response":response,"method":method}

        #* trying to delete another company department
        fields = {"name":"django_dev_department"}
        response = {"message":["error"],"status":404}
        another_company_department = {"fields":fields,"response":response,"method":method}



        test_list = [invalid_name,invalid_all_departments,empty_json,invalid_field_name,another_company_department]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)

