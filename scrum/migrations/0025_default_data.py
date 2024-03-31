import datetime
from django.db import migrations
from ..models import User,Project,AssignedRole,ProjectMember

def create_default_data(apps, schema_editor):
    admin = User.objects.get(username='ad')
    uporabnik = User.objects.get(username='uporabnik')
    uporabnik1 = User.objects.get(username='Veseli Ribnčan')
    project = Project.objects.create(name='Default Project', creation_date=datetime.datetime.now(),  description='Default project description', creator=admin)
    ProjectMember.objects.create(user=admin, project=project)
    ProjectMember.objects.create(user=uporabnik1, project=project)
    ProjectMember.objects.create(user=uporabnik, project=project)
    AssignedRole.objects.create(user=admin, project=project, role='product_owner')
    AssignedRole.objects.create(user=uporabnik1, project=project, role='methodology_manager')
    AssignedRole.objects.create(user=uporabnik1, project=project, role='development_team_member')
    AssignedRole.objects.create(user=uporabnik, project=project, role='development_team_member')

    
    
class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0024_remove_task_end_date_remove_task_name_and_more'),  # Replace 'previous_migration_file' with the name of the previous migration file
    ]

    operations = [
        migrations.RunPython(create_default_data),
    ]
