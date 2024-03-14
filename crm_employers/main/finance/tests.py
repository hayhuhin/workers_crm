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
        response = {"message":["success"],"status":200}
        empty_json = {"fields":fields,"response":response,"method":method}

        test_list = [empty_json]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)

        #* invalid fields
        fields = {"invalid":"invalid"}
        response = {"message":["success"],"status":200}
        invalid_field = {"fields":fields,"response":response,"method":method}

        test_list = [empty_json,invalid_field]
        valid_test = self.generic_tests(path=path,custom_fields=test_list)
