# Generated by Django 5.0.2 on 2024-03-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0013_projectmember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]