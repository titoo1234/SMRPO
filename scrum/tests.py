from django.test import TestCase
from .views import check_sprint_dates

# Create your tests here.
class SprintTestCase(TestCase):
    
    def test_sprint_date_regulation_true(self):
        start_date = '2021-05-01'
        end_date = '2021-05-15'
        duration = 14
        self.assertTrue(check_sprint_dates(start_date, end_date, duration))

    def test_sprint_date_regulation_false(self):
        start_date = '2021-05-01'
        end_date = '2021-05-15'
        duration = 13
        self.assertFalse(check_sprint_dates(start_date, end_date, duration))