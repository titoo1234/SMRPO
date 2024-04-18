# Generated by Django 5.0.2 on 2024-04-10 08:49
import datetime
from django.db import migrations
from ..models import *

def create_default_data(apps, schema_editor):
    pass
    # uporabnik = User.objects.get(username='uporabnik')
    # project = Project.objects.get(name='Default Project')

    # sprint_start_date = datetime.datetime(2024, 3, 11)
    # sprint_end_date = datetime.datetime(2024, 3, 25)
    # default_sprint = Sprint.objects.create(project=project, start_date=sprint_start_date, end_date=sprint_end_date,velocity = 15)
    # user_story = UserStory.objects.create(name="Default user story", description="some random text", project=project, sprint=default_sprint, business_value=8, priority="must_have", size=6, original_estimate=7, workflow="done", user=uporabnik, accepted=True, rejected=False, comment=None)
    # task = Task.objects.create(description="Default task", time_spent=3, assigned_user=uporabnik, user_story=user_story, accepted=True, done=True,estimate=3, rejected=False,started=False, deleted=False)


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0036_alter_task_options_task_task_number'),
    ]

    operations = [
        migrations.RunPython(create_default_data),
    ]
