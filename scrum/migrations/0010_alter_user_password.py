# Generated by Django 5.0.2 on 2024-03-01 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0009_merge_20240301_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
