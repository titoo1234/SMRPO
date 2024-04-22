from django.db import migrations
from ..models import User
import hashlib

def create_default_user(apps, schema_editor):
    User.objects.create(
        name='admin',
        surname='admin',
        mail='default@example.com',
        username='ad',
        admin_user=True,  # Assuming this is your admin user
        active=True,  # Assuming the user is active
        password=hashlib.sha256("ad".encode('utf-8')).hexdigest()
    )
    User.objects.create(
        name='uporabnik',
        surname='uporabnik',
        mail='uporabnik@example.com',
        username='uporabnik',
        admin_user=True,  # Assuming this is your admin user
        active=True,  # Assuming the user is active
        password=hashlib.sha256("uporabnik".encode('utf-8')).hexdigest()
    )
    User.objects.create(
        name='Veseli',
        surname='Ribnčan',
        mail='uporabnik@example.com',
        username='Veseli Ribnčan',
        admin_user=True,  # Assuming this is your admin user
        active=True,  # Assuming the user is active
        password=hashlib.sha256("Veseli Ribnčan".encode('utf-8')).hexdigest()
    )
    User.objects.create(
        name='Lojze',
        surname='Slak',
        mail='lojzeslak@example.com',
        username='lojz',
        admin_user=False,  # Assuming this is your admin user
        active=True,  # Assuming the user is active
        password=hashlib.sha256("lojz".encode('utf-8')).hexdigest()
    )
    User.objects.create(
        name='tit',
        surname='tit',
        mail='tit@example.com',
        username='tit',
        admin_user=True,  # Assuming this is your admin user
        active=True,  # Assuming the user is active
        password= hashlib.sha256("tit".encode('utf-8')).hexdigest()
    )

class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0007_user_active'),  # Replace 'previous_migration_file' with the name of the previous migration file
    ]

    operations = [
        migrations.RunPython(create_default_user),
    ]
