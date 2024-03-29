# Generated by Django 5.0.2 on 2024-02-26 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0005_alter_user_mail'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('product_owner', 'Product Owner'), ('methodology_manager', 'Methodology Manager'), ('development_team_member', 'Development Team Member')], max_length=100)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrum.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrum.user')),
            ],
        ),
    ]
