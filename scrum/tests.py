from django.test import TestCase
from datetime import datetime
from django.utils import timezone

from .views import check_sprint_dates
from scrum.models import Project, User, Sprint

# Create your tests here.
class SprintTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(name='TestUser', surname='TestSurname', mail='test@test.com', username="TestUsername", password="TestPassword", admin_user=True, active=True)
        project = Project.objects.create(name='TestProject', creation_date='2021-05-01', description='TestDescription', creator=user)
        sprints = []
        tmp = datetime.now()
        for i in range(1, 6):
            # create sprints that each last 14 and do not overlap
            end = tmp + timezone.timedelta(days=14)
            sprint = Sprint.objects.create(project=project, start_date=tmp.strftime('%Y-%m-%d'), end_date=end.strftime('%Y-%m-%d'), duration=14)
            tmp = end
            sprints.append(sprint)
        cls.sprints = sprints

    def test_sprint_date_regulation_true(self):
        now = datetime.now() + timezone.timedelta(days=84)
        start_date = now.strftime('%Y-%m-%d')
        end_date = (now + timezone.timedelta(days=14)).strftime('%Y-%m-%d')
        duration = 14
        self.assertTrue(check_sprint_dates(start_date, end_date, duration, self.sprints))

    def test_sprint_date_regulation_false(self):
        start_date = '2021-05-01'
        end_date = '2021-05-15'
        duration = 13
        self.assertFalse(check_sprint_dates(start_date, end_date, duration, self.sprints))
    
    #def test_sprint_start_in_past(self):
