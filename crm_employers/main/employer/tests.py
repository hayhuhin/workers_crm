from django.test import TestCase
from user.models import User
from employer.models import Employer,Department
from company.models import Company
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group



class TestAPIData:
    def __init__(self,user_email):
        self.email = user_email

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
class TestCompanyAPI(TestCase):
    def setUp(self):
        self.APIClassTest = TestAPIData(user_email="test@test.com")
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
                    # print(User.objects.all().values("email","company__name"))
                    print(get_response.json())
                    message_test = self.assertEqual(list(get_response.json().keys()),response["message"])
                    status_code_test = self.assertEqual(get_response.status_code,response["status"])
                if method == "post":
                    get_response = self.send_request.post(format=json_format,path=path,data=fields)
                    print(get_response.json())
                    message_test = self.assertEqual(list(get_response.json().keys()),response["message"])
                    status_code_test = self.assertEqual(get_response.status_code,response["status"])


    #* testing create employer(GET REQUEST)
    def test_create_employer(self):
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        self.APIClassTest.create_department(company_name=self.user_info.company.name,department_name="test_department")
        self.APIClassTest.create_5_users(company_name=self.user_info.company.name)


        new_data = {"first_name":"john","last_name":"doe","email":"john@john.com","phone":"123123123","department":1}
        response = self.send_request.get(format="json",path="/v1/api/employer/create",data=new_data)
        message_test = self.assertEqual(list(response.json().keys()),["error","json_example"])
        status_code_test = self.assertEqual(response.status_code,200)

    #* testing create employer(POST REQUEST)
    def test_create_employer_valid_fields(self):
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        self.APIClassTest.create_department(company_name=self.user_info.company.name,department_name="test_department")
        self.APIClassTest.create_5_users(company_name=self.user_info.company.name)


        new_data = {"first_name":"john","last_name":"doe","email":"arti@arti.com","phone":"123123123","department":"test_department"}
        response = self.send_request.post(format="json",path="/v1/api/employer/create",data=new_data)
        message_test = self.assertEqual(list(response.json().keys()),["success","employer_data"])
        status_code_test = self.assertEqual(response.status_code,201)



    #* testing create employer(POST REQUEST)
    def test_create_employer_invalid_fields(self):
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        self.APIClassTest.create_department(company_name=self.user_info.company.name,department_name="test_department")
        self.APIClassTest.create_5_users(company_name=self.user_info.company.name)

        #* invalid fields name
        new_data = {"name":"john","last_name":"doe","email":"john@john.com","phone":"123123123","department":"test_department"}
        response = self.send_request.post(format="json",path="/v1/api/employer/create",data=new_data)

        message_test = self.assertEqual(list(response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(response.status_code,404)

        #* invalid email
        new_data = {"first_name":"john","last_name":"doe","email":"invalid@email.com","phone":"123123123","department":"test_department"}
        response = self.send_request.post(format="json",path="/v1/api/employer/create",data=new_data)
        message_test = self.assertEqual(list(response.json().keys()),["error"])
        status_code_test = self.assertEqual(response.status_code,404)

        #* invalid department
        new_data = {"first_name":"john","last_name":"doe","email":"yuval@yuval.com","phone":"123123123","department":"invalid_department"}
        response = self.send_request.post(format="json",path="/v1/api/employer/create",data=new_data)
        message_test = self.assertEqual(list(response.json().keys()),["error"])
        status_code_test = self.assertEqual(response.status_code,404)


        #* missing fields
        new_data = {"first_name":"john","last_name":"doe","email":"john@john.com","department":"test_department"}
        response = self.send_request.post(format="json",path="/v1/api/employer/create",data=new_data)

        message_test = self.assertEqual(list(response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(response.status_code,404)


        #* trying to access another company department
        #*creating another department from another company
        self.APIClassTest.create_department(company_name="django_dev",department_name="django_department")

        #* trying to create employer from test company into another company department
        new_data = {"first_name":"john","last_name":"doe","email":"john@john.com","phone":"112211","department":"django_department"}
        response = self.send_request.post(format="json",path="/v1/api/employer/create",data=new_data)
        message_test = self.assertEqual(list(response.json().keys()),["error"])
        status_code_test = self.assertEqual(response.status_code,404)


        #* passing empty json

        #* trying to create employer from test company into another company department
        new_data = {}
        response = self.send_request.post(format="json",path="/v1/api/employer/create",data=new_data)
        message_test = self.assertEqual(list(response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(response.status_code,404)


    #* testing the get employer operations
    def test_get_employer_valid_fields(self):
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        self.APIClassTest.create_department(company_name=self.user_info.company.name,department_name="test_department")
        self.APIClassTest.create_5_users(company_name=self.user_info.company.name)

        new_data = {"all_employers":"true"}
        response = self.send_request.get(format="json",path="/v1/api/employer/get",data=new_data)
        message_test = self.assertEqual(list(response.json().keys()),["success","employer_json"])
        status_code_test = self.assertEqual(response.status_code,200)


        #* creating test employer
        create_data = {"first_name":"john","last_name":"doe","email":"arti@arti.com","phone":"123123123","department":"test_department"}
        post_response = self.send_request.post(format="json",path="/v1/api/employer/create",data=create_data)

        #*trying to get employer by email
        get_data = {"email":"arti@arti.com"}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/get",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["success","employer_json"])
        status_code_test = self.assertEqual(get_response.status_code,200)


    def test_get_employer_invalid_fields(self):
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        self.APIClassTest.create_5_employer(company_name="test_company",department_name="test_department",employers_list=["qq","ww","ee","rr","tt"])
        self.APIClassTest.create_5_employer(company_name="django_dev",department_name="django_test_department",employers_list=["aa","ss","dd","ff","gg"])

        #*trying to get employer from another company
        #* john from test_company trying to get aa@aa.com from django_dev company
        get_data = {"email":"aa@aa.com"}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/get",data=get_data)

        #* this checking that the test is correct and all employers for the test are created
        aa_exists = Employer.objects.filter(**get_data).exists()
        another_company_employer = self.assertEqual(aa_exists,True)

        #* this checking the result itself
        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,404)
        
    
        #*invalid email
        get_data = {"email":"invalid@email.com"}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/get",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,404)

        #*invalid field name
        get_data = {"invalid":"qq@qq.com"}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/get",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error","valid_fields"])
        status_code_test = self.assertEqual(get_response.status_code,404)

        #*passing both fields
        get_data = {"all_employers":"true","email":"qq@qq.com"}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/get",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["success","employer_json"])
        status_code_test = self.assertEqual(get_response.status_code,200)


        #*passing both fields
        get_data = {"email":"qq@qq.com","all_employers":"true",}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/get",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["success","employer_json"])
        status_code_test = self.assertEqual(get_response.status_code,200)

    #* testing delete employer(GET REQUEST)
    def test_valid_get_delete(self):
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        self.APIClassTest.create_5_employer(company_name="test_company",department_name="test_department",employers_list=["qq","ww","ee","rr","tt"])

        #*correct email
        get_data = {"email":"qq@qq.com"}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/delete",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["success","employer_json"])
        status_code_test = self.assertEqual(get_response.status_code,200)

    #*testing invalid delete inputs (GET REQUEST)
    def test_invalid_get_delete(self):
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        self.APIClassTest.create_5_employer(company_name="test_company",department_name="test_department",employers_list=["qq","ww","ee","rr","tt"])

        #*invalid email
        get_data = {"email":"aa@aa.com"}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/delete",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error"])
        status_code_test = self.assertEqual(get_response.status_code,404)



        #*invalid field name
        get_data = {"invalid":"invalid"}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/delete",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(get_response.status_code,404)


        #*empty json
        get_data = {}
        get_response = self.send_request.get(format="json",path="/v1/api/employer/delete",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["error","required_fields"])
        status_code_test = self.assertEqual(get_response.status_code,404)

    
    #* testing valid delete (POST REQUEST)
    def test_valid_post_delete(self):
        self.APIClassTest.permit_admin()
        self.APIClassTest.create_company()
        self.APIClassTest.create_5_employer(company_name="test_company",department_name="test_department",employers_list=["qq","ww","ee","rr","tt"])

        #*valid email
        get_data = {"email":"qq@qq.com"}
        get_response = self.send_request.post(format="json",path="/v1/api/employer/delete",data=get_data)
        message_test = self.assertEqual(list(get_response.json().keys()),["success"])
        status_code_test = self.assertEqual(get_response.status_code,202)


    #* testing invalid delete (POST REQUEST)
    def test_invalid_post_delete(self):
        path = "/v1/api/employer/delete"

        #* invalid field name
        fields = {"sa":"sa"}
        response = {"message":["error","required_fields"],"status":404}
        method = "post"
        invalid_field_name = {"fields":fields,"response":response,"method":method}

        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        method = "post"
        empty_json = {"fields":fields,"response":response,"method":method}

        #* extra fields
        fields = {"id":1,"email":"aa@aa.com"}
        response = {"message":["error"],"status":404}
        method = "post"
        extra_field = {"fields":fields,"response":response,"method":method}


        custom_invalid = self.generic_tests(path=path,custom_fields=[invalid_field_name,empty_json,extra_field])

    #* testing update operations(GET REQUEST)
    def test_valid_get_update(self):
        path = "/v1/api/employer/update"


        #* valid field
        fields = {"email":"qq@qq.com"}
        response = {"message":["success","employer_json"],"status":200}
        method = "get"
        valid_get_request = {"fields":fields,"response":response,"method":method}

        custom_valid = self.generic_tests(path=path,custom_fields=[valid_get_request])

    #* testing uipdate invalid fields(GET REQUEST)
    def test_invalid_get_update(self):
        path = "/v1/api/employer/update"


        #* invalid email
        fields = {"email":"aa@aa.com"}
        response = {"message":["error"],"status":404}
        method = "get"
        invalid_email = {"fields":fields,"response":response,"method":method}

        #* invalid field name
        fields = {"invalid":"qq@qq.com"}
        response = {"message":["error","required_fields"],"status":404}
        method = "get"
        invalid_field_name = {"fields":fields,"response":response,"method":method}

        #* empty json
        fields = {}
        response = {"message":["error","required_fields"],"status":404}
        method = "get"
        empty_json = {"fields":fields,"response":response,"method":method}


        #* adding additional field
        fields = {"email":"aa@aa.com","update_data":{"first_name":"kaka"}}
        response = {"message":["error"],"status":404}
        method = "get"
        update_data_field= {"fields":fields,"response":response,"method":method}


        custom_invalid = self.generic_tests(path=path,custom_fields=[invalid_email,invalid_field_name,empty_json,update_data_field])
        
        
    #* testing update valid fields(POST REQUEST)
    def test_update_data_valid_post(self):
        path = "/v1/api/employer/update"
        method = "post"

        #*valid first_name
        fields = {"email":"qq@qq.com","update_data":{"first_name":"kaka"}}
        response = {"message":["success","employer_json"],"status":201}
        valid_fields= {"fields":fields,"response":response,"method":method}

        #*changing into new user
        fields = {"email":"qq@qq.com","update_data":{"user":"banan@banan.com"}}
        response = {"message":["success","employer_json"],"status":201}
        new_user = {"fields":fields,"response":response,"method":method}

        custom_invalid = self.generic_tests(path=path,custom_fields=[valid_fields,new_user])
        #! tested it internally inside the generic_tests(when changing the user from qq to banan the employer not exists with the email of qq because its changed to banan)
        #* after the change we want to make sure that qq@qq.com not exists


    def test_update_data_invalid_fields(self):
        path = "/v1/api/employer/update"
        method = "post"

        #*invalid email
        fields = {"email":"aa@aa.com","update_data":{"first_name":"kaka"}}
        response = {"message":["error"],"status":404}
        invalid_email = {"fields":fields,"response":response,"method":method}

        #*empty update data
        fields = {"email":"qq@qq.com","update_data":{}}
        response = {"message":["error","json_example"],"status":404}
        empty_update_data= {"fields":fields,"response":response,"method":method}

        #*changing user to existing one as employer
        fields = {"email":"qq@qq.com","update_data":{"user":"ww@ww.com"}}
        response = {"message":["error"],"status":404}
        already_exists_as_employer = {"fields":fields,"response":response,"method":method}

        #*changing into new user that doesnt exist as employer
        fields = {"email":"qq@qq.com","update_data":{"user":"banan@banan.com"}}
        response = {"message":["error"],"status":404}
        new_user = {"fields":fields,"response":response,"method":method}


        #*changing user to unexisting user
        fields = {"email":"qq@qq.com","update_data":{"user":"not_existing@not_existing.com"}}
        response = {"message":["error"],"status":404}
        unexisting_user = {"fields":fields,"response":response,"method":method}

        #*changing user to same user 
        fields = {"email":"qq@qq.com","update_data":{"user":"qq@qq.com"}}
        response = {"message":["error"],"status":404}
        same_user = {"fields":fields,"response":response,"method":method}

        #*changing user to user in another company
        fields = {"email":"qq@aa.com","update_data":{"user":"aa@aa.com"}}
        response = {"message":["error"],"status":404}
        same_user = {"fields":fields,"response":response,"method":method}




        custom_invalid = self.generic_tests(path=path,custom_fields=[invalid_email,empty_update_data,already_exists_as_employer,unexisting_user,same_user,new_user])
