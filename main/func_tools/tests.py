from django.test import TestCase
from graph_calculations import GraphCalculator
from dashboard.models import Income,Outcome
from django.db.models import Sum


class TestSumMonth(TestCase):
    

    def setUp(self):

        self.graph = GraphCalculator("ben",last_save="no save",db=[Income,Outcome],db_func=[Sum])


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
        Income(month='2025-5-1',amount=19888)
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
            
    

class test_sum_by_range(TestCase):


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
        

    def test_valid_input_fields(self):
        self.sql_income_data_dumps()
        first_record_request = self.graph.sum_by_range("2024-01-01","2024-02-29","income") 
        self.assertEqual(first_record_request[0],["January 2024","February 2024"])
        self.assertEqual(first_record_request[1],[9606,922])
    

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
        self.assertEqual(result_with_ordered_database[0],
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
    

    def test_with_unordered_database(self):
        self.sql_income_data_dumps_unordered()
        result_with_unordered_database = self.graph.sum_by_range("2024-01-01","2025-12-31","income")
        self.assertEqual(result_with_unordered_database[0],
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

