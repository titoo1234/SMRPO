# Generated by Django 5.0.2 on 2024-03-10 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0012_userstory_acceptance_tests_userstory_business_value_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrum.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrum.user')),
            ],
            options={
                'unique_together': {('user', 'project')},
            },
        ),
    ]