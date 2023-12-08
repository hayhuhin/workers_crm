from django.test import TestCase
from mongodb_connector import MongoDBConstructor

class TestMongoDBConnectorClasses(TestCase):
    def setUp(self):
        self.uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
        self.good_dict = {"name":"ben","graph_permited":True,"graph_type":"general_graph"}
        self.minimal_data = {"name":"ben","graph_permited":True,"graph_type":"general_graph"}


    def test_user_exists_return_False(self):
        """
        this test is for the structured data method that runs first and then returns structured data as a class variable
        """
        #instantiating the mongodbclass
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()
        #now checking if the user exists
        user_exists = self.mdb.user_exists()
        self.assertEqual(user_exists,False)




    def test_user_exists_return_True(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        #method that creating basic record if the user doesnt exists
        self.mdb.create_basic_record()
        user_exists = self.mdb.user_exists()
        self.assertEqual(user_exists,True)



    def test_creating_basic_record_user_notExists(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        #creating basic record if user not exists
        basic_record_created = self.mdb.create_basic_record()
        self.assertEqual(basic_record_created,True)

    def test_creating_basic_record_user_exists(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()
        #first time creating basic record
        self.mdb.create_basic_record()

        #now that the user is exists now we will check if it will raise ValueError
        create_basic = self.mdb.create_basic_record()
        self.assertEqual(create_basic,False)
            

    def test_graph_records_returns_record_dict(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        #creating basic data
        self.mdb.create_basic_record()

        #dumping random records for testing only
        self.mdb.dump_test_records()

        #checking if the graph_records returning dict with the required data
        records_result = self.mdb.graph_records()
        expected_data = {'0': 
                            {'graph_title': 'Graph',
                            'graph_description': 'No Description',
                            'graph_type': 'bar_graph',
                            'created_at': '2023-12-5. 20:15',
                            'x': ['December 2023'],
                            'y': [7491],
                            'start_date': '2023-11-26',
                            'end_date': '2024-01-06',
                            'position': 1},
                        '1': {'graph_title': 'Graph',
                            'graph_description': 'No Description',
                            'graph_type': 'bar_graph',
                            'created_at': '2023-12-5. 20:15',
                            'x': ['December 2023'],
                            'y': [7491],
                            'start_date': '2023-11-26',
                            'end_date': '2024-01-06',
                            'position': 2}}
        
        self.assertEqual(records_result,expected_data)
        
    def test_graph_records_returns_empty_list(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        #creating basic data
        self.mdb.create_basic_record()
    
        #searching for records but its empty
        # self.mdb.dump_test_records()
        records_result = self.mdb.graph_records()
        self.assertEqual(records_result,{})


    def test_remove_records(self):
        #first instantiating and deleting existing data
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        #creating first data
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()
        
        self.mdb.remove_record(required_record=1,delete_all=False)
        records_result = self.mdb.graph_records()
        expected_result = {'0': {'graph_title': 'Graph', 
                                'graph_description': 'No Description', 'graph_type': 
                                'bar_graph', 'created_at': '2023-12-5. 20:15', 'x': ['December 2023'], 'y': [7491], 'start_date': '2023-11-26', 'end_date': '2024-01-06', 'position': 1}}
        self.assertEqual(records_result,expected_result)


    def test_remove_records_invalid_input(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        #creating first data
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()

        with self.assertRaises(ValueError,msg="this record not exists"):
            self.mdb.remove_record(required_record=100,delete_all=False)

        with self.assertRaises(ValueError,msg="this record not exists"):
            self.mdb.remove_record(required_record="wrong_input",delete_all=False)


    def test_remove_records_user_not_exists(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()


        with self.assertRaises(ValueError,msg="the user not exists"):
            self.mdb.remove_record(required_record=1,delete_all=False)


    def test_remove_records_user_not_exists(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        self.mdb.create_basic_record()
        with self.assertRaises(ValueError,msg="the user exists but dont have records"):
            self.mdb.remove_record(required_record=1,delete_all=False)


    def test_delete_all(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        #creating first data
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()

        #removing all records
        self.mdb.remove_record(required_record=1,delete_all=True)
        user_exists = self.mdb.user_exists()
        self.assertEqual(user_exists,False)

    def test_graph_positions(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        #creating first data
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()

        #extracting list with the positions
        positions = self.mdb.graph_positions()
        expected_result = [1,2]

        self.assertEqual(positions,expected_result)

    def test_graph_positions_no_positions(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()

        #creating first data
        self.mdb.create_basic_record()


        with self.assertRaises(ValueError,msg="no records exists"):
            positions = self.mdb.graph_positions()


    def test_graph_positions_no_user(self):
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        self.mdb.drop_user_data()


        with self.assertRaises(ValueError,msg="user not exists"):
            positions = self.mdb.graph_positions()

