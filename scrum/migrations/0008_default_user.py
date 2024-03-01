from django.db import migrations
from ..models import User

def create_default_user(apps, schema_editor):
    User.objects.create(
        name='admin',
        surname='admin',
        mail='default@example.com',
        username='ad',
        admin_user=True,  # Assuming this is your admin user
        active=True,  # Assuming the user is active
        password='ad'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0007_user_active'),  # Replace 'previous_migration_file' with the name of the previous migration file
    ]

    operations = [
        migrations.RunPython(create_default_user),
    ]
