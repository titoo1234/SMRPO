# Generated by Django 5.0.2 on 2024-04-06 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0029_task_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]
