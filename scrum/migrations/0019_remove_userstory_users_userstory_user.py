# Generated by Django 4.2.10 on 2024-03-16 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0018_userstory_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstory',
            name='users',
        ),
        migrations.AddField(
            model_name='userstory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scrum.user'),
        ),
    ]
