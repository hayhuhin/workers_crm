from django.test import TestCase
from graph_calculations import GraphCalculator
from graph_presentations import GraphRepresantation
from dashboard.models import Income,Outcome
from django.db.models import Sum


class TestGraphCalculator(TestCase):
    

    def setUp(self):

        self.graph = GraphCalculator("ben",last_save="no save",db=[Income,Outcome],db_func=[Sum])



    def sql_income_data_dumps_unordered(self):
        data = [
        Income(month='2024-6-1',amount=578),
        Income(month='2024-7-2',amount=1212),
        Income(month='2024-8-3',amount=9686),
        Income(month='2024-9-4',amount=19786),
        Income(month='2024-10-5',amount=55992),
        Income(month='2023-11-2',amount=5789),
        Income(month='2023-12-8',amount=3451),
        Income(month='2024-1-9',amount=9606),
        Income(month='2024-2-11',amount=922),
        Income(month='2024-3-24',amount=24000),
        Income(month='2024-4-5',amount=3345),
        Income(month='2024-5-21',amount=9876),
        Income(month='2024-11-6',amount=16987),
        Income(month='2024-12-9',amount=13900),
        Income(month='2025-1-13',amount=7899),
        Income(month='2025-2-23',amount=764),
        Income(month='2025-11-1',amount=888),
        Income(month='2025-12-1',amount=66788),
        Income(month='2025-7-1',amount=9888),
        Income(month='2025-8-1',amount=1988),
        Income(month='2025-9-1',amount=98788),
        Income(month='2025-3-31',amount=540),
        Income(month='2025-4-27',amount=13900),
        Income(month='2025-5-1',amount=19888),
        Income(month='2025-6-1',amount=1988),
        Income(month='2025-10-1',amount=16888),
        Income(month='2023-10-7',amount=1000),
]
        self.income = Income.objects.bulk_create(data)
    

    def sql_income_data_dumps(self):
        data = [
        Income(month='2023-10-7',amount=1000),
        Income(month='2023-11-2',amount=5789),
        Income(month='2023-12-8',amount=3451),
        Income(month='2024-1-9',amount=9606),
        Income(month='2024-2-11',amount=922),
        Income(month='2024-3-24',amount=24000),
        Income(month='2024-4-5',amount=3345),
        Income(month='2024-5-21',amount=9876),
        Income(month='2024-6-1',amount=578),
        Income(month='2024-7-2',amount=1212),
        Income(month='2024-8-3',amount=9686),
        Income(month='2024-9-4',amount=19786),
        Income(month='2024-10-5',amount=55992),
        Income(month='2024-11-6',amount=16987),
        Income(month='2024-12-9',amount=13900),
        Income(month='2025-1-13',amount=7899),
        Income(month='2025-2-23',amount=764),
        Income(month='2025-3-31',amount=540),
        Income(month='2025-4-27',amount=13900),
        Income(month='2025-5-1',amount=19888),
        Income(month='2025-6-1',amount=1988),
        Income(month='2025-7-1',amount=9888),
        Income(month='2025-8-1',amount=1988),
        Income(month='2025-9-1',amount=98788),
        Income(month='2025-10-1',amount=16888),
        Income(month='2025-11-1',amount=888),
        Income(month='2025-12-1',amount=66788),
]
        self.income = Income.objects.bulk_create(data)
        

    def test_sum_month_valid_input(self):
        self.sql_income_data_dumps()
        first_record_request = self.graph.sum_single_month("2024-01-01","income") 
        self.assertEqual(first_record_request[0],"January 2024")
        self.assertEqual(first_record_request[1],9606)
    

    def test_sum_month_invalid_date_input(self):
        self.sql_income_data_dumps()
        with self.assertRaises(ValueError):
            self.graph.sum_single_month("2024","income")

        with self.assertRaises(Exception,msg="invalid db name"):
            self.graph.sum_single_month("2024-01-01","invaliddbname")

        with self.assertRaises(TypeError):
            self.graph.sum_single_month(2024,"income")


    def test_sum_sql_query_not_found(self):
        with self.assertRaises(Exception,msg="the record doesnt exists in the database"):
            self.graph.sum_single_month("2027-01-01","income")
            

    def test_valid_input_fields(self):
        self.sql_income_data_dumps()
        first_record_request = self.graph.sum_by_range("2024-01-01","2024-02-29","income") 
        self.assertEqual(first_record_request[1],["January 2024","February 2024"])
        self.assertEqual(first_record_request[0],[9606,922])
    

    def test_invalid_input(self):
        self.sql_income_data_dumps()
        with self.assertRaises(TypeError):
            self.graph.sum_by_range(555,666,"income")

        with self.assertRaises(Exception):
            self.graph.sum_by_range("555","666","income")


    def test_record_not_exists(self):
        self.sql_income_data_dumps()
        with self.assertRaises(Exception,msg="invalid records input"):
            self.graph.sum_by_range("2028-01-01","2029-01-01","income")
            

    def test_reversed_dates(self):
        self.sql_income_data_dumps()
        with self.assertRaises(Exception,msg="invalid records input"):
            self.graph.sum_by_range("2024-02-29","2024-01-01","income")

    
    def test_months_name_ordered(self):
        self.sql_income_data_dumps()
        result_with_ordered_database = self.graph.sum_by_range("2024-01-01","2025-12-31","income")
        self.assertEqual(result_with_ordered_database[1],
                                    ["January 2024",
                                    "February 2024",
                                    "March 2024",
                                    "April 2024",
                                    "May 2024",
                                    "June 2024",
                                    "July 2024",
                                    "August 2024",
                                    "September 2024",
                                    "October 2024",
                                    "November 2024",
                                    "December 2024",
                                    "January 2025",
                                    "February 2025",
                                    "March 2025",
                                    "April 2025",
                                    "May 2025",
                                    "June 2025",
                                    "July 2025",
                                    "August 2025",
                                    "September 2025",
                                    "October 2025",
                                    "November 2025",
                                    "December 2025"]
                                    )
    

    def test_with_unordered_database(self):
        self.sql_income_data_dumps_unordered()
        result_with_unordered_database = self.graph.sum_by_range("2024-01-01","2025-12-31","income")
        self.assertEqual(result_with_unordered_database[1],
                                    ["January 2024",
                                    "February 2024",
                                    "March 2024",
                                    "April 2024",
                                    "May 2024",
                                    "June 2024",
                                    "July 2024",
                                    "August 2024",
                                    "September 2024",
                                    "October 2024",
                                    "November 2024",
                                    "December 2024",
                                    "January 2025",
                                    "February 2025",
                                    "March 2025",
                                    "April 2025",
                                    "May 2025",
                                    "June 2025",
                                    "July 2025",
                                    "August 2025",
                                    "September 2025",
                                    "October 2025",
                                    "November 2025",
                                    "December 2025"])






