import datetime
from django.db import migrations
from ..models import User,Project,AssignedRole,ProjectMember,Sprint

def create_default_data(apps, schema_editor):
    admin = User.objects.get(username='ad')
    uporabnik = User.objects.get(username='uporabnik')
    uporabnik1 = User.objects.get(username='Veseli Ribnčan')
    fixed_date = datetime.datetime(2024, 3, 25)

    project = Project.objects.create(name='Default Project', creation_date=datetime.datetime.now(),  description='Default project description', creator=admin)
    ProjectMember.objects.create(user=admin, project=project)
    ProjectMember.objects.create(user=uporabnik1, project=project)
    ProjectMember.objects.create(user=uporabnik, project=project)
    AssignedRole.objects.create(user=admin, project=project, role='product_owner')
    AssignedRole.objects.create(user=uporabnik1, project=project, role='methodology_manager')
    AssignedRole.objects.create(user=uporabnik1, project=project, role='development_team_member')
    AssignedRole.objects.create(user=uporabnik, project=project, role='development_team_member')

    # SPRINT
    # =============================================
    sprint_start_date = datetime.datetime(2024, 3, 26)
    sprint_end_date = datetime.datetime(2024, 4, 26)
    default_sprint = Sprint.objects.create(project=project, start_date=sprint_start_date, end_date=sprint_end_date,velocity = 20)

    
class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0024_remove_task_end_date_remove_task_name_and_more'),  # Replace 'previous_migration_file' with the name of the previous migration file
    ]

    operations = [
        migrations.RunPython(create_default_data),
    ]
