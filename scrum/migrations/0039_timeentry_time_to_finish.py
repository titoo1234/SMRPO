# Generated by Django 5.0.2 on 2024-04-17 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0038_alter_task_task_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeentry',
            name='time_to_finish',
            field=models.PositiveIntegerField(default=1),
        ),
    ]