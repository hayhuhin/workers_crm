from django.test import TestCase
from user.models import User
from employer.models import Employer,Department
from company.models import Company
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from custom_validation.tests import GeneralTestAPI


class LeadsTest(GeneralTestAPI):

    #! testing create lead operations
    #* testing create with invalid input (GET REQUEST)
    def test_create_invalid_get(self):
        path="/v1/api/employer/lead/create"
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