class TestGraphRepresentation(TestCase):

    def setUp(self):
        self.graph_repr = GraphRepresantation()

        self.good_data = {
            "graph_repr":"1_row",
            "dict_values":{'graph_title': 'Graph', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ['December 2023'], 'y': [7491], 'start_date': '2023-11-26', 'end_date': '2023-12-29', 'position': 1},
            "graph_type":"bar_graph",
            "path":None,
            "to_html":True
        }
        self.bad_data = {
            "graph_repr":"wrong_repr",
            "dict_values":{'wrong_title': 'wrong_Graph', 'wrong_graph_description': 'No Description', 'wrong_graph_type': 'bar_graph', 'wrong_created_at': '2023-12-6. 6:43', 'wrong_x': ['December 2023'], 'wrong_y': [7491], 'wrong_start_date': '2023-11-26', 'wrong_end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":112233,
            "to_html":112233
        }

    def test_graph_options_wrong_inputs(self):
        

        #wrong title key name
        wrong_title = {
            "graph_repr":"wrong_repr",
            "dict_values":{'wrong_graph_title': 'wrong_title', 'graph_description': 'No Description', 'wrong_graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'wrong_x': ['December 2023'], 'wrong_y': [7491], 'wrong_start_date': '2023-11-26', 'wrong_end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError,msg="the correct value must be existing graph type"):
            wrong_graph_type = self.graph_repr.graph_options(graph_type=self.bad_data["graph_type"],dict_values=wrong_title["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])

        #wrong description key name
        wrong_desc = {
            "graph_repr":"wrong_repr",
            "dict_values":{'graph_title': 'wrong_Graph', 'wrong_graph_description': 'No Description', 'wrong_graph_type': 'bar_graph', 'wrong_created_at': '2023-12-6. 6:43', 'wrong_x': ['December 2023'], 'wrong_y': [7491], 'wrong_start_date': '2023-11-26', 'wrong_end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError):
            wrong_dict_values = self.graph_repr.graph_options(graph_type=self.good_data["graph_type"],dict_values=wrong_desc["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])
        
        #wrong graph_type key name
        wrong_graph_type = {
            "graph_repr":"wrong_repr",
            "dict_values":{'graph_title': 'wrong_Graph', 'graph_description': 'No Description', 'wrong_graph_type': 'bar_graph', 'wrong_created_at': '2023-12-6. 6:43', 'wrong_x': ['December 2023'], 'wrong_y': [7491], 'wrong_start_date': '2023-11-26', 'wrong_end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError,msg="the correct value must be existing graph type"):
            print("passed -- wrong_graph_type")
            wrong_dict_values = self.graph_repr.graph_options(graph_type=wrong_graph_type["graph_type"],dict_values=self.good_data["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])
        
        #wrong create_at key name
        wrong_created_at = {
            "graph_repr":"wrong_repr",
            "dict_values":{'graph_title': 'wrong_Graph', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'wrong_created_at': '2023-12-6. 6:43', 'wrong_x': ['December 2023'], 'wrong_y': [7491], 'wrong_start_date': '2023-11-26', 'wrong_end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError):
            wrong_dict_values = self.graph_repr.graph_options(graph_type=self.good_data["graph_type"],dict_values=wrong_created_at["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])
        
        #wrong x
        wrong_x = {
            "graph_repr":"wrong_repr",
            "dict_values":{'graph_title': 'wrong_Graph', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'wrong_x': ['December 2023'], 'wrong_y': [7491], 'wrong_start_date': '2023-11-26', 'wrong_end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError):
            wrong_dict_values = self.graph_repr.graph_options(graph_type=self.good_data["graph_type"],dict_values=wrong_x["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])
        
        #wrong y key name
        wrong_y = {
            "graph_repr":"wrong_repr",
            "dict_values":{'graph_title': 'wrong_Graph', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ['December 2023'], 'wrong_y': [7491], 'wrong_start_date': '2023-11-26', 'wrong_end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError):
            wrong_dict_values = self.graph_repr.graph_options(graph_type=self.good_data["graph_type"],dict_values=wrong_y["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])
        
        #wrong y_2 key name
        wrong_y_2 = {
            "graph_repr":"wrong_repr",
            "dict_values":{'graph_title': 'wrong_Graph', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ['December 2023'], 'y': [7491], 'wrong_y_2':[4455],'wrong_start_date': '2023-11-26', 'wrong_end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError):
            wrong_dict_values = self.graph_repr.graph_options(graph_type=self.good_data["graph_type"],dict_values=wrong_y_2["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])
        
        #wrong start date key name
        wrong_start_date = {
            "graph_repr":"wrong_repr",
            "dict_values":{'graph_title': 'wrong_Graph', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ['December 2023'], 'y': [7491], 'wrong_start_date': '2023-11-26', 'end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError):
            wrong_dict_values = self.graph_repr.graph_options(graph_type=self.good_data["graph_type"],dict_values=wrong_start_date["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])
        
        #wrong end_date key name
        wrong_end_date = {
            "graph_repr":"wrong_repr",
            "dict_values":{'graph_title': 'wrong_Graph', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ['December 2023'], 'y': [7491], 'start_date': '2023-11-26', 'wrong_end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError):
            wrong_dict_values = self.graph_repr.graph_options(graph_type=self.good_data["graph_type"],dict_values=wrong_end_date["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])
        
        #wrong position key name
        wrong_position = {
            "graph_repr":"wrong_repr",
            "dict_values":{'graph_title': 'wrong_Graph', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ['December 2023'], 'y': [7491], 'start_date': '2023-11-26', 'end_date': '2023-12-29', 'wrong_position': 1},
            "graph_type":"wrong_bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError):
            wrong_dict_values = self.graph_repr.graph_options(graph_type=self.good_data["graph_type"],dict_values=wrong_position["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])
        
    def test_graph_options_bad_values(self):
        #invalid x values
        wrong_x_values = {
            "graph_repr":"1_row",
            "dict_values":{'graph_title': 'title', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': [True], 'y': [7491], 'start_date': '2023-11-26', 'end_date': '2023-12-29', 'position': 1},
            "graph_type":"bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError,msg="x/y/y_2 value types are invalid"):
            print("passed -- wrong_x_values")
            wrong_graph_type = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=wrong_x_values["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])

        #invalid y values
        wrong_y_values = {
            "graph_repr":"1_row",
            "dict_values":{'graph_title': 'title', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ["sa","sa"], 'y': ["sassas","sasa"], 'start_date': '2023-11-26', 'end_date': '2023-12-29', 'position': 1},
            "graph_type":"bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError,msg="len x is not the same as y"):
            print("passed -- wrong_y_values ")
            wrong_graph_type = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=wrong_y_values["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])

        #x and y not the same lenght
        x_and_y_not_same_len = {
            "graph_repr":"1_row",
            "dict_values":{'graph_title': 'title', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ["sa","sa"], 'y': [7491,6675,22,222,222], 'start_date': '2023-11-26', 'end_date': '2023-12-29', 'position': 1},
            "graph_type":"bar_graph",
            "path":None,
            "to_html":True
        }
        with self.assertRaises(ValueError,msg="len x is not the same as y"):
            print("passed -- wrong x_and_y_not_same_len")
            wrong_graph_type = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=x_and_y_not_same_len["dict_values"],graph_repr=self.good_data["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])

        #path value type wrong
        wrong_path_type = {
            "graph_repr":"1_row",
            "dict_values":{'graph_title': 'title', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ["sa","sa"], 'y': [7491,6675,22,222,222], 'start_date': '2023-11-26', 'end_date': '2023-12-29', 'position': 1},
            "graph_type":"bar_graph",
            "path":112233,
            "to_html":True
        }
        with self.assertRaises(ValueError,msg="not str type"):
            print("passed -- wrong_path_type")
            wrong_graph_type = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=self.good_data["dict_values"],graph_repr=self.good_data["graph_repr"],path=wrong_path_type["path"],to_html=self.good_data["to_html"])

        #graph_repr worg type
        wrong_graph_repr_type = {
            "graph_repr":1,
            "dict_values":{'graph_title': 'title', 'graph_description': 'No Description', 'graph_type': 'bar_graph', 'created_at': '2023-12-6. 6:43', 'x': ["sa","sa"], 'y': [7491,6675,22,222,222], 'start_date': '2023-11-26', 'end_date': '2023-12-29', 'position': 1},
            "graph_type":"bar_graph",
            "path":None,
            "to_html":True
        }

        with self.assertRaises(ValueError,msg="not str type"):
            print("passed -- wrong_graph_repr_type")
            wrong_graph_repr = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=self.good_data["dict_values"],graph_repr=wrong_graph_repr_type["graph_repr"],path=self.good_data["path"],to_html=self.good_data["to_html"])


        
        
        

