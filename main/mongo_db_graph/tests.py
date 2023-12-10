from django.test import TestCase
from mongodb_connector import MongoDBConstructor

class TestMongoDBConnectorClasses(TestCase):
    def setUp(self):
        self.uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
        self.good_dict = {"name":"ben","graph_permited":True,"graph_type":"general_graph"}
        self.minimal_data = {"name":"ben","graph_permited":True,"graph_type":"general_graph"}
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben",max_records=7)

    def tearDown(self):
        self.mdb.drop_user_data()


    def test_user_exists_return_False(self):
        """
        this test is for the structured data method that runs first and then returns structured data as a class variable
        """
        #instantiating the mongodbclass
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()
        #now checking if the user exists
        user_exists = self.mdb.user_exists()
        self.assertEqual(user_exists,False)


    def test_user_exists_return_True(self):
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()

        #method that creating basic record if the user doesnt exists
        self.mdb.create_basic_record()
        user_exists = self.mdb.user_exists()
        self.assertEqual(user_exists,True)


    def test_creating_basic_record_user_notExists(self):
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()

        #creating basic record if user not exists
        basic_record_created = self.mdb.create_basic_record()
        self.assertEqual(basic_record_created,True)


    def test_creating_basic_record_user_exists(self):
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()
        #first time creating basic record
        self.mdb.create_basic_record()

        #now that the user is exists now we will check if it will raise ValueError
        create_basic = self.mdb.create_basic_record()
        self.assertEqual(create_basic,False)
            

    def test_graph_records_returns_record_dict(self):
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()

        #creating basic data
        self.mdb.create_basic_record()

        #dumping random records for testing only
        self.mdb.dump_test_records()

        #checking if the graph_records returning dict with the required data
        records_result = self.mdb.graph_records()
        expected_data = {'1': 
                            {'graph_title': 'Graph',
                            'graph_description': 'No Description',
                            'graph_type': 'bar_graph',
                            'created_at': '2023-12-5. 20:15',
                            'x': ['December 2023'],
                            'y': [7491],
                            "y_2":[],
                            "sql_database":"income",
                            'start_date': '2023-11-26',
                            'end_date': '2024-01-06'},
                        '2': {'graph_title': 'Graph',
                            'graph_description': 'No Description',
                            'graph_type': 'bar_graph',
                            'created_at': '2023-12-5. 20:15',
                            'x': ['December 2023'],
                            'y': [7491],
                            "y_2":[],
                            "sql_database":"income",
                            'start_date': '2023-11-26',
                            'end_date': '2024-01-06',}}
        
        self.assertEqual(records_result,expected_data)
 
       
    def test_graph_records_returns_empty_list(self):
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()

        #creating basic data
        self.mdb.create_basic_record()
    
        #searching for records but its empty
        # self.mdb.dump_test_records()
        records_result = self.mdb.graph_records()
        self.assertEqual(records_result,{})


    def test_remove_records(self):
        #first instantiating and deleting existing data
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()

        #creating first data
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()
        self.mdb.remove_record(required_record=1,delete_all=False)
        records_result = self.mdb.graph_records()
        expected_result = {'1': {'graph_title': 'Graph', 
                                'graph_description': 'No Description',
                                'graph_type': 'bar_graph',
                                'created_at': '2023-12-5. 20:15',
                                'x': ['December 2023'],
                                'y': [7491],
                                "y_2":[],   
                                "sql_database":"income",
                                'start_date': '2023-11-26',
                                'end_date': '2024-01-06'}}
        self.maxDiff = None
        self.assertEqual(records_result,expected_result)


    def test_remove_records_invalid_input(self):
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()

        #creating first data
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()

        with self.assertRaises(ValueError,msg="this record not exists"):
            self.mdb.remove_record(required_record=100,delete_all=False)

        with self.assertRaises(ValueError,msg="this record not exists"):
            self.mdb.remove_record(required_record="wrong_input",delete_all=False)


    def test_remove_records_user_not_exists(self):
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()


        with self.assertRaises(ValueError,msg="the user not exists"):
            self.mdb.remove_record(required_record=1,delete_all=False)


    def test_remove_records_user_not_exists(self):
        # self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user="ben")
        # self.mdb.drop_user_data()

        self.mdb.create_basic_record()
        with self.assertRaises(ValueError,msg="the user exists but dont have records"):
            self.mdb.remove_record(required_record=1,delete_all=False)


    def test_delete_all(self):

        #creating first data
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()

        #removing all records
        self.mdb.remove_record(required_record=1,delete_all=True)
        user_exists = self.mdb.user_exists()
        self.assertEqual(user_exists,False)


    def test_graph_positions(self):

        #creating first data
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()

        #extracting list with the positions
        positions = self.mdb.graph_positions()
        expected_result = ["1","2"]

        self.assertEqual(positions,expected_result)

    
    def test_graph_positions_no_positions(self):

        #creating first data
        self.mdb.create_basic_record()


        with self.assertRaises(ValueError,msg="no records exists"):
            positions = self.mdb.graph_positions()


    def test_graph_positions_no_user(self):

        with self.assertRaises(ValueError,msg="user not exists"):
            positions = self.mdb.graph_positions()


    def test_add_record_user_not_exist(self):
        
        new_record = {  
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        self.mdb.add_record(new_record=new_record)
        #this method returns list with the existing positions
        positions = self.mdb.graph_positions()

        self.assertEqual(positions,["1"])

        #this method returns dict with the existing records
        expected_data = {"1":{  
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }}
        records = self.mdb.graph_records()
        self.assertEqual(records,expected_data)


    def test_add_records_first_time(self):

        #creating new user data
        self.mdb.create_basic_record()
        new_record = {
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        self.mdb.add_record(new_record=new_record)

        positions = self.mdb.graph_positions()

        self.assertEqual(positions,["1"])

        #this method returns dict with the existing records
        expected_data = {"1":{  
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }}
        records = self.mdb.graph_records()
        self.assertEqual(records,expected_data)


    def test_add_records_records_exist(self):

        #creating new user data
        self.mdb.create_basic_record()
        #adding 2 records to the db
        self.mdb.dump_test_records()
        new_record = {
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
       #creating additional record
        self.mdb.add_record(new_record=new_record)

        positions = self.mdb.graph_positions()
        #expected positions are ["1","2","3"]
        self.assertEqual(positions,["1","2","3"])

        expected_data = {
                    "1": {
                    'graph_title': 'Graph',
                    'graph_description': 'No Description',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023' ],
                    'y': [ 7491 ],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    },
                    "2": {
                    'graph_title': 'Graph',
                    'graph_description': 'No Description',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023' ],
                    'y': [ 7491 ],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    },
                    "3":{  
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }}
        records = self.mdb.graph_records()
        self.assertEqual(records,expected_data)


    def test_add_record_position_EQ_value(self):
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()
        new_record = {
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        self.mdb.add_record(new_record=new_record,position=33)

        positions = self.mdb.graph_positions()
        #expected positions are ["1","2","33"]
        self.assertEqual(positions,["1","2","33"])

        expected_data = {
                    "1": {
                    'graph_title': 'Graph',
                    'graph_description': 'No Description',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023' ],
                    'y': [ 7491 ],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    },
                    "2": {
                    'graph_title': 'Graph',
                    'graph_description': 'No Description',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023' ],
                    'y': [ 7491 ],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    },
                    "33":{  
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }}
        
        records = self.mdb.graph_records()
        self.assertEqual(records,expected_data)


    def test_add_record_position_EQ_no_records(self):
        new_record = {
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        self.mdb.add_record(new_record=new_record,position=33)

        positions = self.mdb.graph_positions()
        #expected positions are ["33"]
        self.assertEqual(positions,["33"])

        expected_data = {
                    "33":{  
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }}
        
        records = self.mdb.graph_records()
        self.assertEqual(records,expected_data)


    def test_switch_records(self):
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()
        
        
        previous_result = self.mdb.graph_records()
        previous_result_expected = {
            '1': {'graph_title': 'Graph',
                'graph_description': 'No Description',
                'graph_type': 'bar_graph',
                'created_at': '2023-12-5. 20:15',
                'x': ['December 2023'],
                'y': [7491],
                "y_2":[],
                "sql_database":"income",
                'start_date': '2023-11-26',
                'end_date': '2024-01-06'},
            '2': {'graph_title': 'Graph',
                'graph_description': 'No Description',
                'graph_type': 'bar_graph',
                'created_at': '2023-12-5. 20:15',
                'x': ['December 2023'],
                'y': [7491],
                "y_2":[],
                "sql_database":"income",
                'start_date': '2023-11-26',
                'end_date': '2024-01-06'}}
        
        
        new_record = {
            'graph_title': 'test graph',
            'graph_description': 'some desc',
            'graph_type': 'bar_graph',
            'created_at': '2023-12-5. 20:15',
            'x': [ 'December 2023','January 2023'],
            'y': [ 7491,22112],
            "y_2":[],
            "sql_database":"income",
            'start_date': '2023-11-26',
            'end_date': '2024-01-06',
            }
        self.mdb.add_record(new_record=new_record)
        # test = self.mdb.sort_records()
        self.mdb.switch_records(src_position=1,dst_position=3)
        updated_result = self.mdb.graph_records()
        updated_result_expected = {
            '1': {'graph_title': 'test graph',
                'graph_description': 'some desc',
                'graph_type': 'bar_graph',
                'created_at': '2023-12-5. 20:15',
                'x': ['December 2023', 'January 2023'],
                'y': [7491, 22112],
                "y_2":[],
                "sql_database":"income",
                'start_date': '2023-11-26',
                'end_date': '2024-01-06'},
            '2': {'graph_title': 'Graph',
                'graph_description': 'No Description',
                'graph_type': 'bar_graph',
                'created_at': '2023-12-5. 20:15',
                'x': ['December 2023'],
                'y': [7491],
                "y_2":[],
                "sql_database":"income",
                'start_date': '2023-11-26',
                'end_date': '2024-01-06'},
            '3': {'graph_title': 'Graph',
                'graph_description': 'No Description',
                'graph_type': 'bar_graph',
                'created_at': '2023-12-5. 20:15',
                'x': ['December 2023'],
                'y': [7491],
                "y_2":[],
                "sql_database":"income",
                'start_date': '2023-11-26',
                'end_date': '2024-01-06'}
                }

        self.assertEqual(previous_result,previous_result_expected)
        self.assertEqual(updated_result,updated_result_expected)

    
    def test_switch_invalid_src(self):
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()

        with self.assertRaises(ValueError,msg="src_position is invalid"):
            self.mdb.switch_records(src_position=5,dst_position=1)


    def test_switch_invalid_dst(self):
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()

        with self.assertRaises(ValueError,msg="dst_position is invalid"):
            self.mdb.switch_records(src_position=1,dst_position=5)
            

    def test_compare_record(self):
        self.mdb.create_basic_record()
        self.mdb.dump_test_records()
        self.mdb.compare_record(position_1="1",position_2="2")
        data = self.mdb.graph_records()
        expected_data = {'1':
                          {'graph_title': 'Graph',
                            'graph_description': 'No Description',
                            'graph_type': 'bar_graph_compared',
                            'created_at': '2023-12-5. 20:15',
                            'x': ['December 2023'],
                            'y': [7491],
                            'y_2': [7491],
                            'sql_database':'income',
                            'sql_database_compared':'outcome',
                            'start_date': '2023-11-26',
                            'end_date': '2024-01-06'}}
        self.assertEqual(data,expected_data)

    
    def test_compare_record_user_not_exists(self):
        with self.assertRaises(ValueError):
            self.mdb.compare_record(position_1="1",position_2="2")


    def test_compare_record_user_no_records(self):
        self.mdb.create_basic_record()
        with self.assertRaises(ValueError):
            data = self.mdb.graph_records()
            print(data)
            self.mdb.compare_record(position_1="1",position_2="2")


    def test_compare_record_one_record(self):
        self.mdb.create_basic_record()
        new_record = {
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2': [],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        self.mdb.add_record(new_record=new_record)
        with self.assertRaises(ValueError,msg="cant compare when have only one record"):
            self.mdb.compare_record(position_1="1",position_2="2")


    def test_edit_graph_repr(self):
        self.mdb.create_basic_record()
        self.mdb.edit_graph_repr("2_row")
        data = self.mdb.find_data({"name":"ben"})
        expected_result = {'name': 'ben', 'db': 'test', 'collection': 'test', 'graph_permited': True, 'graph_db_type': 'general_graph', 'graph_records': {}, 'graph_repr': '2_row','ordered_list':[]
}
        self.assertEqual(data,expected_result)


    def test_remove_record_begining(self):
        self.mdb.create_basic_record()
        # data = self.mdb.populate_record()
        new_record = {
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        
        new_record2 = {
                    'graph_title': 'test graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        new_record3 = {
                    'graph_title': 'valeri',
                    'graph_description': 'valeri',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        self.mdb.add_record(new_record=new_record3)
        self.mdb.add_record(new_record=new_record)
        self.mdb.add_record(new_record=new_record2)

        self.mdb.remove_record(required_record="1")
        newest = self.mdb.graph_records()
        expected_result = {'1':
                            {'graph_title': 'test graph', 'graph_description': 'some desc', 'graph_type': 'bar_graph', 'created_at': '2023-12-5. 20:15', 'x': ['December 2023', 'January 2023'], 'y': [7491, 22112], 'y_2': [], 'sql_database': 'income', 'start_date': '2023-11-26', 'end_date': '2024-01-06'}, '2': {'graph_title': 'test graph', 'graph_description': 'some desc', 'graph_type': 'bar_graph', 'created_at': '2023-12-5. 20:15', 'x': ['December 2023', 'January 2023'], 'y': [7491, 22112], 'y_2': [], 'sql_database': 'income', 'start_date': '2023-11-26', 'end_date': '2024-01-06'}}
        self.assertEqual(newest,expected_result)


    def test_remove_record_center(self):
        self.mdb.create_basic_record()
        # data = self.mdb.populate_record()
        new_record = {
                    'graph_title': 'first graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }     
        new_record2 = {
                    'graph_title': 'second graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        new_record3 = {
                    'graph_title': 'third graph',
                    'graph_description': 'valeri',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        self.mdb.add_record(new_record=new_record)
        self.mdb.add_record(new_record=new_record2)
        self.mdb.add_record(new_record=new_record3)

        self.mdb.remove_record(required_record="2")
        newest = self.mdb.graph_records()
        expected_result = {'1':
                                {
                                'graph_title': 'first graph',
                                'graph_description': 'some desc',
                                'graph_type': 'bar_graph',
                                'created_at': '2023-12-5. 20:15',
                                'x': [ 'December 2023','January 2023'],
                                'y': [ 7491,22112],
                                'y_2':[],
                                'sql_database':'income',
                                'start_date': '2023-11-26',
                                'end_date': '2024-01-06',
                                },
                            '2':{
                                'graph_title': 'third graph',
                                'graph_description': 'valeri',
                                'graph_type': 'bar_graph',
                                'created_at': '2023-12-5. 20:15',
                                'x': [ 'December 2023','January 2023'],
                                'y': [ 7491,22112],
                                'y_2':[],
                                'sql_database':'income',
                                'start_date': '2023-11-26',
                                'end_date': '2024-01-06',
                            }}
        self.assertEqual(newest,expected_result)


    def test_remove_record_end(self):
        self.mdb.create_basic_record()
        # data = self.mdb.populate_record()
        new_record = {
                    'graph_title': 'first graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        
        new_record2 = {
                    'graph_title': 'second graph',
                    'graph_description': 'some desc',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        new_record3 = {
                    'graph_title': 'third',
                    'graph_description': 'valeri',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023','January 2023'],
                    'y': [ 7491,22112],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }
        self.mdb.add_record(new_record=new_record)
        self.mdb.add_record(new_record=new_record2)
        self.mdb.add_record(new_record=new_record3)

        self.mdb.remove_record(required_record="3")
        newest = self.mdb.graph_records()
        expected_result = {'1':
                                {
                                'graph_title': 'first graph',
                                'graph_description': 'some desc',
                                'graph_type': 'bar_graph',
                                'created_at': '2023-12-5. 20:15',
                                'x': [ 'December 2023','January 2023'],
                                'y': [ 7491,22112],
                                'y_2':[],
                                'sql_database':'income',
                                'start_date': '2023-11-26',
                                'end_date': '2024-01-06',
                                },
                            '2':{
                                'graph_title': 'second graph',
                                'graph_description': 'some desc',
                                'graph_type': 'bar_graph',
                                'created_at': '2023-12-5. 20:15',
                                'x': [ 'December 2023','January 2023'],
                                'y': [ 7491,22112],
                                'y_2':[],
                                'sql_database':'income',
                                'start_date': '2023-11-26',
                                'end_date': '2024-01-06',
                    }}
        self.assertEqual(newest,expected_result)


    