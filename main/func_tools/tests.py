from django.test import TestCase
from graph import sum_single_month,sum_by_range
from dashboard.models import Income
from django.db.models import Sum


class TestSumMonth(TestCase):

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
        first_record_request = sum_single_month("2024-01-01",Income,Sum) 
        self.assertEqual(first_record_request[0],"January 2024")
        self.assertEqual(first_record_request[1],9606)
    
    def test_sum_month_invalid_date_input(self):
        self.sql_income_data_dumps()
        with self.assertRaises(ValueError):
            sum_single_month("2024",Income,Sum)

        with self.assertRaises(TypeError):
            sum_single_month(2024,Income,Sum)


    def test_sum_sql_query_not_found(self):
        with self.assertRaises(Exception,msg="the record doesnt exists in the database"):
            sum_single_month("2027-01-01",Income,Sum)
            
    



class test_sum_by_range(TestCase):
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
        
    def test_invalid_input_fields(self):
        self.sql_income_data_dumps()
        first_record_request = sum_by_range("2024-01-01","2024-02-01",Income,Sum) 
        self.assertEqual(first_record_request[0],list())
        self.assertEqual(first_record_request[1],list())
    