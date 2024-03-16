# Generated by Django 4.2.10 on 2024-03-16 20:42

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0019_remove_userstory_users_userstory_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userstory',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Upper('name'), name='Unique name'),
        ),
    ]
