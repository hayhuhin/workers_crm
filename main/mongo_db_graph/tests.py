from django.test import TestCase
from mongodb_connector import MongoDBConstructor

class TestMongoDBConnectorClasses(TestCase):
    def setUp(self):
        self.uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
        self.good_dict = {"user_name":"ben","graph_permited":True,"graph_type":"general_graph"}
        self.delete_all = MongoDBConstructor(uri=self.uri,db="test",collection="test",user_data=self.good_dict).remove_record(required_record=1,delete_all=True)


    def test_structured_data(self):
        """
        this test is for the structured data method that runs first and then returns structured data as a class variable
        """
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user_data=self.good_dict)
        #the mdb.raw_dict is the class variable that calls the structured_data and gets the raw data for later usage
        available_pos_result = self.mdb.raw_dict

        expected_dict = {'user_name': 'ben', 'db': 'test', 'collection': 'test', 'graph_permited': True, 'graph_type': 'general_graph', 'graph_records': {'records': {}}, 'graph_repr': '1_row'}
        self.assertEqual(available_pos_result,expected_dict)
        self.delete_all()

    def test_delete_all_data(self):
        mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user_data=self.good_dict)
        removed_result = mdb.remove_record(required_record=1,delete_all=True)
        self.assertEqual(mdb.raw_dict,{})

    def test_structured_data(self):
        user_data_input = {'user_name': 'ben', 'db': 'test', 'collection': 'test', 'graph_permited': True, 'graph_type': 'general_graph', 'graph_records': {'records': {'1':{'record_data'},'2':{'record_data'}}}, 'graph_repr': '1_row'}
        self.mdb = MongoDBConstructor(uri=self.uri,db="test",collection="test",user_data=user_data_input)
        record_output = self.mdb.raw_dict
        expected_dict = {'user_name': 'ben', 'db': 'test', 'collection': 'test', 'graph_permited': True, 'graph_type': 'general_graph', 'graph_records': {'records': {"1":{"record_data"},"2":{"record_data"}}}, 'graph_repr': '1_row'}
        self.assertEqual(record_output,expected_dict

